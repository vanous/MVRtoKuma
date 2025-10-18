# Uptime Kuma MVR

A tool to quickly create monitors in [Uptime Kuma](https://uptime.kuma.pet/),
from fixtures defined in a [MVR](https://gdtf-share.com/) (My Virtual Rig)
scene file.

<img  src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/images/uk_mvr_00.png">

## Features

- Uses  [pymvr](https://pypi.org/project/pymvr/) to read fixtures from MVR
  files
- Uses [Uptime Kuma](https://uptime.kuma.pet/)
  [API](https://github.com/lucasheld/uptime-kuma-api)
- Provides Graphical [Terminal User Interface](https://textual.textualize.io/)
- Creates tags from scene Layers and from fixture Classes and Positions
- Creates monitors, marked with the above mentioned tags, allowing grouping in
  Uptime Kuma
- Provides an MVR Merging tool, allowing to merge IP address from one MVR file
  (created by some network scanning tool) with another scene file - typically
  the main planning file. The fixture matching is based on fixture UUIDs or on
  DMX Universe + Address
- Bulk delete of monitors and tags - all, or only those matching from an MVR
  import

## FAQ

### What is this

A tool to quickly create monitors in Uptime Kuma, based on fixtures defined in MVR scene file.

### What this is not

This is not a tool to create MVR files. It also is not a general MVR file merger.

### What is MVR?

The My Virtual Rig file format is an open standard which allows programs to
share data and geometry of a scene for the entertainment industry. A scene is a
set of parametric objects such as fixtures, trusses, video screens, and other
objects that are used in the entertainment industry. See documentation and
further details on [GDTF Hub](https://gdtf.eu/).

## Quick Start

- Start the software, configure settings for Uptime Kuma server
- Use the `Get Server Data` to get data from Uptime Kuma
- Use `MVR Files - Import MVR`to import and MVR with fixtures. Make sure the
  MVR contains data for IPv4 addresses
- Use `Add Monitors` to create monitors in Uptime Kuma

## Features

- ### Settings
    - Set IP address, username and password for access to Uptime Kuma server
    - Choose to (not) display IDs of objects in MVR/Uptime Kuma
- ### Import MVR
    - Loads fixtures from MVR file
    - Reads IPv4 addresses of these fixtures
    - Reads layer, class and position names
- ### Merge MVR
    - Takes fixtures and IPv4 data from one MVR file
    - Adds the IPv4 data into matching fixtures in another MVR file
    - Fixture matching is based either on fixtures UUIDs or on DMX Universe + Addresses
- ### Clean MVR data
    - Cleans the MVR imported data in the currently running program
- ### Create Monitors
    - Creates monitors in Uptime Kuma
    - Allows to select which MVR features will be used for tags:
        - Layers
        - Classes
        - Positions
- ### Delete
    - Allows to delete in the Uptime Kuma:
        - All monitors
        - All tags
        - Monitors matching those from imported MVR
        - Tags matching those from imported MVR

## Instalation

Binary release is currently available for Linux, download it from the
[releases](https://github.com/vanous/uptime-kuma-mvr/releases). For other
operating systems use the instructions below.

## Requirements

Install `uv` on your system. `uv` will manage python and dependencies
installation and will also run the application.

- [uv](https://docs.astral.sh/uv/)

## Installation

Clone the [repository](https://github.com/vanous/uptime-kuma-mvr/) or [download
it](https://github.com/vanous/uptime-kuma-mvr/archive/refs/heads/master.zip) and uzip.

## Run the application

Inside the downloaded/unzipped repository, run:

```bash
uv run run.py
```

## Screenshots

<img  src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/images/uk_mvr_01.png">

<img  src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/images/uk_mvr_02.png">

<img  src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/images/uk_mvr_03.png">

<img  src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/images/uk_mvr_05.png">

<img  src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/images/uk_mvr_06.png">

<img  src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/images/uk_mvr_04.png">

## Development

```
uv run textual console
```

```
uv run textual run --dev run.py
```

## Bugs

### Testing git-bugs

- Issues are handled via https://github.com/git-bug/git-bug
- For pushing/pulling of bugs, either ssh based cloning must be used, or these [aliases](https://github.com/git-bug/git-bug/discussions/1332) can be used:

```
[alias]
	bugs = bug bug
	bug-users = bug user user
	open-bug = bug bug new
	push-bugs = "! fn(){ remote=origin; echo \"fetching bugs from '$remote' remote...\" >&2; git push  \"$remote\" --prune refs/bugs/* refs/identities/*; }; fn"
	pull-bugs = "! fn(){ remote=origin; echo \"fetching bugs from '$remote' remote...\" >&2; git fetch \"$remote\" \"refs/bugs/*:refs/bugs/*\" \"refs/identities/*:refs/identities/*\" && { [ ! -d .git/git-bug/cache/ ] || rm -r .git/git-bug/cache/; }; }; fn"
```
- I have no idea yet how to enable collaborators to pull/push bugs, probably by adding write access to the repo...?
- Try to use this and report any issues :)
- Maybe a branch with bugs via PR?

### Upside

- GitHub independent
- Local TUI and WEBUI

### Downside

- No notification about new issues/comments

## Packaging

Initial pyinstaller setup

```
uv run pyinstaller --onefile --add-data "tui/*.css:tui" run.py
```

## Running on Android in Termux

With a small amount of effort, it is possible:

- Install Termux
- Install uv, python, wget:

```sh
pkg install uv python3 wget
```

- Download and unzip uptime-kuma-mvr:

```sh
wget https://github.com/vanous/uptime-kuma-mvr/archive/refs/heads/master.zip
unzip master.zip
cd uptime-kume-mvr-master
```

- You will need to edit the pyproject.toml and change python to 3.11, then you
  can run it:

  ```sh
  uv run run.py
  ```

<img src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/images/ui_mvr_android.jpg" height=400px>

## Running Uptime Kuma with Podman

```sh
/usr/bin/podman run \
 --replace \
 --restart=always \
 --detach \
 --publish 3001:3001/tcp \
 --volume /full path to the directory/data:/app/data:Z \
 --name uptime-kuma \
 docker.io/louislam/uptime-kuma:1
```
```bibtex
@software{pymvr2025,
  title        = {pyMVR: Python Library for My Virtual Rig},
  author       = {{OpenStage}},
  year         = {2025},
  version      = {1.0.3},
  url          = {https://github.com/open-stage/python-mvr}
}
```
