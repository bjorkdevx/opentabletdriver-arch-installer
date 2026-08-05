# OpenTabletDriver Arch Installer

An automated Python script designed to build and install [OpenTabletDriver](https://opentabletdriver.net/) on Arch Linux directly from the latest GitHub release.

## Features

* **Automated Version Fetching**: Queries the GitHub API via `gh` CLI to always install the latest release.
* **PKGBUILD Generation**: Builds the package locally using standard Arch tools (`makepkg`).
* **Module Conflict Resolution**: Automatically unloads conflicting kernel drivers (`wacom`, `hid_uclogic`) and updates `initramfs`.
* **Systemd Integration**: Enables and starts the `opentabletdriver` daemon for your user account automatically.

## Prerequisites

Ensure you have git, base-devel (for building packages), and github-cli, dotnet-sdk dotnet-runtime installed:


sudo pacman -S --needed base-devel git github-cli python dotnet-sdk dotnet-runtime 

Quick Start

    Clone the repository:
    
    git clone https://github.com/bjorkdevx/opentabletdriver-arch-installer.git
    cd opentabletdriver-arch-installer

    Run the installer:

    python3 main.py

Post-Installation (Tablet Configurations)

If you have a custom layout file (such as Kamvas 22.json), copy it to the OpenTabletDriver configuration directory after running the script:

mkdir -p ~/.config/OpenTabletDriver/Configurations/
cp "Kamvas 22.json" ~/.config/OpenTabletDriver/Configurations/

Restart the OpenTabletDriver service to apply your configuration:
Bash

systemctl --user restart opentabletdriver
