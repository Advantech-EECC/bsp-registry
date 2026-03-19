# Advantech BSP configurations registry

[![Validate KAS Configurations](https://github.com/Advantech-EECC/bsp-registry/actions/workflows/validate-kas-configs.yml/badge.svg)](https://github.com/Advantech-EECC/bsp-registry/actions/workflows/validate-kas-configs.yml)
[![Docker containers validation](https://github.com/Advantech-EECC/bsp-registry/actions/workflows/validate-docker-containers.yml/badge.svg)](https://github.com/Advantech-EECC/bsp-registry/actions/workflows/validate-docker-containers.yml)

A Board Support Package (`BSP`) build configuration registry defines environment variables, build systems and configurations to build BSP images. It ensures that the BSP can be consistently built and customized, providing a structured way to manage hardware features, initialization routines, and software components required for embedded systems. This registry allows reproducible builds across different environments and makes it easier to tailor BSPs for unique hardware platforms while maintaining compatibility with the broader OS stack.

The registry supports two build systems:
* **Yocto Project**: For building custom embedded Linux distributions with full control over the software stack
* **Isar**: For building Debian-based embedded systems using native Debian packaging tools

# Table of Contents

- [Advantech BSP configurations registry](#advantech-bsp-configurations-registry)
- [Table of Contents](#table-of-contents)
- [1. Build System Architecture](#1-build-system-architecture)
  - [1.1. Component Overview](#11-component-overview)
    - [1.1.1. Details](#111-details)
- [2. Supported Hardware](#2-supported-hardware)
  - [2.1. NXP Boards Compatibility Matrix](#21-nxp-boards-compatibility-matrix)
    - [2.1.1. Alternative View](#211-alternative-view)
      - [2.1.1.1. Yocto releases](#2111-yocto-releases)
  - [2.2. Isar Build System Support](#22-isar-build-system-support)
    - [2.2.1. Isar Overview](#221-isar-overview)
    - [2.2.2. Isar Hardware Support](#222-isar-hardware-support)
    - [2.2.3. Building Isar BSPs](#223-building-isar-bsps)
    - [2.2.4. Isar Container Configuration](#224-isar-container-configuration)
    - [2.2.5. Isar Resources](#225-isar-resources)
    - [2.1.2. OTA Update Support](#212-ota-update-support)
      - [2.1.2.1. Supported OTA Technologies](#2121-supported-ota-technologies)
      - [2.1.2.2. OTA Support Matrix](#2122-ota-support-matrix)
      - [2.1.2.3. Building Images with OTA Support](#2123-building-images-with-ota-support)
  - [2.3. MediaTek Boards Compatibility Matrix](#23-mediatek-boards-compatibility-matrix)
    - [2.3.1. Building MediaTek BSPs](#231-building-mediatek-bsps)
  - [2.4. Qualcomm Boards Compatibility Matrix](#24-qualcomm-boards-compatibility-matrix)
    - [2.4.1. Building Qualcomm BSPs](#241-building-qualcomm-bsps)
- [3. BSP Registry Manager](#3-bsp-registry-manager)
  - [3.1. Overview](#31-overview)
  - [3.2. Installation](#32-installation)
  - [3.3. Basic Usage](#33-basic-usage)
  - [3.4. Container Management](#34-container-management)
  - [3.5. Configuration File Structure](#35-configuration-file-structure)
  - [3.6. Command Reference](#36-command-reference)
    - [3.6.1. Checkout and Validation](#361-checkout-and-validation)
  - [4. HowTo Assemble BSPs](#4-howto-assemble-bsps)
    - [4.1. Host System dependencies](#41-host-system-dependencies)
      - [4.1.1. Setup Python virtual environment](#411-setup-python-virtual-environment)
        - [4.1.1.1. Advanced Tools for Managing Multiple Python Environments](#4111-advanced-tools-for-managing-multiple-python-environments)
        - [4.1.1.2. Install Python packages dependencies](#4112-install-python-packages-dependencies)
      - [4.1.2. Setting up Docker engine](#412-setting-up-docker-engine)
      - [4.1.2.1. Docker `buildx`](#4121-docker-buildx)
  - [4.2. Building BSP](#42-building-bsp)
    - [4.2.1. Running BSP build](#421-running-bsp-build)
    - [4.2.2. Running Modular BSP build](#422-running-modular-bsp-build)
    - [4.2.3. Bitbake development shell](#423-bitbake-development-shell)
  - [4.3. HowTo build a BSP using KAS](#43-howto-build-a-bsp-using-kas)
    - [4.3.1. Building a BSP image using KAS in a container](#431-building-a-bsp-image-using-kas-in-a-container)
    - [4.3.2. Bitbake development shell](#432-bitbake-development-shell)
  - [4.4. HowTo build a BSP using Repo Tool](#44-howto-build-a-bsp-using-repo-tool)
  - [5. Advanced Topics](#5-advanced-topics)
    - [5.1. Export KAS configuration](#51-export-kas-configuration)
    - [5.2. Lock KAS configuration](#52-lock-kas-configuration)
    - [5.3. Reusing BSP Registry configurations](#53-reusing-bsp-registry-configurations)
  - [6. Patches](#6-patches)
  - [7. Links](#7-links)

---

# 1. Build System Architecture

Build System Architecture defines the structure and workflow of how source code, configurations, and dependencies are transformed into deployable artifacts. The registry supports two build systems: **Yocto Project** (for custom embedded Linux distributions) and **Isar** (for Debian-based embedded systems).

## 1.1. Component Overview

The build system follows a layered architecture that ensures reproducibility, isolation, and maintainability:

```bash
┌─────────────────────────────────────────┐
│         BSP Registry Manager            │  # BSP management and container orchestration
├─────────────────────────────────────────┤
│          KAS Configuration Files        │  # Build definitions
├─────────────────────────────────────────┤
│         Docker Container Engine         │  # Isolated build environment
├─────────────────────────────────────────┤
│    Yocto Project / Isar Build System    │  # Core build systems
├─────────────────────────────────────────┤
│   Source Layers / Debian Packages       │  # BSP components
└─────────────────────────────────────────┘
```

### 1.1.1. Details

| Layer | Purpose | Key Components |
|-------|---------|----------------|
| **BSP Registry Manager** | BSP management and container orchestration | `bsp` CLI tool (`bsp-registry-tools` package), YAML configuration, container definitions |
| **KAS Configuration Files** | Build definitions and dependencies | YAML configs for boards, distros, and features |
| **Docker Container Engine** | Isolated build environment | Consistent toolchains, isolated dependencies |
| **Yocto Project / Isar Build System** | Core build systems | Yocto: BitBake, OpenEmbedded, meta-layers; Isar: apt, dpkg, Debian packages |
| **Source Layers / Debian Packages** | BSP components | Yocto: Machine configs, recipes, kernel; Isar: Debian packages, system configuration |

---

# 2. Supported Hardware

The BSP build system is designed to support a wide range of hardware platforms, including reference boards, evaluation kits, and custom embedded devices. Each supported target is defined through configuration files that specify processor architecture, memory layout, peripherals, and drivers, ensuring that builds are tailored to the unique requirements of the hardware.

## 2.1. NXP Boards Compatibility Matrix

Table describes in which combinations yocto releases could be used together with boards.

| Board \ Yocto  | walnascar | styhead | scarthgap | mickledore | langdale | kirkstone | Status        |
| -------------- | :-------: | :-----: | :-------: | :--------: | :------: | :-------: | ------------- |
| **RSB3720**    |     ✅     |    ✅    |     ✅     |     ❌      |    ❌     |     🟡     | 🟢 Stable      |
| **RSB3720 4G** |     ✅     |    ❌    |     ❌     |     ❌      |    ❌     |     ❌     | 🟢 Stable      |
| **RSB3720 6G** |     ✅     |    ❌    |     ❌     |     ❌      |    ❌     |     ❌     | 🟢 Stable      |
| **RSB3730**    |     ❌     |    ❌    |     ❌     |     ✅      |    ❌     |     ❌     | 🟡 Development |
| **ROM2620**    |     ✅     |    ✅    |     ✅     |     ❌      |    ❌     |     ❌     | 🟢 Stable      |
| **ROM5720**    |     ✅     |    ✅    |     ✅     |     ❌      |    ❌     |     ❌     | 🟢 Stable      |
| **ROM5721**    |     ✅     |    ✅    |     ✅     |     ✅      |    ❌     |     ❌     | 🟢 Stable      |
| **ROM5721 1G** |     ✅     |    ❌    |     ✅     |     ✅      |    ❌     |     ❌     | 🟢 Stable      |
| **ROM5721 2G** |     ✅     |    ❌    |     ✅     |     ✅      |    ❌     |     ❌     | 🟢 Stable      |
| **ROM5722**    |     ✅     |    ✅    |     ✅     |     ❌      |    ❌     |     ❌     | 🟢 Stable      |
| **ROM2820**    |     ✅     |    ✅    |     ✅     |     ❌      |    ❌     |     ❌     | 🟢 Stable      |
| **AOM5521 A1** |     🟡     |    ❌    |     ✅     |     ❌      |    ❌     |     ❌     | 🟢 Stable      |
| **AOM5521 A2** |     ✅     |    ❌    |     ❌     |     ❌      |    ❌     |     ❌     | 🟢 Stable      |

**Status Legend:**

* 🟢 **Stable**: Production-ready, fully tested and supported
* 🟡 **Development**: Under active development, may have limitations
* 🔴 **EOL**: End of Life, not recommended for new projects

### 2.1.1. Alternative View

| **Hardware**   | **Supported Releases** | **Status** | **Documentation** |
|----------------|-------------------------|------------|-------------------|
| **RSB3720**    | walnascar, styhead, scarthgap | 🟢 Stable | [Advantech RSB-3720 Product Page](https://www.advantech.com/en-us/products/5912096e-f242-4b17-993a-1acdcaada6f6/rsb-3720/mod_d2f1b0bc-650b-449a-8ef7-b65ce4f69949) · [User Manual](https://www.manualslib.com/manual/2293645/Advantech-Rsb-3720.html) |
| **RSB3720 4G** | walnascar | 🟢 Stable | *(Same as RSB3720, variant-specific)* |
| **RSB3720 6G** | walnascar | 🟢 Stable | *(Same as RSB3720, variant-specific)* |
| **RSB3730**    | mickledore | 🟡 Development | [Advantech RSB-3730 Product Page](https://www.advantech.com/en-eu/products/5912096e-f242-4b17-993a-1acdcaada6f6/rsb-3730/mod_5d7887e6-b7e3-427c-8729-b81ac7d89ccd) · [RSB-3730 User Manual (PDF)](https://advdownload.advantech.com/productfile/Downloadfile4/1-2HACYHA/RSB-3730_User_Manual_Eng_yocto%20Ed.1_FINAL.pdf) · [Yocto BSP Guide](https://ess-wiki.advantech.com.tw/view/Yocto_Linux_BSP_Ver.A_User_Guide_for_RSB-3730_series-Yocto_4.2) |
| **ROM2620**    | walnascar, styhead, scarthgap | 🟢 Stable | [Advantech ROM-2620 Product Page](https://www.advantech.com/en-eu/products/8fc6f753-ca1d-49f9-8676-10d53129570f/rom-2620/mod_294031c8-4a21-4b95-adf2-923c412ef761) |
| **ROM5720**    | walnascar, styhead, scarthgap | 🟢 Stable | [Advantech ROM-5720 Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5720/mod_4fbfe9fa-f5b2-4ba8-940e-e47585ad0fef) |
| **ROM5721**    | walnascar, styhead, scarthgap, mickledore | 🟢 Stable | [Advantech ROM-5721 Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5721/mod_271dbc68-878b-486d-85cf-30cc9f1f8f16) |
| **ROM5721 1G** | walnascar, scarthgap, mickledore | 🟢 Stable | *(Same as ROM5721, variant-specific)* |
| **ROM5721 2G** | walnascar, scarthgap, mickledore | 🟢 Stable | *(Same as ROM5721, variant-specific)* |
| **ROM5722**    | walnascar, styhead, scarthgap | 🟢 Stable | [Advantech ROM-5722 Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5722/mod_11aa0c77-868e-4014-8151-ac7a7a1c5c1b) |
| **ROM2820**    | walnascar, styhead, scarthgap | 🟢 Stable | [Advantech ROM-2820 Product Page](https://www.advantech.com/en-eu/products/8fc6f753-ca1d-49f9-8676-10d53129570f/rom-2820/mod_bb82922e-d3a2-49d7-80ff-dc57f400185e) |
| **AOM5521 A1** | scarthgap | 🟢 Stable | [Advantech AOM-5521 Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/aom-5521/mod_75b36e99-ac3f-4801-8b2b-1706ade1025d) |
| **AOM5521 A1** | walnascar | 🟡 Development | *(Same as above)* |
| **AOM5521 A2** | walnascar | 🟢 Stable | *(Same as above)* |

#### 2.1.1.1. Yocto releases

This list below covers the most recent and commonly referenced Yocto releases:

* [Walnascar (Yocto 5.2)](https://docs.yoctoproject.org/walnascar/releases.html)  
* [Styhead (Yocto 5.1)](https://docs.yoctoproject.org/dev/migration-guides/release-5.1.html)  
* [Scarthgap (Yocto 5.0 LTS)](https://docs.yoctoproject.org/scarthgap/releases.html)  
* [Mickledore (Yocto 4.2)](https://docs.yoctoproject.org/mickledore/releases.html)  
* [Kirkstone (Yocto 4.0 LTS)](https://docs.yoctoproject.org/kirkstone/releases.html)  

The full overview of Yocto releases can be found here https://www.yoctoproject.org/development/releases/

## 2.2. Isar Build System Support

In addition to Yocto-based BSPs, this registry supports **Isar** (Integration System for Automated Root filesystem generation), a build system specifically designed for creating Debian-based embedded Linux systems. Isar uses Debian's native packaging tools (apt, dpkg) rather than BitBake, providing a more familiar environment for developers experienced with Debian/Ubuntu systems.

### 2.2.1. Isar Overview

📖 **For detailed information**, see the **[Isar Directory README](isar/README.md)** which includes comprehensive documentation on configuration, build architecture, and ASCII diagrams of the image generation process.

**Key Features:**
* Native Debian package management (apt/dpkg)
* Supports multiple Debian-based distributions (Debian, Ubuntu)
* Faster build times for Debian-familiar developers
* Direct access to Debian package ecosystem
* Cross-compilation support for ARM, ARM64, x86, and x86-64 architectures

**Supported Distributions:**
* Debian (Bookworm, Bullseye, Buster, Trixie, Sid)
* Ubuntu (Focal, Jammy, Noble)

### 2.2.2. Isar Hardware Support

The registry includes Isar-based BSP configurations for the following targets:

| Hardware | Distribution | Status | BSP Name |
|----------|-------------|--------|----------|
| **RSB3720** | Debian Trixie | 🟡 Development | `adv-mbsp-isar-debian-rsb3720` |
| **QEMU ARM64** | Debian Trixie | ✅ Ready | `isar-qemuarm64-debian-trixie` |
| **QEMU ARM64** | Ubuntu Noble | ✅ Ready | `isar-qemuarm64-ubuntu-noble` |
| **QEMU ARM** | Debian Trixie | ✅ Ready | `isar-qemuarm-debian-trixie` |

**Status Legend:**
* ✅ **Ready**: Functional and available for testing/development
* 🟡 **Development**: Under active development

### 2.2.3. Building Isar BSPs

Isar builds require privileged container execution to support Debian package management operations. The registry handles this automatically when using Isar-enabled containers.

**Example: Build RSB3720 with Debian Trixie**
```bash
bsp build adv-mbsp-isar-debian-rsb3720
```

**Example: Build QEMU ARM64 with Debian Trixie**
```bash
bsp build isar-qemuarm64-debian-trixie
```

**Example: Build QEMU ARM64 with Ubuntu Noble**
```bash
bsp build isar-qemuarm64-ubuntu-noble
```

### 2.2.4. Isar Container Configuration

Isar builds use the `isar-debian-13` container, which is automatically configured with:
* Privileged mode for package management operations
* Based on official kas-isar container images
* KAS version 5.0
* Debian Trixie base distribution

The container definition in `bsp-registry.yml`:
```yaml
- isar-debian-13:
    file: Dockerfile.isar.debian
    image: "advantech/bsp-registry/isar/debian-13/kas:5.2"
    privileged: true
    args:
      - name: "KAS_VERSION"
        value: "5.2"
      - name: "DISTRO"
        value: "debian-trixie"
```

### 2.2.5. Isar Resources

* **[Isar Directory README](isar/README.md)** - Comprehensive guide to Isar configuration, build process diagrams, and advanced topics
* [Isar Documentation](https://github.com/ilbers/isar/blob/master/doc/user_manual.md)
* [Isar GitHub Repository](https://github.com/ilbers/isar)
* [Advantech Isar Modular BSP](https://github.com/Advantech-EECC/meta-isar-modular-bsp-nxp)

### 2.1.2. OTA Update Support

The BSP registry includes Over-The-Air (OTA) update configurations for supported boards. OTA updates enable remote software updates without physical access to devices, critical for production deployments.

#### 2.1.2.1. Supported OTA Technologies

* **RAUC** (Robust Auto-Update Controller): A safe and reliable software update framework that supports atomic updates with rollback capabilities
* **SWUpdate**: A software update framework designed for embedded systems with support for multiple update strategies
* **OSTree**: An upgrade system for Linux-based operating systems that performs atomic upgrades of complete filesystem trees

#### 2.1.2.2. OTA Support Matrix

The following boards support OTA updates with the indicated technologies and Yocto releases:

| Board | RAUC | SWUpdate | OSTree | Supported Releases |
|-------|:----:|:--------:|:------:|-------------------|
| **RSB3720** | ✅ | ✅ | ✅ | walnascar, styhead, scarthgap |
| **RSB3720-4G** | ✅ | ✅ | ❌ | walnascar |
| **RSB3720-6G** | ✅ | ✅ | ❌ | walnascar |
| **ROM2620-ED91** | ✅ | ✅ | ✅ | walnascar, styhead, scarthgap |
| **ROM2820-ED93** | ✅ | ✅ | ✅ | walnascar, styhead, scarthgap |
| **ROM5720-DB5901** | ✅ | ✅ | ✅ | walnascar, styhead, scarthgap |
| **ROM5721-1G-DB5901** | ✅ | ✅ | ✅ | walnascar |
| **ROM5721-2G-DB5901** | ✅ | ✅ | ✅ | walnascar |
| **ROM5722-DB2510** | ✅ | ✅ | ✅ | walnascar, styhead, scarthgap |

#### 2.1.2.3. Building Images with OTA Support

To build a BSP image with OTA support, use the `bsp build` command:

```bash
# Build with RAUC OTA support
bsp build adv-ota-mbsp-oenxp-rauc-walnascar-rsb3720

# Build with RAUC OTA support for RSB3720 4G variant
bsp build adv-ota-mbsp-oenxp-rauc-walnascar-rsb3720-4g

# Build with SWUpdate OTA support
bsp build adv-ota-mbsp-oenxp-swupdate-scarthgap-rsb3720

# Build with OSTree OTA support
bsp build adv-ota-mbsp-oenxp-ostree-styhead-rom5722-db2510
```

Alternatively, you can use the `bsp` CLI tool directly:

```bash
# List all available OTA configurations
bsp list | grep ota

# Build a specific OTA configuration
bsp build adv-ota-mbsp-oenxp-rauc-walnascar-rsb3720-6g

# Build RSB3720 4G variant with RAUC OTA support
bsp build adv-ota-mbsp-oenxp-rauc-walnascar-rsb3720-4g
```

## 2.3. MediaTek Boards Compatibility Matrix

The BSP registry supports MediaTek-based boards through the **MediaTek AIoT Rity** BSP stack. The
current integration targets the Yocto **Scarthgap** release and uses the upstream Rity v25.0 layer
set. For detailed configuration, see the [MediaTek vendor README](vendors/mediatek/README.md) and the
[Advantech MediaTek overlay README](vendors/advantech/mediatek/README.md).

| Board \ Yocto  | scarthgap | Status        |
| -------------- | :-------: | ------------- |
| **Genio 1200 EVK** | ✅    | 🟡 Development |
| **RSB-3810**   |     ✅     | 🟡 Development |

**Status Legend:**

* 🟢 **Stable**: Production-ready, fully tested and supported
* 🟡 **Development**: Under active development, may have limitations

| **Hardware**         | **Supported Releases** | **Status**       | **Documentation** |
|----------------------|------------------------|------------------|-------------------|
| **Genio 1200 EVK**   | scarthgap              | 🟡 Development   | [MediaTek Genio 1200 EVK](https://mediatek.gitlab.io/aiot/doc/aiot-dev-guide/master/hw/g1200-evk.html) |
| **RSB-3810**         | scarthgap              | 🟡 Development   | [Advantech RSB-3810](https://ess-wiki.advantech.com.tw/view/AIM-Linux/RSB-3810) |

### 2.3.1. Building MediaTek BSPs

```bash
# List available MediaTek BSPs
bsp list | grep -i oemtk

# Build MediaTek Genio 1200 EVK (scarthgap)
bsp build oemtk-scarthgap-genio-1200-evk

# Build Advantech RSB-3810 (scarthgap)
bsp build adv-mbsp-oemtk-scarthgap-rsb3810
```

---

## 2.4. Qualcomm Boards Compatibility Matrix

The BSP registry supports Qualcomm-based boards through the **Qualcomm Linux (QLI)** BSP stack.
The current integration targets the Yocto **Scarthgap** release and uses the QLI v1.5 Ver.1.1 layer
set. For detailed configuration, see the [Qualcomm vendor README](vendors/qualcomm/README.md) and
the [Advantech Qualcomm overlay README](vendors/advantech/qualcomm/README.md).

| Board \ Yocto         | scarthgap | Status        |
| --------------------- | :-------: | ------------- |
| **QCS6490 RB3gen2**   |     ✅     | 🟡 Development |
| **AOM-2721**          |     ✅     | 🟡 Development |

**Status Legend:**

* 🟢 **Stable**: Production-ready, fully tested and supported
* 🟡 **Development**: Under active development, may have limitations

| **Hardware**          | **Supported Releases** | **Status**     | **Documentation** |
|-----------------------|------------------------|----------------|-------------------|
| **QCS6490 RB3gen2**   | scarthgap              | 🟡 Development | [Qualcomm RB3gen2 Vision Kit](https://www.qualcomm.com/developer/hardware/rb3-gen-2-development-kit) |
| **AOM-2721**          | scarthgap              | 🟡 Development | [Advantech AOM-2721 Product Page](https://www.advantech.com/en/products/som/aom-2721) |

### 2.4.1. Building Qualcomm BSPs

```bash
# List available Qualcomm BSPs
bsp list | grep -i qcom

# Build Qualcomm QCS6490 RB3gen2 EVK (scarthgap)
bsp build bsp-oeqcom-scarthgap-qcs6490-evk
```

---

# 3. BSP Registry Manager

The BSP Registry Manager is provided by the [`bsp-registry-tools`](https://pypi.org/project/bsp-registry-tools/) Python package. It offers a command-line interface (`bsp`) for managing and building Yocto-based BSPs using the KAS build system. It features Docker container management, cached builds, and sophisticated configuration management for embedded Linux development.

## 3.1. Overview

The BSP Registry Manager supports:

- **BSP registry management** via YAML configuration files
- **Docker container building and management** for reproducible builds
- **KAS build system integration** for Yocto-based builds
- **Interactive shell access** to build environments
- **Comprehensive error handling** and configuration validation
- **Advanced cache management** for faster incremental builds
- **Environment variable configuration management** with expansion support
- **KAS configuration export** functionality

## 3.2. Installation

The BSP Registry Manager requires Python 3.7+ and is installed via pip. A virtual environment is recommended to avoid conflicts with system packages:

```bash
# Optional: create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install bsp-registry-tools
pip3 install bsp-registry-tools
```

## 3.3. Basic Usage

```bash
# List available BSPs in the registry
bsp list

# Checkout and validate a BSP configuration without building (fast)
bsp build <bsp_name> --checkout

# Build a specific BSP
bsp build <bsp_name>

# Enter interactive shell for a BSP
bsp shell <bsp_name>

# Export BSP configuration
bsp export <bsp_name>

# List available container definitions
bsp containers
```

## 3.4. Container Management

The BSP Registry Manager supports container definitions that can be shared across multiple BSPs:

```bash
# List all available containers
bsp containers

# Example output:
# Available Containers:
# - ubuntu-20.04:
#     Image: advantech/bsp-registry/ubuntu-20.04/kas:4.7
#     File: Dockerfile.ubuntu
#     Args: DISTRO=ubuntu:20.04, KAS_VERSION=4.7
# - ubuntu-22.04:
#     Image: advantech/bsp-registry/ubuntu-22.04/kas:5.2
#     File: Dockerfile.ubuntu
#     Args: DISTRO=ubuntu:22.04, KAS_VERSION=5.0
```

## 3.5. Configuration File Structure

The BSP registry uses a YAML configuration file (default: `bsp-registry.yml`) with the following structure:

```yaml
specification:
  version: '1.0'

# Global environment variables (supports $ENV{VAR} expansion)
environment:
  - name: "DL_DIR"
    value: "$ENV{HOME}/yocto-cache/downloads"
  - name: "SSTATE_DIR"
    value: "$ENV{HOME}/yocto-cache/sstate-cache"

# Container definitions (reusable across BSPs)
containers:
  - ubuntu-20.04:
      file: Dockerfile.ubuntu
      image: "advantech/bsp-registry/ubuntu-20.04/kas:4.7"
      args:
        - name: "DISTRO"
          value: "ubuntu:20.04"
        - name: "KAS_VERSION"
          value: "4.7"
  - ubuntu-22.04:
      file: Dockerfile.ubuntu
      image: "advantech/bsp-registry/ubuntu-22.04/kas:5.2"
      args:
        - name: "DISTRO"
          value: "ubuntu:22.04"
        - name: "KAS_VERSION"
          value: "5.2"

# BSP definitions
registry:
  bsp:
    - name: "imx8mpevk"
      description: "i.MX8MP EVK Board"
      os:
        name: "linux"
        build_system: "yocto"
        version: "scarthgap"
      build:
        path: "build/imx8mpevk"
        copy:
          - scripts/helper.sh: build/  # Copies into <build path>/build/
        environment:
          container: "ubuntu-22.04"  # Reference to container definition
          runtime_args: "--device=/dev/net/tun --cap-add=NET_ADMIN"  # Optional kas-container args (e.g. for QEMU networking)
        docker: "docker"
        configuration:
          - "conf/imx8mpevk.yml"
          - "conf/scarthgap.yml"
```

## 3.6. Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List all available BSPs | `bsp list` |
| `build <bsp_name>` | Build a specific BSP | `bsp build imx8mpevk` |
| `build <bsp_name> --checkout` | Checkout and validate BSP configuration without building (fast) | `bsp build imx8mpevk --checkout` |
| `shell <bsp_name>` | Enter interactive shell | `bsp shell imx8mpevk` |
| `export <bsp_name>` | Export KAS configuration | `bsp export imx8mpevk` |
| `containers` | List available containers | `bsp containers` |

### 3.6.1. Checkout and Validation

The `--checkout` flag provides a fast way to checkout and validate BSP configurations without performing time-consuming Docker builds and Yocto compilations. This follows the KAS command naming convention (`kas checkout`). It is particularly useful for:

- **CI/CD pipelines**: Quickly verify configuration validity before committing resources to a full build
- **Development iteration**: Test configuration changes without waiting for complete builds
- **Pre-build checks**: Ensure all required files and repositories are accessible before starting a build

**How it works:**

1. Validates BSP configuration files and dependencies
2. Skips Docker image build (uses native KAS installation)
3. Runs `kas checkout` to verify repository configurations
4. Validates that all required source repositories can be cloned
5. Confirms build configuration is valid without performing actual compilation

**Example:**

```bash
# Checkout and validate configuration for RSB3720 6G board
bsp build adv-mbsp-oenxp-walnascar-rsb3720-6g --checkout

# Checkout and validate configuration for RSB3720 4G board
bsp build adv-mbsp-oenxp-walnascar-rsb3720-4g --checkout

# If validation passes, proceed with full build
bsp build adv-mbsp-oenxp-walnascar-rsb3720-6g
```

---

## 4. HowTo Assemble BSPs

This chapter explains how to assemble modular BSPs using KAS configuration files. It provides step‑by‑step instructions for setting up prerequisites, selecting the right configuration, and running builds to generate reproducible BSP images tailored to specific hardware platforms.

### 4.1. Host System dependencies

The host system must provide essential tools and libraries required for building BSPs, including compilers, version control systems, and scripting environments. Ensuring these dependencies are installed and up to date guarantees a stable build process and consistent results across different development environments.

**Host system initial setup must include:**

* Python 3.x
  * Including python virtual environment module
* `pip` package manager is available
* Docker
* Git

The build have been tested on the following host systems: `Ubuntu 22.04`, `Ubuntu 24.04`

#### 4.1.1. Setup Python virtual environment

It is recommended to install python based tools and packages in a separate python virtual envronment, which could be created
using python virtualenv package.

```bash
python3 -m venv venv
```

To activate virtual environment use following command:

```bash
source venv/bin/activate
```

##### 4.1.1.1. Advanced Tools for Managing Multiple Python Environments

While venv and virtualenv cover most basic needs, advanced tools provide additional functionality for dependency management, reproducibility, and handling multiple Python versions.

* [pipenv](https://pipenv.pypa.io/en/latest/)
* [pyenv](https://github.com/pyenv/pyenv)
* [conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html) 

##### 4.1.1.2. Install Python packages dependencies

Install the `bsp-registry-tools` package to get the `bsp` CLI tool:

```bash
pip3 install bsp-registry-tools
```

#### 4.1.2. Setting up Docker engine

The BSP images build would run in a docker container, meaning host system should have docker installed.
If your host system is Ubuntu, check official docker installation guide at <https://docs.docker.com/engine/install/ubuntu/>.

To run docker from a non root user (which is required) please follow instructions from the official docker documentation
<https://docs.docker.com/engine/install/linux-postinstall/>. But, in most cases, one command have to be executed

```bash
sudo usermod -aG docker $USER
```

and reboot or re-login the system for the changes to take affect.

#### 4.1.2.1. Docker `buildx`

Docker `buildx` extends the standard Docker build command with advanced capabilities powered by BuildKit. It enables developers to build multi‑platform images, leverage efficient caching, and run builds in parallel, ensuring faster and more consistent results across diverse environments.

To download `buildx` binary for your host system use link below:
<https://github.com/docker/buildx?tab=readme-ov-file#manual-download>

## 4.2. Building BSP

Building a Board Support Package (BSP) combining Yocto, KAS, and Docker. Yocto provides the framework for creating custom Linux distributions tailored to specific hardware platforms. KAS simplifies the process by managing layered build configurations through YAML files, ensuring reproducibility and modularity. Docker adds portability by encapsulating the build environment, eliminating host system inconsistencies and making it easy to run builds across different machines.

Together, these tools enable developers to assemble BSP images in a consistent, automated, and scalable way. By defining configurations in KAS, leveraging Yocto recipes, and running builds inside Docker containers, teams can ensure reliable results while reducing setup complexity and dependency issues.

### 4.2.1. Running BSP build

Use the `bsp` CLI tool to list available BSPs and build a specific one:

```bash
# List available BSPs
bsp list

# Build a specific BSP
bsp build adv-mbsp-oenxp-scarthgap-rsb3720
```

### 4.2.2. Running Modular BSP build

To build a BSP image for a specific Yocto release use command below:

```bash
# Build Modular BSP for RSB3720 (Scarthgap)
bsp build adv-mbsp-oenxp-scarthgap-rsb3720
```

Use command below to build i.MX images with OTA support

```bash
# Build with RAUC OTA support
bsp build adv-ota-mbsp-oenxp-rauc-scarthgap-rsb3720
```

Use command below to build i.MX images with ROS2 support

```bash
# Build with ROS2 Humble support
bsp build adv-mbsp-oenxp-ros2-humble-scarthgap-rsb3720
```

### 4.2.3. Bitbake development shell

To enter a docker container shell initialized with yocto bitbake environment run:

```bash
bsp shell adv-mbsp-oenxp-scarthgap-rsb3720
```

## 4.3. HowTo build a BSP using KAS

To assemble BSP images using KAS tool following commands can be used

```bash
# activate python virtual environment
source venv/bin/activate

# add proper KAS configuration variables to your environment
source .env

# run the build
# kas build <path-to-kas-yaml-file>
kas build adv-mbsp-oenxp-walnascar-rsb3720-6g.yaml

# Build RSB3720 4G variant
kas build adv-mbsp-oenxp-walnascar-rsb3720-4g.yaml
```

### 4.3.1. Building a BSP image using KAS in a container

Define environment variables `KAS_CONTAINER_ENGINE` and `KAS_CONTAINER_IMAGE`. 

For example:

```bash
export KAS_CONTAINER_ENGINE=docker
export KAS_CONTAINER_IMAGE=advantech/bsp-registry/ubuntu:22.04
```

Container image should have `kas` tool installed inside and use [scripts/kas/container-entrypoint](./scripts/kas/container-entrypoint) script. Check [Dockerfile.ubuntu](./Dockerfile.ubuntu) for reference.

To run build inside a docker container use `kas-container` tool

```bash
kas-container build adv-mbsp-oenxp-walnascar-rsb3720-6g.yaml

# Build RSB3720 4G variant
kas-container build adv-mbsp-oenxp-walnascar-rsb3720-4g.yaml
```

### 4.3.2. Bitbake development shell

Using pure `kas` it is possible to enter bitbake shell via command:

```bash
kas shell adv-mbsp-oenxp-walnascar-rsb3720-6g.yaml

# Or for RSB3720 4G variant
kas shell adv-mbsp-oenxp-walnascar-rsb3720-4g.yaml
```

or in a `docker` container using following command:

```bash
kas-container shell adv-mbsp-oenxp-walnascar-rsb3720-6g.yaml

# Or for RSB3720 4G variant
kas-container shell adv-mbsp-oenxp-walnascar-rsb3720-4g.yaml
```

## 4.4. HowTo build a BSP using Repo Tool

For users who prefer the traditional Yocto workflow using the `repo` tool and standard BitBake commands, we provide comprehensive documentation in a separate guide.

The repo-based workflow is ideal for:

* Developers familiar with standard Yocto Project workflows
* Integration with NXP i.MX reference documentation
* Projects requiring fine-grained control over layer management
* Direct use of BitBake without container abstraction

**📖 See the complete guide:** [Building Modular BSP using Repo Tool](BUILDING_WITH_REPO.md)

This guide covers:

* Installing and configuring the repo tool
* Downloading BSP sources from the [imx-manifest](https://github.com/Advantech-EECC/imx-manifest) repository
* Setting up the build environment
* Building images for Advantech boards (RSB3720, ROM2620, ROM5722, etc.)
* Troubleshooting common issues

---

## 5. Advanced Topics

This chapter provides overview of advanced topics working with KAS build configurations.

### 5.1. Export KAS configuration

kas tool can dump final configuration in standart output with `kas dump` command

```bash
kas dump adv-mbsp-oenxp-walnascar-rsb3720-6g.yaml > final.yaml

# Or for RSB3720 4G variant
kas dump adv-mbsp-oenxp-walnascar-rsb3720-4g.yaml > final.yaml
```

For details check https://kas.readthedocs.io/en/latest/userguide/plugins.html#module-kas.plugins.dump

`final.yaml` would contain all the included `yaml` configuration files and can be reused later.

### 5.2. Lock KAS configuration

Similar to `kas dump` there is a `kas lock` command, it would generate a yaml file with all layer revisions. 
For datailed overview check official kas documentation https://kas.readthedocs.io/en/latest/userguide/plugins.html#module-kas.plugins.lock

### 5.3. Reusing BSP Registry configurations

It is possible to include BSP registry YAML configurations in your images (provided your project uses kas to assemble OS images). An example KAS configuration 

To extend an existing BSP with a custom Yocto layer create a following kas config:

```yaml
header:
  version: 19
  includes:
    - repo: bsp-registry
      file: adv-mbsp-oenxp-walnascar-rsb3720-6g.yaml

repos:
  this:
    layers:
      meta-custom:

  bsp-registry:
    url: "https://github.com/Advantech-EECC/modular-bsp-build"
    branch: "main"
    layers:
      .: "disabled"
```

where `meta-custom` repository scructure looks like:

```bash
(venv) ➜  meta-custom
.
├── .config.yaml
└── meta-custom
    ├── conf
    │   └── layer.conf
    └── recipes-core
        └── imx-image-%.bbappend
```

where `imx-image-%.bbappend` recipes contains:

```bitbake
CORE_IMAGE_EXTRA_INSTALL += "mpv"
LICENSE_FLAGS_ACCEPTED += "commercial"
```

and layer configuration:

```bitbake
# We have a conf and classes directory, add to BBPATH
BBPATH .= ":${LAYERDIR}"

# We have recipes-* directories, add to BBFILES
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
            ${LAYERDIR}/recipes-*/*/*.bbappend"

BBFILE_COLLECTIONS += "custom"
BBFILE_PATTERN_custom = "^${LAYERDIR}/"
BBFILE_PRIORITY_custom = "10"
LAYERVERSION_custom = "0.1"
LAYERSERIES_COMPAT_custom = "scarthgap"
LAYERDEPENDS_custom = "eecc-nxp"
```

---

## 6. Patches

The BSP registry uses patches to fix build issues, add hardware support, and ensure compatibility across different Yocto releases. Patches are organized by vendor and Yocto version to maintain stability and reproducibility.

The repository contains **16 patches** organized into:

* **NXP vendor patches** (12 patches): Address build failures, dependency corrections, and hardware-specific configurations for NXP i.MX platforms
* **OTA feature patches** (2 patches): Enable OSTree-based over-the-air updates for Styhead and Walnascar releases
* **MediaTek vendor patches** (2 patches): Fix recipe and git checkout issues specific to the MediaTek Rity Scarthgap BSP

All patches are documented with:

* Purpose and rationale
* Affected layers and recipes
* Yocto release compatibility

For detailed information about each patch, including what they fix and which components they affect, see the **[Patches Documentation](patches/README.md)**.

---

## 7. Links

* [Building Modular BSP using Repo Tool](BUILDING_WITH_REPO.md) - Alternative build method using Google's repo tool
* [KAS Container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html)
* [KAS](https://kas.readthedocs.io/en/latest/intro.html)
