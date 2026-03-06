# Building Modular BSP using Repo Tool

This guide describes how to build Advantech modular BSP using the `repo` tool and the [imx-manifest](https://github.com/Advantech-EECC/imx-manifest) repository. This method provides an alternative to the KAS-based workflow for assembling Yocto-based Board Support Packages.

## Table of Contents

- [1. Overview](#1-overview)
- [2. Prerequisites](#2-prerequisites)
  - [2.1 Install Repo Tool](#21-install-repo-tool)
  - [2.2 Install Essential Host Packages](#22-install-essential-host-packages)
- [3. Download Yocto Project BSP](#3-download-yocto-project-bsp)
  - [3.1 Available Releases](#31-available-releases)
  - [3.2 Download Process](#32-download-process)
  - [3.3 Supported Branches](#33-supported-branches)
- [4. Setup Build Environment](#4-setup-build-environment)
  - [4.1 Enabling Advantech BSP Layer](#41-enabling-advantech-bsp-layer)
- [5. Build Images](#5-build-images)
  - [5.1 Available Image Recipes](#51-available-image-recipes)
- [6. Supported Boards](#6-supported-boards)
  - [6.1 Board Compatibility Matrix](#61-board-compatibility-matrix)
  - [6.2 i.MX 8ULP Boards](#62-imx-8ulp-boards)
  - [6.3 i.MX 93 Boards](#63-imx-93-boards)
  - [6.4 i.MX 8M Boards](#64-imx-8m-boards)
  - [6.5 i.MX 8M Mini Boards](#65-imx-8m-mini-boards)
  - [6.6 i.MX 8M Plus Boards](#66-imx-8m-plus-boards)
  - [6.7 i.MX 95 Boards](#67-imx-95-boards)
- [7. Comparison with KAS-based Workflow](#7-comparison-with-kas-based-workflow)
  - [7.1 Repo Tool Workflow (This Guide)](#71-repo-tool-workflow-this-guide)
  - [7.2 KAS-based Workflow](#72-kas-based-workflow)
- [8. Additional Resources](#8-additional-resources)
  - [8.1 Official Documentation](#81-official-documentation)
  - [8.2 Advantech Resources](#82-advantech-resources)
  - [8.3 Google Repo Tool](#83-google-repo-tool)
  - [8.4 NXP i.MX Resources](#84-nxp-imx-resources)
- [9. Troubleshooting](#9-troubleshooting)
  - [9.1 Common Issues](#91-common-issues)
  - [9.2 Getting Help](#92-getting-help)
- [10. Contributing](#10-contributing)

## 1. Overview

The `repo` tool is a repository management tool built on top of Git by Google. It allows you to manage multiple Git repositories as a single workspace. The Advantech modular BSP uses repo manifests to define and synchronize all the required Yocto layers and metadata for building embedded Linux images.

**Key Benefits:**
- Standard Yocto workflow using `bitbake` directly
- Compatible with NXP i.MX BSP releases
- Flexible layer management
- Easy synchronization of multiple repositories

## 2. Prerequisites

### 2.1 Install Repo Tool

The `repo` utility must be installed first before you can download the BSP sources.

```bash
# Create a directory for repo tool
mkdir -p ~/bin

# Download the repo tool
curl http://commondatastorage.googleapis.com/git-repo-downloads/repo > ~/bin/repo

# Make it executable
chmod a+x ~/bin/repo

# Add to your PATH
export PATH=${PATH}:~/bin

# Optionally, add to your shell profile for persistence
echo 'export PATH=${PATH}:~/bin' >> ~/.bashrc
```

**Verify Installation:**
```bash
repo version
```

### 2.2 Install Essential Host Packages

Your build host must have required packages for Yocto builds. The specific packages depend on your Linux distribution.

**For Ubuntu 22.04 / Ubuntu 24.04:**

```bash
sudo apt-get update
sudo apt-get install -y \
    gawk wget git diffstat unzip texinfo gcc build-essential \
    chrpath socat cpio python3 python3-pip python3-pexpect \
    xz-utils debianutils iputils-ping python3-git python3-jinja2 \
    libegl1-mesa libsdl1.2-dev python3-subunit mesa-common-dev \
    zstd liblz4-tool file locales libacl1
```

**Reference:**
For detailed host package requirements, refer to the [Yocto Project Quick Build Guide](https://docs.yoctoproject.org/5.2.4/brief-yoctoprojectqs/index.html#build-host-packages).

## 3. Download Yocto Project BSP

### 3.1 Available Releases

The Advantech i.MX manifest repository provides BSP releases for multiple Yocto versions. Each `-adv` manifest file adds the [`meta-modular-bsp-nxp`](https://github.com/Advantech-EECC/meta-modular-bsp-nxp) Advantech BSP layer on top of the base NXP release.

| Yocto Release | Yocto Version | Kernel Version | imx-manifest Branch | Manifest File |
|---------------|---------------|----------------|---------------------|---------------|
| Walnascar | 5.2 (latest) | Linux 6.12.49 | imx-linux-walnascar-adv | imx-6.12.49-2.2.0-adv-r2.xml |
| Walnascar | 5.2 | Linux 6.12.49 | imx-linux-walnascar-adv | imx-6.12.49-2.2.0-adv.xml |
| Walnascar | 5.2 | Linux 6.12.34 | imx-linux-walnascar-adv | imx-6.12.34-2.1.0-adv.xml |
| Walnascar | 5.2 | Linux 6.12.20 | imx-linux-walnascar-adv | imx-6.12.20-2.0.0-adv.xml |
| Styhead | 5.1 | Linux 6.12.3 | imx-linux-styhead-adv | imx-6.12.3-1.0.0-adv.xml |
| Scarthgap | 5.0 | Linux 6.6.52 | imx-linux-scarthgap-adv | imx-6.6.52-2.2.0-adv-r2.xml |
| Scarthgap | 5.0 | Linux 6.6.52 | imx-linux-scarthgap-adv | imx-6.6.52-2.2.0-adv.xml |
| Scarthgap | 5.0 | Linux 6.6.36 | imx-linux-scarthgap-adv | imx-6.6.36-2.1.0-adv.xml |
| Scarthgap | 5.0 | Linux 6.6.23 | imx-linux-scarthgap-adv | imx-6.6.23-2.0.0-adv.xml |
| Nanbield | 4.3 | Linux 6.6.3 | imx-linux-nanbield-adv | imx-6.6.3-1.0.0-adv.xml |

> **Note:** Manifest files with the `-r2` suffix (e.g. `imx-6.12.49-2.2.0-adv-r2.xml`) are revision 2 releases of the same NXP BSP version, using a newer commit of the `meta-modular-bsp-nxp` layer.

### 3.2 Download Process

Create a workspace directory and initialize the repo:

```bash
# Create a workspace directory
mkdir -p ~/imx-yocto-bsp
cd ~/imx-yocto-bsp

# Initialize repo with a specific release manifest
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-walnascar-adv -m imx-6.12.49-2.2.0-adv-r2.xml

# Download all the source repositories
repo sync
```

**Examples for Walnascar (Yocto 5.2) Releases:**

```bash
# For 6.12.49-2.2.0 release (latest revision)
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-walnascar-adv -m imx-6.12.49-2.2.0-adv-r2.xml
repo sync

# For 6.12.49-2.2.0 release
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-walnascar-adv -m imx-6.12.49-2.2.0-adv.xml
repo sync

# For 6.12.34-2.1.0 release
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-walnascar-adv -m imx-6.12.34-2.1.0-adv.xml
repo sync

# For 6.12.20-2.0.0 release
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-walnascar-adv -m imx-6.12.20-2.0.0-adv.xml
repo sync
```

**Examples for Styhead (Yocto 5.1) Releases:**

```bash
# For 6.12.3-1.0.0 release
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-styhead-adv -m imx-6.12.3-1.0.0-adv.xml
repo sync
```

**Examples for Scarthgap (Yocto 5.0) Releases:**

```bash
# For 6.6.52-2.2.0 release (latest revision)
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-scarthgap-adv -m imx-6.6.52-2.2.0-adv-r2.xml
repo sync

# For 6.6.52-2.2.0 release
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-scarthgap-adv -m imx-6.6.52-2.2.0-adv.xml
repo sync

# For 6.6.36-2.1.0 release
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-scarthgap-adv -m imx-6.6.36-2.1.0-adv.xml
repo sync

# For 6.6.23-2.0.0 release
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-scarthgap-adv -m imx-6.6.23-2.0.0-adv.xml
repo sync
```

**Examples for Nanbield (Yocto 4.3) Releases:**

```bash
# For 6.6.3-1.0.0 release
repo init -u https://github.com/Advantech-EECC/imx-manifest -b imx-linux-nanbield-adv -m imx-6.6.3-1.0.0-adv.xml
repo sync
```

### 3.3 Supported Branches

**imx-manifest Advantech branches** (use with `-u https://github.com/Advantech-EECC/imx-manifest`):

| Branch | Yocto Release | Yocto Version |
|--------|---------------|---------------|
| `imx-linux-walnascar-adv` | Walnascar | 5.2 (Latest) |
| `imx-linux-styhead-adv` | Styhead | 5.1 |
| `imx-linux-scarthgap-adv` | Scarthgap | 5.0 |
| `imx-linux-nanbield-adv` | Nanbield | 4.3 |

**meta-modular-bsp-nxp branches** (Advantech BSP layer, automatically fetched by the manifests above):

| Branch | Yocto Release | Yocto Version |
|--------|---------------|---------------|
| `walnascar` | Walnascar | 5.2 (Latest) |
| `styhead` | Styhead | 5.1 |
| `scarthgap` | Scarthgap | 5.0 |
| `nanbield` | Nanbield | 4.3 |

## 4. Setup Build Environment

After downloading the sources, you need to set up the build environment. The `imx-setup-release.sh` script initializes the build configuration.

**Basic Syntax:**
```bash
MACHINE=<machine> DISTRO=fsl-imx-<backend> source ./imx-setup-release.sh -b bld-<backend>
```

**Parameters:**
- `<machine>` - Target board/machine name (defaults to `imx6qsabresd`)
- `<backend>` - Graphics backend type:
  - `xwayland` - Wayland with X11 support (default, recommended)
  - `wayland` - Pure Wayland
  - `fb` - Framebuffer (not supported for i.MX8)

**Examples for Advantech Boards:**

```bash
# For RSB-3720 (6G) board with XWayland
MACHINE=rsb3720 DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland

# For RSB-3720 (4G) board with XWayland (Walnascar only)
MACHINE=rsb3720-4g DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland

# For ROM-2620-ED91 board with XWayland
MACHINE=rom2620-ed91 DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland

# For ROM-2820-ED93 board with XWayland
MACHINE=rom2820-ed93 DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland

# For ROM-5720-DB5901 board with XWayland
MACHINE=rom5720-db5901 DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland

# For ROM-5721-DB5901 (2G) board with XWayland
MACHINE=rom5721-db5901 DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland

# For ROM-5721-DB5901 (1G) board with XWayland (Walnascar only)
MACHINE=rom5721-1g-db5901 DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland

# For ROM-5722-DB2510 board with XWayland
MACHINE=rom5722-db2510 DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland

# For AOM-5521-DB2510 board with XWayland (Walnascar only)
MACHINE=aom5521-db2510 DISTRO=fsl-imx-xwayland source ./imx-setup-release.sh -b bld-xwayland
```

This script will:
1. Create a build directory (`bld-xwayland`, `bld-wayland`, etc.)
2. Set up `conf/local.conf` and `conf/bblayers.conf`
3. Initialize the BitBake environment

### 4.1 Enabling Advantech BSP Layer

**IMPORTANT:** To access Advantech-specific machine configurations, you must enable the Advantech BSP layer.

After running the setup script, add the following line to the **end** of `conf/bblayers.conf`:

```bash
# Edit the bblayers.conf file
cd bld-xwayland  # or your build directory name
vi conf/bblayers.conf
```

Add this line at the end:
```
BBLAYERS += "${BSPDIR}/sources/meta-modular-bsp-nxp"
```

**Alternative (automatic method):**
```bash
# From your build directory
echo 'BBLAYERS += "${BSPDIR}/sources/meta-modular-bsp-nxp"' >> conf/bblayers.conf
```

**Verify the layer is enabled:**
```bash
bitbake-layers show-layers | grep meta-modular-bsp-nxp
```

## 5. Build Images

Once the environment is set up, you can build images using BitBake.

```bash
# Make sure you're in the build directory
cd bld-xwayland  # or your build directory

# Build an image
bitbake <image-recipe>
```

### 5.1 Available Image Recipes

| Image Recipe | Description |
|--------------|-------------|
| `imx-image-core` | Core image with basic graphics and no multimedia |
| `imx-image-multimedia` | Image with multimedia and graphics support |
| `imx-image-full` | Full-featured image with multimedia, machine learning, and Qt |

**Examples:**

```bash
# Build core image for RSB3720
bitbake imx-image-core

# Build multimedia image
bitbake imx-image-multimedia

# Build full-featured image with Qt and ML
bitbake imx-image-full
```

**Build Output Location:**

After a successful build, images will be located at:
```
tmp/deploy/images/<machine>/
```

For example, for RSB3720:
```
tmp/deploy/images/rsb3720/
```

## 6. Supported Boards

The following Advantech boards are supported in the modular BSP. Support availability depends on the Yocto release used.

### 6.1 Board Compatibility Matrix

| Board | Machine Name | NXP SoC | Nanbield (4.3) | Scarthgap (5.0) | Styhead (5.1) | Walnascar (5.2) |
|-------|-------------|---------|:--------------:|:---------------:|:-------------:|:---------------:|
| ROM-2620-ED91 | `rom2620-ed91` | i.MX 8ULP | ✅ | ✅ | ✅ | ✅ |
| ROM-2820-ED93 | `rom2820-ed93` | i.MX 93 | ❌ | ✅ | ✅ | ✅ |
| ROM-5720-DB5901 | `rom5720-db5901` | i.MX 8M | ❌ | ✅ (preliminary) | ✅ (preliminary) | ✅ (preliminary) |
| ROM-5721-DB5901 (1G) | `rom5721-1g-db5901` | i.MX 8M Mini | ❌ | ❌ | ❌ | ✅ (preliminary) |
| ROM-5721-DB5901 (2G) | `rom5721-db5901` / `rom5721-2g-db5901` | i.MX 8M Mini | ❌ | ✅ (preliminary) | ✅ (preliminary) | ✅ (preliminary) |
| ROM-5722-DB2510 | `rom5722-db2510` | i.MX 8M Plus | ❌ | ✅ | ✅ | ✅ |
| RSB-3720 (6G) | `rsb3720` / `rsb3720-6g` | i.MX 8M Plus | ❌ | ✅ | ✅ | ✅ |
| RSB-3720 (4G) | `rsb3720-4g` | i.MX 8M Plus | ❌ | ❌ | ❌ | ✅ |
| AOM-5521-DB2510 | `aom5521-db2510` | i.MX 95 | ❌ | ❌ | ❌ | ✅ (preliminary) |

### 6.2 i.MX 8ULP Boards
- **ROM-2620-ED91** - Embedded module with i.MX 8ULP SoC (`rom2620-ed91`)

### 6.3 i.MX 93 Boards
- **ROM-2820-ED93** - Embedded module with i.MX 93 SoC (`rom2820-ed93`)

### 6.4 i.MX 8M Boards
- **ROM-5720-DB5901** - Embedded module with i.MX 8M SoC (`rom5720-db5901`) — preliminary support

### 6.5 i.MX 8M Mini Boards
- **ROM-5721-DB5901 (1G)** - Embedded module with i.MX 8M Mini, 1GB RAM (`rom5721-1g-db5901`) — Walnascar only, preliminary support
- **ROM-5721-DB5901 (2G)** - Embedded module with i.MX 8M Mini, 2GB RAM (`rom5721-db5901` / `rom5721-2g-db5901`) — preliminary support

### 6.6 i.MX 8M Plus Boards
- **ROM-5722-DB2510** - Embedded module with i.MX 8M Plus SoC (`rom5722-db2510`)
- **RSB-3720 (6G)** - Industrial SBC with i.MX 8M Plus, 6GB RAM (`rsb3720` / `rsb3720-6g`)
- **RSB-3720 (4G)** - Industrial SBC with i.MX 8M Plus, 4GB RAM (`rsb3720-4g`) — Walnascar only

### 6.7 i.MX 95 Boards
- **AOM-5521-DB2510** - Module with i.MX 95 SoC (`aom5521-db2510`) — Walnascar only, preliminary support

## 7. Comparison with KAS-based Workflow

This repository supports two build workflows:

### 7.1 Repo Tool Workflow (This Guide)
- **Pros:**
  - Standard Yocto workflow using BitBake directly
  - Compatible with NXP reference documentation
  - Familiar to Yocto developers
  - Fine-grained control over layers and configurations
  
- **Cons:**
  - Manual layer management
  - More setup steps required
  - Less container integration

### 7.2 KAS-based Workflow
(See [README.md](README.md))

- **Pros:**
  - Simplified configuration using YAML files
  - Integrated Docker container support
  - Automated layer management
  - Reproducible builds with locked configurations
  - Pre-configured board and feature combinations
  
- **Cons:**
  - Requires KAS tool installation
  - Different workflow from standard Yocto

**Recommendation:**
- Use **Repo Tool** if you're familiar with standard Yocto workflows or need to follow NXP reference documentation
- Use **KAS** if you want automated, reproducible builds with minimal configuration

## 8. Additional Resources

### 8.1 Official Documentation
- [Yocto Project Documentation](https://docs.yoctoproject.org/)
- [Yocto Project Quick Build Guide](https://docs.yoctoproject.org/5.2.4/brief-yoctoprojectqs/index.html)
- [BitBake User Manual](https://docs.yoctoproject.org/bitbake/)

### 8.2 Advantech Resources
- [imx-manifest Repository](https://github.com/Advantech-EECC/imx-manifest)
- [meta-modular-bsp-nxp Layer](https://github.com/Advantech-EECC/meta-modular-bsp-nxp)

### 8.3 Google Repo Tool
- [Repo Command Reference](https://source.android.com/docs/setup/reference/repo)
- [Repo Tool Overview](https://gerrit.googlesource.com/git-repo/)

### 8.4 NXP i.MX Resources
- [NXP i.MX Software](https://www.nxp.com/design/software/embedded-software/i-mx-software:IMX-SW)
- [NXP Community](https://community.nxp.com/)

## 9. Troubleshooting

### 9.1 Common Issues

**2. BitBake cannot find Advantech machines:**
```bash
# Verify meta-modular-bsp-nxp is in bblayers.conf
grep meta-modular-bsp-nxp conf/bblayers.conf

# Add if missing
echo 'BBLAYERS += "${BSPDIR}/sources/meta-modular-bsp-nxp"' >> conf/bblayers.conf
```
