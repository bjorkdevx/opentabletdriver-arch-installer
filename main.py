#!/usr/bin/env python3
import os
import subprocess
import sys

print("Step 1: Asking GitHub CLI (`gh`) for the latest release tag...")
try:
    result = subprocess.run(
        ["gh", "release", "view", "-R", "OpenTabletDriver/OpenTabletDriver", "--json", "tagName", "-q", ".tagName"],
        capture_output=True,
        text=True,
        check=True
    )
    latest_tag = result.stdout.strip()
    latest_version = latest_tag.lstrip("v")
    print(f"-> GitHub CLI returned latest version: {latest_version} (Tag: {latest_tag})")
except subprocess.CalledProcessError as e:
    print(f"Error querying gh CLI: {e}")
    sys.exit(1)

pkgbuild_content = f"""
pkgname=opentabletdriver
_pkgname=OpenTabletDriver
pkgver={latest_version}
pkgrel=1
pkgdesc="A cross-platform open source tablet driver"
arch=('x86_64')
url="https://opentabletdriver.net"
license=('LGPL-3.0-or-later')
depends=('dotnet-runtime-8.0' 'gtk3' 'libevdev')
optdepends=('libxrandr' 'libx11')
makedepends=('dotnet-sdk>=8.0' 'jq' 'git')

conflicts=('digimend-kernel-drivers-dkms-git'
'digimend-drivers-git-dkms' 'digimend-kernel-drivers-dkms'
'digimend-kernel-drivers')
install="notes.install"
options=('!strip')
source=("git+https://github.com/OpenTabletDriver/OpenTabletDriver.git#tag=v$pkgver"
        "notes.install")
sha256sums=('SKIP'
            'SKIP')

_srcdir="OpenTabletDriver"

build() {{
    export DOTNET_CLI_TELEMETRY_OPTOUT=1
    export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=true
    cd "$srcdir/$_srcdir"
    if check_option "strip" y; then
        EXTRA_OPTIONS="/p:DebugType=None /p:DebugSymbols=false"
    fi
    export OTD_CONFIGURATIONS="${{PWD}}/OpenTabletDriver.Configurations/Configurations"
    ./eng/bash/package.sh --package Generic -c Release -- $EXTRA_OPTIONS
}}

package() {{
    cd "$srcdir/$_srcdir"
    cp -r ./dist/files/* "${{pkgdir}}/"
    mkdir -p "$pkgdir"/usr/share/licenses/$pkgname
    mv "$pkgdir"/usr/share/doc/opentabletdriver/LICENSE "$pkgdir"/usr/share/licenses/$pkgname/LICENSE
    rmdir -p --ignore-fail-on-non-empty "$pkgdir"/usr/share/doc/opentabletdriver
}}
"""

notes_install_content = """
post_install() {
    echo ":: OpenTabletDriver installed successfully."
}
"""

build_folder = os.path.expanduser("~/otd_build")
os.makedirs(build_folder, exist_ok=True)
os.chdir(build_folder)

with open("PKGBUILD", "w") as f:
    f.write(pkgbuild_content.strip())

with open("notes.install", "w") as f:
    f.write(notes_install_content.strip())

print(f"Step 2: Compiling OpenTabletDriver {latest_version} via makepkg...")
try:
    subprocess.run(["makepkg", "-si"], check=True)
except subprocess.CalledProcessError:
    print("Error: makepkg failed. Aborting.")
    sys.exit(1)

print("Step 3: Updating drivers and starting service...")
subprocess.run(["sudo", "mkinitcpio", "-P"])
subprocess.run(["sudo", "rmmod", "wacom"], check=False)
subprocess.run(["sudo", "rmmod", "hid_uclogic"], check=False)
subprocess.run(["systemctl", "--user", "enable", "--now", "opentabletdriver"])

print("\nDone! Installed directly from official Git repository.")
