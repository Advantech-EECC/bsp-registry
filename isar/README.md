# Isar Build System Configuration

This directory contains the Isar (Integration System for Automated Root filesystem generation) build system configuration for the Advantech BSP registry. Isar is a build framework designed specifically for creating Debian-based embedded Linux systems using native Debian packaging tools.

## Table of Contents

- [Isar Build System Configuration](#isar-build-system-configuration)
  - [Table of Contents](#table-of-contents)
  - [1. Overview](#1-overview)
  - [2. What is Isar?](#2-what-is-isar)
  - [3. Directory Structure](#3-directory-structure)
    - [3.1 File Descriptions](#31-file-descriptions)
  - [4. Image Generation Process](#4-image-generation-process)
    - [4.1 High-Level Build Flow](#41-high-level-build-flow)
    - [4.2 Detailed BitBake Task Flow](#42-detailed-bitbake-task-flow)
    - [4.3 Layer Architecture](#43-layer-architecture)
    - [4.4 Comparison: Isar vs Yocto Build Process](#44-comparison-isar-vs-yocto-build-process)
  - [5. Supported Distributions](#5-supported-distributions)
    - [5.1 Debian Distributions](#51-debian-distributions)
    - [5.2 Ubuntu Distributions](#52-ubuntu-distributions)
  - [6. Supported Architectures](#6-supported-architectures)
    - [6.1 Real Hardware Support](#61-real-hardware-support)
  - [7. Configuration Files](#7-configuration-files)
    - [7.1 isar.yaml - Core Configuration](#71-isaryaml---core-configuration)
    - [7.2 Distribution Configuration Example](#72-distribution-configuration-example)
    - [7.3 Machine Configuration Example](#73-machine-configuration-example)
  - [8. Host System Configuration](#8-host-system-configuration)
    - [8.1 Operating System Requirements](#81-operating-system-requirements)
    - [8.2 Essential Tools](#82-essential-tools)
      - [8.2.1 Docker](#821-docker)
      - [8.2.2 Python Environment](#822-python-environment)
      - [8.2.3 Cross-Compilation Support (qemu-user-static)](#823-cross-compilation-support-qemu-user-static)
    - [8.3 Disk Space and Resources](#83-disk-space-and-resources)
  - [9. Building Isar Images](#9-building-isar-images)
    - [9.1 Prerequisites](#91-prerequisites)
    - [9.2 Using BSP Registry Manager](#92-using-bsp-registry-manager)
    - [9.3 Interactive Shell Access](#93-interactive-shell-access)
    - [9.4 Manual Build with KAS](#94-manual-build-with-kas)
    - [9.5 Build Configuration Composition](#95-build-configuration-composition)
    - [9.6 Running Images in QEMU](#96-running-images-in-qemu)
  - [10. Build System Architecture](#10-build-system-architecture)
    - [10.1 Container-Based Build Environment](#101-container-based-build-environment)
    - [10.2 Why Privileged Mode?](#102-why-privileged-mode)
  - [11. Key Features](#11-key-features)
    - [11.1 Native Debian Packaging](#111-native-debian-packaging)
    - [11.2 Cross-Compilation Support](#112-cross-compilation-support)
    - [11.3 Reproducible Builds](#113-reproducible-builds)
    - [11.4 Modular Configuration](#114-modular-configuration)
  - [12. Advantages Over Traditional Build Systems](#12-advantages-over-traditional-build-systems)
  - [13. Advanced Topics](#13-advanced-topics)
    - [13.1 Custom Package Development](#131-custom-package-development)
    - [13.2 Adding Custom Layers](#132-adding-custom-layers)
    - [13.3 Build Caching](#133-build-caching)
    - [13.4 Multiconfig Builds](#134-multiconfig-builds)
  - [14. Resources](#14-resources)
    - [14.1 Official Documentation](#141-official-documentation)
    - [14.2 Debian Resources](#142-debian-resources)
    - [14.3 Advantech-Specific Resources](#143-advantech-specific-resources)
    - [14.4 KAS Tool](#144-kas-tool)
    - [14.5 Community and Support](#145-community-and-support)
    - [14.6 Presentations and Articles](#146-presentations-and-articles)
  - [15. Getting Help](#15-getting-help)

---

## 1. Overview

The Isar directory provides a modular, reusable configuration structure for building Debian-based embedded Linux images. Unlike Yocto/OpenEmbedded which builds packages from source, Isar leverages Debian's existing binary package ecosystem while providing the customization and reproducibility features needed for embedded systems.

**Key characteristics:**
- Uses BitBake recipes similar to Yocto
- Leverages Debian's apt/dpkg package management
- Supports cross-compilation for multiple architectures
- Provides reproducible, container-based builds
- Faster build times by using pre-built Debian packages

---

## 2. What is Isar?

**Isar** stands for **Integration System for Automated Root filesystem generation**. It is a build framework developed by Siemens and ilbers GmbH that combines the best of both worlds:

1. **Debian ecosystem advantages:**
   - Extensive, tested binary package repository
   - Long-term support and security updates
   - Clear licensing and compliance
   - Familiar tools (apt, dpkg, deb packages)

2. **Embedded build system features:**
   - Reproducible builds
   - Layered architecture for customization
   - Cross-compilation support
   - Full image generation (bootloader, kernel, rootfs)
   - BitBake-based dependency tracking

**Use Cases:**
- Industrial embedded systems
- Automotive and telecommunications
- IoT devices requiring Debian stability
- Projects needing faster build times than full source builds
- Systems requiring long-term Debian support

---

## 3. Directory Structure

```
isar/
├── README.md              # This file
├── isar.yaml             # Core Isar build system configuration
├── distro/               # Distribution configurations
│   ├── debian-bookworm.yaml
│   ├── debian-bullseye.yaml
│   ├── debian-buster.yaml
│   ├── debian-sid.yaml
│   ├── debian-trixie.yaml
│   ├── ubuntu-focal.yaml
│   ├── ubuntu-jammy.yaml
│   └── ubuntu-noble.yaml
└── qemu/                 # QEMU machine configurations
    ├── qemuarm.yaml      # ARM 32-bit
    ├── qemuarm64.yaml    # ARM 64-bit
    ├── qemux86.yaml      # x86 32-bit
    └── qemux86-64.yaml   # x86 64-bit
```

### 3.1 File Descriptions

| File/Directory | Purpose |
|----------------|---------|
| `isar.yaml` | Core Isar configuration defining the build system, repository URLs, and layers |
| `distro/` | Contains distribution-specific configurations for Debian variants and Ubuntu |
| `qemu/` | Machine definitions for QEMU virtual platforms (testing and development) |

---

## 4. Image Generation Process

The following ASCII diagrams illustrate the Isar image generation workflow:

### 4.1 High-Level Build Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Initiates Build                        │
│              (python bsp.py build <isar-config>.yaml)               │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     KAS Configuration Loading                       │
│  • Reads YAML configuration (distro + machine + isar.yaml)          │
│  • Resolves includes and dependencies                               │
│  • Sets up build environment variables                              │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Docker Container Setup                          │
│  • Launches privileged kas-isar container                           │
│  • Mounts source directories and build paths                        │
│  • Configures Debian base distribution                              │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Repository Checkout                             │
│  • Clones Isar framework (github.com/ilbers/isar)                   │
│  • Checks out specified version (v0.11)                             │
│  • Sets up meta-layers (meta, meta-isar, meta-test)                 │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     BitBake Initialization                          │
│  • Parses bblayers.conf and local.conf                              │
│  • Loads machine configuration                                      │
│  • Loads distribution configuration                                 │
│  • Initializes task dependency graph                                │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Package Resolution Phase                        │
│  • Reads image recipe (e.g., isar-image-base)                       │
│  • Resolves Debian package dependencies                             │
│  • Downloads .deb packages from Debian repositories                 │
│  • Verifies package signatures and checksums                        │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Cross-Compilation Setup                         │
│  • Installs cross-toolchain packages (if needed)                    │
│  • Configures dpkg for target architecture                          │
│  • Sets up sbuild/schroot environment                               │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Root Filesystem Assembly                        │
│  • Creates base Debian rootfs using debootstrap/multistrap          │
│  • Installs packages via apt/dpkg                                   │
│  • Applies customizations from recipes                              │
│  • Configures system services and startup                           │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Kernel and Bootloader                           │
│  • Installs kernel package (linux-image-*)                          │
│  • Installs bootloader (u-boot/grub)                                │
│  • Generates device tree blobs (if needed)                          │
│  • Configures boot parameters                                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Image Finalization                              │
│  • Creates filesystem images (ext4, wic, etc.)                      │
│  • Generates partition layouts                                      │
│  • Creates bootable disk images                                     │
│  • Compresses and checksums final artifacts                         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Build Artifacts Output                          │
│  Output: build/<bsp-name>/tmp/deploy/images/<machine>/              │
│   • .wic.img    - Flashable disk image                              │
│   • .ext4       - Root filesystem image                             │
│   • vmlinuz     - Kernel image                                      │
│   • .dtb        - Device tree blobs                                 │
│   • .manifest   - Package list and versions                         │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Detailed BitBake Task Flow

```
┌────────────────────────────────────────────────────────────────────┐
│                    BitBake Task Execution Flow                     │
└────────────────────────────────────────────────────────────────────┘

  Recipe: isar-image-base
     │
     ├─► do_fetch
     │      │
     │      └─► Download Debian packages from repos
     │
     ├─► do_unpack
     │      │
     │      └─► Extract package metadata
     │
     ├─► do_apt_config_prepare
     │      │
     │      └─► Configure apt sources for target architecture
     │
     ├─► do_bootstrap
     │      │
     │      └─► Create minimal Debian base system (debootstrap)
     │            ┌────────────────────────────────────┐
     │            │  • Install essential packages      │
     │            │  • Configure dpkg for target arch  │
     │            │  • Set up base filesystem layout   │
     │            └────────────────────────────────────┘
     │
     ├─► do_install_packages
     │      │
     │      └─► Install additional packages via apt-get
     │            ┌────────────────────────────────────┐
     │            │  • Resolve dependencies            │
     │            │  • Download .deb files             │
     │            │  • Install with dpkg               │
     │            │  • Run post-install scripts        │
     │            └────────────────────────────────────┘
     │
     ├─► do_rootfs_postprocess
     │      │
     │      └─► Apply customizations
     │            ┌────────────────────────────────────┐
     │            │  • Copy overlay files              │
     │            │  • Modify configuration files      │
     │            │  • Set permissions and ownership   │
     │            │  • Enable/disable services         │
     │            └────────────────────────────────────┘
     │
     ├─► do_image
     │      │
     │      └─► Create filesystem images
     │            ┌────────────────────────────────────┐
     │            │  • Generate ext4 image             │
     │            │  • Create partition table          │
     │            │  • Format partitions               │
     │            └────────────────────────────────────┘
     │
     └─► do_image_wic
            │
            └─► Generate bootable WIC image
                  ┌────────────────────────────────────┐
                  │  • Assemble bootloader partition   │
                  │  • Add root filesystem partition   │
                  │  • Create boot configuration       │
                  │  • Generate final .wic image       │
                  └────────────────────────────────────┘
```

### 4.3 Layer Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Isar Layer Stack                          │
└──────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────┐
   │        User Custom Layers (optional)            │
   │  • meta-isar-modular-bsp-nxp                    │
   │  • Custom machine and distro definitions        │
   │  • Application-specific recipes                 │
   └──────────────────┬──────────────────────────────┘
                      │
   ┌──────────────────▼──────────────────────────────┐
   │           meta-test (optional)                  │
   │  • Test images and recipes                      │
   │  • Validation and QA tools                      │
   └──────────────────┬──────────────────────────────┘
                      │
   ┌──────────────────▼──────────────────────────────┐
   │             meta-isar                           │
   │  • Core image recipes (isar-image-base, etc.)   │
   │  • Package groups                               │
   │  • System configuration                         │
   │  • Distribution policies                        │
   └──────────────────┬──────────────────────────────┘
                      │
   ┌──────────────────▼──────────────────────────────┐
   │               meta                              │
   │  • BitBake classes and functions                │
   │  • Core Isar build system logic                 │
   │  • Cross-compilation framework                  │
   │  • Debian package integration                   │
   │  • Image generation infrastructure              │
   └──────────────────┬──────────────────────────────┘
                      │
   ┌──────────────────▼──────────────────────────────┐
   │          Debian Base System                     │
   │  • Debian package repositories                  │
   │  • Binary .deb packages                         │
   │  • apt/dpkg infrastructure                      │
   └─────────────────────────────────────────────────┘
```

### 4.4 Comparison: Isar vs Yocto Build Process

```
┌─────────────────────────────────────────────────────────────────┐
│                  Yocto Build Process                            │
└─────────────────────────────────────────────────────────────────┘

Source Code → Compile → Package → Assemble → Image
   (Days)      (Hours)   (Minutes)  (Minutes)  (Minutes)
      │
      └─► Every package built from source
          • Longer build times
          • Full control over compilation
          • Smaller final images possible
          • Requires powerful build servers

┌─────────────────────────────────────────────────────────────────┐
│                   Isar Build Process                            │
└─────────────────────────────────────────────────────────────────┘

Debian Packages → Assemble → Customize → Image
   (Seconds)       (Minutes)   (Minutes)   (Minutes)
      │
      └─► Uses pre-built Debian packages
          • Much faster builds
          • Debian-tested packages
          • Larger images (full packages)
          • Runs on modest hardware
```

---

## 5. Supported Distributions

The Isar configuration supports the following Debian-based distributions:

### 5.1 Debian Distributions

| Distribution | Version | Codename | Status | Configuration File |
|--------------|---------|----------|--------|-------------------|
| Debian 13 | Testing | Trixie | 🟢 Active | `distro/debian-trixie.yaml` |
| Debian 12 | Stable | Bookworm | 🟢 Stable | `distro/debian-bookworm.yaml` |
| Debian 11 | Old Stable | Bullseye | 🟡 Maintenance | `distro/debian-bullseye.yaml` |
| Debian 10 | Old Old Stable | Buster | 🟠 Legacy | `distro/debian-buster.yaml` |
| Debian Unstable | Rolling | Sid | 🔴 Experimental | `distro/debian-sid.yaml` |

### 5.2 Ubuntu Distributions

| Distribution | Codename | Status | Configuration File |
|--------------|----------|--------|-------------------|
| Ubuntu 24.04 LTS | Noble Numbat | 🟢 Active | `distro/ubuntu-noble.yaml` |
| Ubuntu 22.04 LTS | Jammy Jellyfish | 🟢 Stable | `distro/ubuntu-jammy.yaml` |
| Ubuntu 20.04 LTS | Focal Fossa | 🟡 Maintenance | `distro/ubuntu-focal.yaml` |

**Status Legend:**
- 🟢 **Active/Stable**: Recommended for new projects
- 🟡 **Maintenance**: Supported but not recommended for new projects
- 🟠 **Legacy**: Limited support, upgrade recommended
- 🔴 **Experimental**: Not for production use

---

## 6. Supported Architectures

Isar supports cross-compilation for multiple CPU architectures through QEMU machine definitions:

| Architecture | Machine | Debian Arch | Configuration | Use Case |
|--------------|---------|-------------|---------------|----------|
| **ARM 64-bit** | qemuarm64 | arm64/aarch64 | `qemu/qemuarm64.yaml` | Modern ARM devices, testing |
| **ARM 32-bit** | qemuarm | armhf | `qemu/qemuarm.yaml` | Legacy ARM devices |
| **x86 64-bit** | qemuamd64 | amd64 | `qemu/qemux86-64.yaml` | PC platforms, testing |
| **x86 32-bit** | qemui386 | i386 | `qemu/qemux86.yaml` | Legacy x86 systems |

### 6.1 Real Hardware Support

In addition to QEMU virtual machines, Isar supports real hardware platforms through custom BSP layers:

| Hardware | Architecture | Distribution | BSP Configuration |
|----------|--------------|--------------|-------------------|
| **Advantech RSB3720** | ARM64 (NXP i.MX8) | Debian Trixie | `adv-mbsp-isar-debian-rsb3720.yaml` |

*Additional hardware platforms can be added through meta-isar-modular-bsp layers.*

---

## 7. Configuration Files

### 7.1 isar.yaml - Core Configuration

```yaml
header:
  version: 14

build_system: isar

repos:
  isar:
    url: "https://github.com/ilbers/isar.git"
    tag: "v0.11"
    commit: "f8558fcf3ecf98e58853b82d89645bcedb24b853"
    path: "layers/isar"
    layers:
      meta:
      meta-isar:
      meta-test:

bblayers_conf_header:
  standard: |
    BBPATH = "${TOPDIR}"
    BBFILES ?= ""
```

**Key Components:**
- **build_system**: Specifies Isar instead of Yocto
- **repos**: Defines the Isar framework repository
  - Uses stable version v0.11
  - Pinned to specific commit for reproducibility
- **layers**: Enables meta, meta-isar, and meta-test layers
- **bblayers_conf_header**: BitBake layer configuration template

### 7.2 Distribution Configuration Example

```yaml
# distro/debian-trixie.yaml
header:
  version: 14

distro: debian-trixie
```

Simple distribution selector that sets the Debian version to use.

### 7.3 Machine Configuration Example

```yaml
# qemu/qemuarm64.yaml
header:
  version: 14

machine: qemuarm64

target:
  - isar-image-base
```

Defines the target machine and which image recipe to build.

---

## 8. Host System Configuration

To successfully build Isar images, your host system must meet specific requirements and be properly configured.

### 8.1 Operating System Requirements
A Linux-based operating system is required. Recommended distributions:
- **Ubuntu**: 20.04 LTS, 22.04 LTS, or newer
- **Debian**: 11 (Bullseye), 12 (Bookworm), or newer

### 8.2 Essential Tools

#### 8.2.1 Docker
Isar performs builds inside a privileged Docker container.
- Install Docker Engine: [Docker Installation Guide](https://docs.docker.com/engine/install/)
- **Important**: Your user must be in the `docker` group to run containers without sudo.
  ```bash
  sudo usermod -aG docker $USER
  # Log out and back in for changes to take effect
  newgrp docker
  ```

#### 8.2.2 Python Environment
To use the BSP Registry Manager (`bsp.py`), install the required Python packages:
```bash
pip3 install -r requirements.txt
```

#### 8.2.3 Cross-Compilation Support (qemu-user-static)
Isar uses QEMU user emulation for cross-compilation (e.g., building ARM64 on x86). Ensure your kernel supports `binfmt_misc` and install the static QEMU user helpers.

On Debian/Ubuntu:
```bash
sudo apt-get install qemu-user-static binfmt-support
```

### 8.3 Disk Space and Resources
Building embedded Linux images requires significant resources:
 - **Disk Space**: Recommended 100 GB+ free space. Isar caches downloads (`DL_DIR`) and build artifacts (`SSTATE_DIR`) which grow over time.
 - **RAM**: 8GB minimum, 16GB+ recommended.
 - **CPU**: Multi-core processor recommended for parallel task execution.

---

## 9. Building Isar Images

### 9.1 Prerequisites

1. **Docker** with privileged mode support
2. **Python 3.x** with required dependencies
3. **KAS tool** (handled automatically via container)

### 9.2 Using BSP Registry Manager

The recommended method is using the `bsp.py` script:

```bash
# Build RSB3720 with Debian Trixie
python bsp.py build adv-mbsp-isar-debian-rsb3720

# Build QEMU ARM64 with Debian Trixie
python bsp.py build isar-qemuarm64-debian-trixie

# Build QEMU ARM64 with Ubuntu Noble
python bsp.py build isar-qemuarm64-ubuntu-noble
```

### 9.3 Interactive Shell Access

Enter a build environment for debugging or development:

```bash
python bsp.py shell adv-mbsp-isar-debian-rsb3720
```

### 9.4 Manual Build with KAS

For advanced users, you can build directly with KAS:

```bash
# Create configuration by combining files
kas-container build \
  isar/isar.yaml:isar/distro/debian-trixie.yaml:isar/qemu/qemuarm64.yaml
```

### 9.5 Build Configuration Composition

Isar builds use a modular configuration approach:

```
Base Config     +    Distribution    +    Machine      =    Full Config
-----------          ------------         --------          ------------
isar.yaml            debian-trixie.yaml   qemuarm64.yaml    Complete build
                                                             definition
```

**Example compositions:**

```bash
# QEMU ARM64 + Debian Bookworm
isar/isar.yaml:isar/distro/debian-bookworm.yaml:isar/qemu/qemuarm64.yaml

# QEMU x86-64 + Ubuntu Noble
isar/isar.yaml:isar/distro/ubuntu-noble.yaml:isar/qemu/qemux86-64.yaml

# RSB3720 + Debian Trixie (includes hardware BSP layer)
isar/isar.yaml:isar/distro/debian-trixie.yaml:adv-mbsp-isar-debian-rsb3720.yaml
```

### 9.6 Running Images in QEMU

After a successful build, you can boot the produced image using the helper script:

- `isar/scripts/isar-runqemu.sh`

This script expects a deploy directory that contains the image artifacts (disk image, and optionally kernel+initrd).

**Common workflow:**

1. Build a QEMU machine configuration (example):

  ```bash
  python bsp.py build isar-qemuarm64-debian-trixie
  ```

2. Locate the deploy directory produced by the build (it must contain `*.wic`/`*.img`/`*.ext4`).

3. Start QEMU by pointing `--deploy` at that directory:

  ```bash
  ./isar/scripts/isar-runqemu.sh \
    --machine qemuarm64 \
    --deploy <path-to-build>/tmp/deploy/images/qemuarm64
  ```

For all options, environment variables, boot modes, and troubleshooting, see [isar/scripts/README.md](scripts/README.md)

---

## 10. Build System Architecture

### 10.1 Container-Based Build Environment

```
┌─────────────────────────────────────────────────────────────┐
│                    Host System                              │
│  • Docker Engine                                            │
│  • BSP Registry Manager (bsp.py)                            │
│  • Configuration Files (YAML)                               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ Launches
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            Privileged Docker Container                      │
│  Image: advantech/bsp-registry/isar/debian-13/kas:5.2       │
│  Base: ghcr.io/siemens/kas/kas-isar:5.0-debian-bookworm    │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  KAS Build System (v5.0)                              │ │
│  │  • Configuration parsing                              │ │
│  │  • Repository management                              │ │
│  │  • BitBake orchestration                              │ │
│  └─────────────────┬─────────────────────────────────────┘ │
│                    │                                         │
│                    ▼                                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  BitBake (Isar-enabled)                               │ │
│  │  • Task dependency resolution                         │ │
│  │  • Parallel execution                                 │ │
│  │  • Package management                                 │ │
│  └─────────────────┬─────────────────────────────────────┘ │
│                    │                                         │
│                    ▼                                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Debian Package Management                            │ │
│  │  • apt/dpkg                                            │ │
│  │  • debootstrap/multistrap                             │ │
│  │  • sbuild/schroot (cross-compilation)                 │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

  Shared Volumes:
  • Source repositories (read-only)
  • Build output directory (read-write)
  • Download cache (read-write)
  • Shared state cache (read-write)
```

### 10.2 Why Privileged Mode?

Isar builds require privileged container execution for:
- **Loop device access**: Creating filesystem images
- **chroot operations**: Setting up cross-compilation environments
- **Device node creation**: Generating special files in rootfs
- **Mount operations**: Handling partition images

This is automatically configured in the BSP registry configuration.

---

## 11. Key Features

### 11.1 Native Debian Packaging

```
Traditional Yocto:          Isar:
───────────────────         ──────
Source Code                 Debian Repository
     ↓                           ↓
Patch & Configure           apt-get download
     ↓                           ↓
Compile (hours)             Extract (seconds)
     ↓                           ↓
Package                     Install via dpkg
     ↓                           ↓
Install to rootfs           Done!
```

### 11.2 Cross-Compilation Support

Isar automatically handles cross-compilation through:
- **sbuild**: Debian's standard cross-build tool
- **schroot**: Isolated build environments
- **multiarch**: Support for multiple architectures

### 11.3 Reproducible Builds

- Pinned repository commits
- Version-locked Debian packages
- Containerized build environment
- Checksum validation

### 11.4 Modular Configuration

Layer-based architecture allows:
- Mix and match distributions
- Reuse machine definitions
- Share common configurations
- Override settings per project

---

## 12. Advantages Over Traditional Build Systems

| Aspect | Yocto/OpenEmbedded | Isar | Advantage |
|--------|-------------------|------|-----------|
| **Build Time** | Hours to days | Minutes | ✅ Isar (10-50x faster) |
| **Learning Curve** | Steep | Moderate | ✅ Isar (Debian familiarity) |
| **Package Availability** | Build from source | Debian repos | ✅ Isar (60,000+ packages) |
| **Image Size** | Minimal possible | Larger (full packages) | ⚖️ Depends on use case |
| **Customization** | Full source control | Package-level | ⚖️ Depends on needs |
| **Security Updates** | Manual recipe updates | apt upgrade | ✅ Isar (automatic) |
| **Reproducibility** | Good (with effort) | Excellent | ✅ Isar (built-in) |
| **Build Infrastructure** | Powerful servers needed | Modest hardware OK | ✅ Isar |
| **Debugging** | Complex | Standard Debian tools | ✅ Isar |

**When to use Isar:**
- Debian-based systems preferred
- Fast iteration needed
- Limited build infrastructure
- Standard Debian packages sufficient
- Long-term Debian support desired

**When to use Yocto:**
- Need absolute minimal images
- Custom hardware with no Debian support
- Full source-level customization required
- Non-Debian distribution needed

---

## 13. Advanced Topics

### 13.1 Custom Package Development

For packages not in Debian repositories, Isar supports custom package recipes:

```
meta-custom/
├── recipes-app/
│   └── myapp/
│       ├── myapp_1.0.bb      # BitBake recipe
│       └── files/
│           ├── myapp         # Application files
│           └── debian/       # Debian packaging
│               ├── control
│               ├── rules
│               └── changelog
```

### 13.2 Adding Custom Layers

To add custom functionality:

1. Create a new meta-layer
2. Add layer to `bblayers_conf`
3. Include layer path in configuration
4. Reference recipes in image

### 13.3 Build Caching

Isar leverages multiple cache levels:

```
┌──────────────────────────────────────┐
│  DL_DIR (Download Cache)             │
│  • Debian .deb packages              │
│  • Source tarballs                   │
│  • Shared across builds              │
└──────────────────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│  SSTATE_DIR (Shared State Cache)     │
│  • Pre-built task outputs            │
│  • Shared across similar builds      │
│  • Massive time savings              │
└──────────────────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│  TMP/DEPLOY (Build Output)           │
│  • Final images                      │
│  • Package manifests                 │
│  • Deployment artifacts              │
└──────────────────────────────────────┘
```

### 13.4 Multiconfig Builds

Build for multiple machines or distributions simultaneously:

```bash
kas-container build \
  isar/isar.yaml:isar/distro/debian-trixie.yaml \
  --target qemuarm64:isar-image-base \
  --target qemuamd64:isar-image-base
```

---

## 14. Resources

### 14.1 Official Documentation

- **Isar GitHub Repository**: [https://github.com/ilbers/isar](https://github.com/ilbers/isar)
- **Isar User Manual**: [https://github.com/ilbers/isar/blob/master/doc/user_manual.md](https://github.com/ilbers/isar/blob/master/doc/user_manual.md)
- **ilbers GmbH** (Isar Maintainer): [https://ilbers.de/en/isar.html](https://ilbers.de/en/isar.html)

### 14.2 Debian Resources

- **Debian Packages**: [https://packages.debian.org/](https://packages.debian.org/)
- **Debian Security Updates**: [https://www.debian.org/security/](https://www.debian.org/security/)
- **Debian Cross-Compilation**: [https://wiki.debian.org/CrossCompiling](https://wiki.debian.org/CrossCompiling)

### 14.3 Advantech-Specific Resources

- **Advantech Isar Modular BSP for NXP**: [https://github.com/Advantech-EECC/meta-isar-modular-bsp-nxp](https://github.com/Advantech-EECC/meta-isar-modular-bsp-nxp)
- **BSP Registry Main README**: [../README.md](../README.md)

### 14.4 KAS Tool

- **KAS Documentation**: [https://kas.readthedocs.io/](https://kas.readthedocs.io/)
- **KAS GitHub**: [https://github.com/siemens/kas](https://github.com/siemens/kas)
- **KAS Container Images**: [https://github.com/siemens/kas/pkgs/container/kas%2Fkas-isar](https://github.com/siemens/kas/pkgs/container/kas%2Fkas-isar)

### 14.5 Community and Support

- **Isar Mailing List**: [isar-users@googlegroups.com](mailto:isar-users@googlegroups.com)
- **GitHub Issues**: [https://github.com/ilbers/isar/issues](https://github.com/ilbers/isar/issues)
- **Stack Overflow**: Tag `isar` for questions

### 14.6 Presentations and Articles

- "Building Products with Debian and Isar" - LinuxFoundation
- "First Experiences with the Embedded Debian Build System Isar" - ELC 2017
- "Isar: Embedded Debian Development 2025" - Siemens OpenSource

---

## 15. Getting Help

For issues specific to this BSP registry:
1. Check the main [README.md](../README.md)
2. Review example configurations in this directory
3. Open an issue in the BSP registry repository
4. Contact Advantech ETC support

For general Isar questions:
1. Consult the [Isar User Manual](https://github.com/ilbers/isar/blob/master/doc/user_manual.md)
2. Search [Isar GitHub Issues](https://github.com/ilbers/isar/issues)
3. Ask on the isar-users mailing list
