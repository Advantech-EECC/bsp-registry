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
    - [2.1.2. OTA Update Support](#212-ota-update-support)
      - [2.1.2.1. Supported OTA Technologies](#2121-supported-ota-technologies)
      - [2.1.2.2. OTA Support Matrix](#2122-ota-support-matrix)
      - [2.1.2.3. Building Images with OTA Support](#2123-building-images-with-ota-support)
    - [2.1.3. Secure Boot Support](#213-secure-boot-support)
      - [2.1.3.1. Secure Boot Support Matrix](#2131-secure-boot-support-matrix)
      - [2.1.3.2. Building Images with Secure Boot](#2132-building-images-with-secure-boot)
  - [2.2. Isar Build System Support](#22-isar-build-system-support)
    - [2.2.1. Isar Overview](#221-isar-overview)
    - [2.2.2. Isar Hardware Support](#222-isar-hardware-support)
    - [2.2.3. Building Isar BSPs](#223-building-isar-bsps)
    - [2.2.4. Isar Container Configuration](#224-isar-container-configuration)
    - [2.2.5. Isar Resources](#225-isar-resources)
  - [2.3. MediaTek Boards Compatibility Matrix [preview]](#23-mediatek-boards-compatibility-matrix-preview)
    - [2.3.1. Building MediaTek BSPs](#231-building-mediatek-bsps)
  - [2.4. Qualcomm Boards Compatibility Matrix](#24-qualcomm-boards-compatibility-matrix)
    - [2.4.1. Building Qualcomm BSPs](#241-building-qualcomm-bsps)
  - [2.5. NVIDIA Jetson Boards Compatibility Matrix](#25-nvidia-jetson-boards-compatibility-matrix)
    - [2.5.1. Building NVIDIA Jetson BSPs](#251-building-nvidia-jetson-bsps)
- [3. BSP Registry Manager](#3-bsp-registry-manager)
  - [3.1. Overview](#31-overview)
  - [3.2. Installation](#32-installation)
  - [3.3. Basic Usage](#33-basic-usage)
  - [3.4. Command Reference](#34-command-reference)
    - [3.4.1. Checkout and Validation](#341-checkout-and-validation)
- [4. HowTo Assemble BSPs](#4-howto-assemble-bsps)
  - [4.1. Host System dependencies](#41-host-system-dependencies)
    - [4.1.1. Setup Python virtual environment](#411-setup-python-virtual-environment)
      - [4.1.1.1. Advanced Tools for Managing Multiple Python Environments](#4111-advanced-tools-for-managing-multiple-python-environments)
      - [4.1.1.2. Install Python packages dependencies](#4112-install-python-packages-dependencies)
    - [4.1.2. Setting up Docker engine](#412-setting-up-docker-engine)
      - [4.1.2.1. Docker `buildx`](#4121-docker-buildx)
  - [4.2. Building BSP](#42-building-bsp)
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
│         BSP Registry Configuration      │  # BSP Registry model definition
├─────────────────────────────────────────┤
│         KAS Configuration Files         │  # Build definitions
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

The table below is derived from the presets defined in `bsp-registry.yml`. A ✅ means a
ready-made preset exists and can be built directly with `bsp build <preset>-<release>`.

| Board \ Yocto  | wrynose | whinlatter | walnascar | styhead | scarthgap | mickledore | kirkstone |
| -------------- |:-------:|:----------:|:---------:|:-------:|:---------:|:----------:|:---------:|
| **RSB-3720** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **RSB-3720 4G** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **RSB-3720 6G** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **ROM-2620 (ED91)** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ROM-2820 (ED93)** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ROM-5720 (DB5901)** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ROM-5721 (DB5901)** | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ROM-5721 1G** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **ROM-5721 2G** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **ROM-5722 (DB2510)** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **AOM-5521 (DB2510)** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **AOM-5521 A1** | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **AOM-5521 A2** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **AOM-2521 B0** | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **ECU-150** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **NXP i.MX8ULP EVK** | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |

**Legend:**

* ✅ **Preset available**: a preset is shipped for this board and release
* ❌ **No preset**: not available for this release

### 2.1.1. Legacy and Product-Line Presets

A number of boards additionally carry older, product-line specific presets that pin a fixed NXP
BSP revision (`vendor_release`). These are kept for reproducing existing product builds and are
not carried forward to newer Yocto releases:

| Preset | Board | Release | NXP BSP revision |
|--------|-------|---------|------------------|
| `advantech-imx8mprsb3720a1-kirkstone` | RSB-3720 A1 | kirkstone | `imx-5.15.52-2.1.0` |
| `advantech-imx8mprsb3720a2-scarthgap` | RSB-3720 A2 | scarthgap | `imx-6.6.23-2.0.0` |
| `advantech-rsb3730-mickledore` | RSB-3730 | mickledore | `imx-6.1.22-2.0.0` |
| `advantech-rsb3730-2g-mickledore` | RSB-3730 2G | mickledore | `imx-6.1.22-2.0.0` |
| `advantech-rsb3730-4g-mickledore` | RSB-3730 4G | mickledore | `imx-6.1.22-2.0.0` |
| `advantech-rom2820-a1-mickledore` | ROM-2820 A1 | mickledore | `imx-6.1.22-2.0.0` |
| `advantech-rom5721-db5901-1g-mickledore` | ROM-5721 1G | mickledore | — |
| `advantech-rom5721-db5901-2g-mickledore` | ROM-5721 2G | mickledore | — |

These presets do not take a `-<release>` suffix, because the release is already part of the
preset name (for example `bsp build advantech-rsb3730-mickledore`).

### 2.1.2. Alternative View

| **Hardware**   | **Preset** | **Supported Releases** | **Status** | **Documentation** |
|----------------|------------|-------------------------|------------|-------------------|
| **RSB-3720**    | `modular-bsp-rsb3720` | scarthgap, styhead, walnascar, whinlatter, wrynose | 🟢 Stable | [Advantech RSB-3720 Product Page](https://www.advantech.com/en-us/products/5912096e-f242-4b17-993a-1acdcaada6f6/rsb-3720/mod_d2f1b0bc-650b-449a-8ef7-b65ce4f69949) · [User Manual](https://www.manualslib.com/manual/2293645/Advantech-Rsb-3720.html) |
| **RSB-3720 4G** | `modular-bsp-rsb3720-4g` | walnascar, whinlatter, wrynose | 🟢 Stable | *(Same as RSB-3720, variant-specific)* |
| **RSB-3720 6G** | `modular-bsp-rsb3720-6g` | walnascar, whinlatter, wrynose | 🟢 Stable | *(Same as RSB-3720, variant-specific)* |
| **RSB-3730**    | `advantech-rsb3730-mickledore` | mickledore | 🟡 Development | [Advantech RSB-3730 Product Page](https://www.advantech.com/en-eu/products/5912096e-f242-4b17-993a-1acdcaada6f6/rsb-3730/mod_5d7887e6-b7e3-427c-8729-b81ac7d89ccd) · [RSB-3730 User Manual (PDF)](https://advdownload.advantech.com/productfile/Downloadfile4/1-2HACYHA/RSB-3730_User_Manual_Eng_yocto%20Ed.1_FINAL.pdf) · [Yocto BSP Guide](https://ess-wiki.advantech.com.tw/view/Yocto_Linux_BSP_Ver.A_User_Guide_for_RSB-3730_series-Yocto_4.2) |
| **ROM-2620**    | `modular-bsp-rom2620-ed91` | scarthgap, styhead, walnascar, whinlatter, wrynose | 🟢 Stable | [Advantech ROM-2620 Product Page](https://www.advantech.com/en-eu/products/8fc6f753-ca1d-49f9-8676-10d53129570f/rom-2620/mod_294031c8-4a21-4b95-adf2-923c412ef761) |
| **ROM-2820**    | `modular-bsp-rom2820-ed93` | scarthgap, styhead, walnascar, whinlatter, wrynose | 🟢 Stable | [Advantech ROM-2820 Product Page](https://www.advantech.com/en-eu/products/8fc6f753-ca1d-49f9-8676-10d53129570f/rom-2820/mod_bb82922e-d3a2-49d7-80ff-dc57f400185e) |
| **ROM-5720**    | `modular-bsp-rom5720-db5901` | scarthgap, styhead, walnascar, whinlatter, wrynose | 🟢 Stable | [Advantech ROM-5720 Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5720/mod_4fbfe9fa-f5b2-4ba8-940e-e47585ad0fef) |
| **ROM-5721**    | `modular-bsp-rom5721-db5901` | scarthgap, styhead, walnascar | 🟢 Stable | [Advantech ROM-5721 Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5721/mod_271dbc68-878b-486d-85cf-30cc9f1f8f16) |
| **ROM-5721 1G** | `modular-bsp-rom5721-1g-db5901` | walnascar, whinlatter, wrynose | 🟢 Stable | *(Same as ROM-5721, variant-specific)* |
| **ROM-5721 2G** | `modular-bsp-rom5721-2g-db5901` | walnascar, whinlatter, wrynose | 🟢 Stable | *(Same as ROM-5721, variant-specific)* |
| **ROM-5722**    | `modular-bsp-rom5722-db2510` | scarthgap, styhead, walnascar, whinlatter, wrynose | 🟢 Stable | [Advantech ROM-5722 Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5722/mod_11aa0c77-868e-4014-8151-ac7a7a1c5c1b) |
| **AOM-5521 (DB2510)** | `modular-bsp-aom5521-db2510` | walnascar, whinlatter, wrynose | 🟢 Stable | [Advantech AOM-5521 Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/aom-5521/mod_75b36e99-ac3f-4801-8b2b-1706ade1025d) |
| **AOM-5521 A1** | `advantech-imx95aom5521a1` | scarthgap, walnascar | 🟡 Development | *(Same as above)* |
| **AOM-5521 A2** | `advantech-imx95aom5521a2` | walnascar | 🟡 Development | *(Same as above)* |
| **AOM-2521 B0** | `advantech-imx95aom2521b0` | walnascar, whinlatter | 🟡 Development | [Advantech AOM-2521 Product Page](https://www.advantech.com/en/products/som/aom-2521) |
| **ECU-150**     | `modular-bsp-ecu-150` | scarthgap, styhead, walnascar, whinlatter, wrynose | 🟡 Development | [Advantech ECU-150 Product page](https://www.advantech.com/en-us/products/7332cf9e-bf70-4a79-b0b6-fd8a2182cd72/ecu-150/mod_7af3b0b8-4e52-4ed2-bbdc-22ad3222def0) |
| **NXP i.MX8ULP EVK** | `nxp-imx8ulp-evk` | scarthgap, styhead, walnascar, whinlatter | 🟡 Development | [NXP i.MX 8ULP EVK](https://www.nxp.com/design/design-center/development-boards-and-designs/i-mx-evaluation-and-development-boards/i-mx-8ulp-evaluation-kit:i.MX8ULP-EVK) |

**Status Legend:**

* 🟢 **Stable**: Production-ready, fully tested and supported
* 🟡 **Development**: Under active development, may have limitations
* 🔴 **EOL**: End of Life, not recommended for new projects

#### 2.1.2.1. Yocto releases

This list below covers the most recent and commonly referenced Yocto releases:

* [Whinlatter (Yocto 5.3)](https://docs.yoctoproject.org/whinlatter/releases.html)  
* [Walnascar (Yocto 5.2)](https://docs.yoctoproject.org/walnascar/releases.html)  
* [Styhead (Yocto 5.1)](https://docs.yoctoproject.org/dev/migration-guides/release-5.1.html)  
* [Scarthgap (Yocto 5.0 LTS)](https://docs.yoctoproject.org/scarthgap/releases.html)  
* [Mickledore (Yocto 4.2)](https://docs.yoctoproject.org/mickledore/releases.html)  
* [Kirkstone (Yocto 4.0 LTS)](https://docs.yoctoproject.org/kirkstone/releases.html)  

The full overview of Yocto releases can be found here https://www.yoctoproject.org/development/releases/

### 2.1.3. OTA Update Support

The BSP registry includes Over-The-Air (OTA) update configurations for supported boards. OTA updates enable remote software updates without physical access to devices, critical for production deployments.

#### 2.1.3.1. Supported OTA Technologies

* **RAUC** (Robust Auto-Update Controller): A safe and reliable software update framework that supports atomic updates with rollback capabilities
* **SWUpdate**: A software update framework designed for embedded systems with support for multiple update strategies
* **OSTree**: An upgrade system for Linux-based operating systems that performs atomic upgrades of complete filesystem trees

#### 2.1.3.2. OTA Support Matrix

The registry distinguishes two levels of support:

* **🅿️ Preset** — a ready-made preset exists; build it directly with `bsp build <preset>-<release>`
* **➕ Composable** — the OTA feature is supported on the board and can be enabled by adding the
  feature to the preset's `features:` list in `bsp-registry.yml`, or by composing the feature
  fragment manually with KAS. No preset is shipped today.

| Board | RAUC | SWUpdate | OSTree | Supported Releases |
|-------|:----:|:--------:|:------:|-------------------|
| **RSB-3720** | 🅿️ | 🅿️ | 🅿️ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| **RSB-3720 4G** | ➕ | ➕ | ➕ | walnascar, whinlatter, wrynose |
| **RSB-3720 6G** | ➕ | ➕ | ➕ | walnascar, whinlatter, wrynose |
| **ROM-2620 (ED91)** | ➕ | ➕ | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| **ROM-2820 (ED93)** | ➕ | ➕ | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| **ROM-5720 (DB5901)** | ➕ | ➕ | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| **ROM-5721 1G** | ➕ | ➕ | ➕ | walnascar, whinlatter, wrynose |
| **ROM-5721 2G** | ➕ | ➕ | ➕ | walnascar, whinlatter, wrynose |
| **ROM-5722 (DB2510)** | ➕ | ➕ | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |

The three presets shipped today are `modular-bsp-rauc-rsb3720`, `modular-bsp-swupdate-rsb3720`
and `modular-bsp-ostree-rsb3720`, each available for scarthgap through wrynose. The `qcs6490-rb3gen2-vision-kit`
preset also enables the `ostree` feature.

The corresponding feature fragments live under `features/ota/`:

| Feature | Registry feature | Fragment |
|---------|------------------|----------|
| RAUC | `rauc` | `features/ota/rauc/rauc.yml` |
| SWUpdate | `swupdate` | `features/ota/swupdate/swupdate.yml` |
| OSTree | `ostree` | `features/ota/ostree/ostree.yml` |

OSTree additionally carries per-release compatibility fragments:
`features/ota/ostree/ostree-scarthgap.yml`, `features/ota/ostree/ostree-styhead.yml`,
`features/ota/ostree/ostree-walnascar.yml` and `features/ota/ostree/ostree-whinlatter.yml`.

#### 2.1.3.3. Building Images with OTA Support

To build a BSP image with OTA support, use the `bsp` command:

```bash
# List all available OTA configurations
bsp list | grep -E 'rauc|swupdate|ostree'

# Build RSB-3720 with RAUC support
bsp build modular-bsp-rauc-rsb3720-walnascar

# Build RSB-3720 with SWUpdate support
bsp build modular-bsp-swupdate-rsb3720-styhead

# Build RSB-3720 with OSTree support
bsp build modular-bsp-ostree-rsb3720-scarthgap
```

### 2.1.4. Secure Boot Support

NXP-based Advantech Europe boards support cryptographic boot-image signing via
**HAB** (High Assurance Boot, i.MX8 family) and **AHAB** (Advanced High Assurance Boot,
i.MX9 / i.MX95 family).

📖 **See [docs/secure-boot.md](docs/secure-boot.md)** for full instructions including:
- Obtaining and configuring the NXP Code Signing Tool (CST)
- Generating SRK keys and certificates
- Required environment variables
- Board fusing / provisioning procedures
- CI / Azure Pipelines integration

#### 2.1.4.1. Secure Boot Support Matrix

As with OTA, the registry distinguishes a shipped preset from a supported-but-composable
configuration:

* **🅿️ Preset** — a ready-made secure-boot preset exists
* **➕ Composable** — the board supports signing; enable it by adding the `secure-boot` feature to
  the preset's `features:` list, or by composing `features/secure-boot/secure-boot.yml` with KAS

| Board              | SoC Family | Secure Boot | Support | Yocto Releases                        |
|--------------------|-----------|-------------|:-------:|---------------------------------------|
| ROM-2620 (ed91)    | i.MX8     | HAB         | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| ROM-5720 (db5901)  | i.MX8     | HAB         | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| ROM-5721 (db5901)  | i.MX8     | HAB         | ➕ | scarthgap, styhead, walnascar         |
| ROM-5721 1G        | i.MX8     | HAB         | ➕ | walnascar, whinlatter, wrynose        |
| ROM-5721 2G        | i.MX8     | HAB         | 🅿️ | walnascar (preset), whinlatter, wrynose |
| ROM-5722 (db2510)  | i.MX8     | HAB         | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| RSB-3720           | i.MX8     | HAB         | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| RSB-3720 4G        | i.MX8     | HAB         | ➕ | walnascar, whinlatter, wrynose        |
| RSB-3720 6G        | i.MX8     | HAB         | ➕ | walnascar, whinlatter, wrynose        |
| ROM-2820 (ed93)    | i.MX9     | AHAB        | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| AOM-5521 (db2510)  | i.MX95    | AHAB        | ➕ | walnascar, whinlatter, wrynose        |

The only secure-boot preset shipped today is `modular-bsp-rom5721-2g-db5901-secureboot`
(walnascar). The listed releases are those for which the board has a preset that the
`secure-boot` feature can be added to.

#### 2.1.4.2. Building Images with Secure Boot

```bash
# Export signing environment variables before building
export CST_TOOL_PATH=/opt/cst

# Build a signed image (example: ROM-5721, Walnascar release)
bsp build  modular-bsp-rom5721-2g-db5901-secureboot-walnascar
```

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
* Raspberry Pi OS (Bookworm, Bullseye) — 🟡 preview, no preset yet

Of these, the registry currently exposes `debian-trixie`, `ubuntu-jammy` and `ubuntu-noble` as
Isar releases. The remaining fragments are available for manual KAS composition.

### 2.2.2. Isar Hardware Support

The registry includes Isar-based BSP configurations for the following targets:

| Hardware | Distribution | Status | BSP Name |
|----------|-------------|--------|----------|
| **QEMU ARM64** | Debian Trixie | ✅ Ready | `isar-qemuarm64-debian-trixie` |
| **QEMU x86-64** | Debian Trixie | ✅ Ready | `isar-qemuamd64-debian-trixie` |
| **QEMU x86-64** | Ubuntu Noble | ✅ Ready | `isar-qemuamd64-ubuntu-noble` |
| **QEMU x86-64** | Ubuntu Jammy | ✅ Ready | `isar-qemuamd64-ubuntu-jammy` |

**Status Legend:**
* ✅ **Ready**: Functional and available for testing/development

All Isar presets currently target QEMU. Real hardware can be added through the
[meta-isar-modular-bsp-nxp](https://github.com/Advantech-EECC/meta-isar-modular-bsp-nxp) layer by
registering a device and a preset in `bsp-registry.yml`.

### 2.2.3. Building Isar BSPs

Isar builds require privileged container execution to support Debian package management operations. The registry handles this automatically when using Isar-enabled containers.

**Example: Build QEMU ARM64 with Debian Trixie**
```bash
bsp build isar-qemuarm64-debian-trixie
```

**Example: Build QEMU x86-64 with Ubuntu Noble**
```bash
bsp build isar-qemuamd64-ubuntu-noble
```

### 2.2.4. Isar Container Configuration

Isar builds use the `isar-debian-13` container, which is automatically configured with:
* Privileged mode for package management operations
* Based on official kas-isar container images
* KAS version 5.2
* Debian Trixie base distribution
* Extra runtime arguments for TUN/TAP networking, required to run the built image under QEMU

The container definition in `bsp-registry.yml`:
```yaml
- isar-debian-13:
    file: Dockerfile.isar.debian
    image: "advantech/bsp-registry/isar/debian-13/kas:5.2"
    privileged: true
    runtime_args: "-p 2222:2222 --device=/dev/net/tun --cap-add=NET_ADMIN"
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

## 2.3. MediaTek Boards Compatibility Matrix [preview]

The BSP registry supports MediaTek-based boards through the **MediaTek AIoT Rity** BSP stack. The
current integration targets the Yocto **Scarthgap** release and uses the upstream Rity v25.0 layer
set. For detailed configuration, see the [MediaTek vendor README](vendors/mediatek/README.md) and the
[Advantech MediaTek overlay README](vendors/advantech-europe/mediatek/README.md).

| Board \ Yocto  | scarthgap | Status        |
| -------------- | :-------: | ------------- |
| **Genio 1200 EVK** | 🅿️    | 🟡 Development |
| **RSB-3810**   |     🅿️     | 🟡 Development |

**Status Legend:**

* 🟢 **Stable**: Production-ready, fully tested and supported
* 🟡 **Development**: Under active development, may have limitations
* 🅿️ **Preset available**: a preset is shipped for this board and release

| **Hardware**         | **Preset** | **Supported Releases** | **Status**       | **Documentation** |
|----------------------|------------|------------------------|------------------|-------------------|
| **Genio 1200 EVK**   | `mediatek-genio-1200-evk` | scarthgap | 🟡 Development   | [MediaTek Genio 1200 EVK](https://mediatek.gitlab.io/aiot/doc/aiot-dev-guide/master/hw/g1200-evk.html) |
| **RSB-3810**         | `modular-bsp-rsb3810` | scarthgap | 🟡 Development   | [Advantech RSB-3810](https://ess-wiki.advantech.com.tw/view/AIM-Linux/RSB-3810) |

### 2.3.1. Building MediaTek BSPs

```bash
# List available MediaTek BSPs
bsp list | grep -i mediatek

# Build MediaTek Genio 1200 EVK (scarthgap)
bsp build mediatek-genio-1200-evk-scarthgap

# Build Advantech RSB-3810 (scarthgap)
bsp build modular-bsp-rsb3810-scarthgap
```

---

## 2.4. Qualcomm Boards Compatibility Matrix

The BSP registry supports Qualcomm-based boards through the **Qualcomm Linux (QLI)** BSP stack.
The current integration targets the Yocto **Scarthgap** release and uses the QLI v1.5 Ver.1.1 layer
set. For detailed configuration, see the [Qualcomm vendor README](vendors/qualcomm/README.md) and
the [Advantech Qualcomm overlay README](vendors/advantech-europe/qualcomm/README.md).

| Board \ Yocto         | scarthgap | Status        |
| --------------------- | :-------: | ------------- |
| **QCS6490 RB3gen2**   |     🅿️     | 🟡 Development |
| **AOM-2721**          |     🔍     | 🔍 Preview     |

**Status Legend:**

* 🟢 **Stable**: Production-ready, fully tested and supported
* 🟡 **Development**: Under active development, may have limitations
* 🔍 **Preview**: Device and machine config exist in the registry, but no preset is wired up yet,
  so the board does not appear in `bsp list` and must be composed manually with KAS

| **Hardware**          | **Preset** | **Supported Releases** | **Status**     | **Documentation** |
|-----------------------|------------|------------------------|----------------|-------------------|
| **QCS6490 RB3gen2**   | `qcs6490-rb3gen2-vision-kit` | scarthgap | 🟡 Development | [Qualcomm RB3gen2 Vision Kit](https://www.qualcomm.com/developer/hardware/rb3-gen-2-development-kit) |
| **AOM-2721**          | *(none — `aom2721` device only)* | — | 🔍 Preview | [Advantech AOM-2721 Product Page](https://www.advantech.com/en/products/som/aom-2721) |

### 2.4.1. Building Qualcomm BSPs

```bash
# List available Qualcomm BSPs
bsp list | grep -i qcs

# Build Qualcomm QCS6490 RB3gen2 EVK (scarthgap)
bsp build qcs6490-rb3gen2-vision-kit-scarthgap
```
---

## 2.5. NVIDIA Jetson Boards Compatibility Matrix

The BSP registry supports **NVIDIA Jetson** platforms through the community
**[OE4T](https://github.com/OE4T)** layers (`meta-tegra`, `meta-tegra-community`) and the full
**`tegra-demo-distro`** distribution (`tegrademo`). For detailed configuration, see the
[NVIDIA vendor README](vendors/nvidia/README.md).

Orin (JetPack 6 / L4T r36.x) is supported across all Yocto releases from scarthgap to wrynose.
Xavier (JetPack 5 / L4T r35.x) is available on **scarthgap only**, because NVIDIA's Xavier
support lives on the OE4T `*-l4t-r35.x` branches, which only exist for kirkstone and scarthgap.

| Board \ Yocto              | scarthgap | styhead | walnascar | whinlatter | wrynose | Status        |
| -------------------------- | :-------: | :-----: | :-------: | :--------: | :-----: | ------------- |
| **Jetson AGX Orin**        |     🅿️     |    🅿️    |     🅿️     |     🅿️      |    🅿️    | 🟡 Development |
| **Jetson Orin Nano**       |     🅿️     |    🅿️    |     🅿️     |     🅿️      |    🅿️    | 🟡 Development |
| **Jetson Orin Nano NVMe**  |     🅿️     |    🅿️    |     🅿️     |     🅿️      |    🅿️    | 🟡 Development |
| **Jetson AGX Xavier**      |     🅿️     |    ❌    |     ❌     |     ❌      |    ❌    | 🟡 Development |
| **Jetson Xavier NX**       |     🅿️     |    ❌    |     ❌     |     ❌      |    ❌    | 🟡 Development |

**Status Legend:**

* 🟢 **Stable**: Production-ready, fully tested and supported
* 🟡 **Development**: Under active development, may have limitations
* 🅿️ **Preset available**: a preset is shipped for this board and release
* ❌ **Unsupported**: Not available for this Yocto release

| **Hardware**              | **Preset** | **Supported Releases**                             | **JetPack / L4T**     | **Status**     | **Documentation** |
|---------------------------|------------|----------------------------------------------------|-----------------------|----------------|-------------------|
| **Jetson AGX Orin**       | `jetson-agx-orin-devkit` | scarthgap, styhead, walnascar, whinlatter, wrynose | JetPack 6 / L4T r36.x | 🟡 Development | [NVIDIA Jetson Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) |
| **Jetson Orin Nano**      | `jetson-orin-nano-devkit` | scarthgap, styhead, walnascar, whinlatter, wrynose | JetPack 6 / L4T r36.x | 🟡 Development | [NVIDIA Jetson Orin Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) |
| **Jetson Orin Nano NVMe** | `jetson-orin-nano-devkit-nvme` | scarthgap, styhead, walnascar, whinlatter, wrynose | JetPack 6 / L4T r36.x | 🟡 Development | *(Same as Jetson Orin Nano, NVMe boot variant)* |
| **Jetson AGX Xavier**     | `jetson-agx-xavier-devkit` | scarthgap                                          | JetPack 5 / L4T r35.x | 🟡 Development | [NVIDIA Jetson Xavier](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-xavier/) |
| **Jetson Xavier NX**      | `jetson-xavier-nx-devkit` | scarthgap                                          | JetPack 5 / L4T r35.x | 🟡 Development | [NVIDIA Jetson Xavier NX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-xavier-nx/) |

### 2.5.1. Building NVIDIA Jetson BSPs

```bash
# List available NVIDIA Jetson BSPs
bsp list | grep -i jetson

# Build Jetson AGX Orin (JetPack 6, scarthgap)
bsp build jetson-agx-orin-devkit-scarthgap

# Build Jetson AGX Xavier (JetPack 5, scarthgap only)
bsp build jetson-agx-xavier-devkit-scarthgap

# Build Jetson Orin Nano on the latest release (wrynose)
bsp build jetson-orin-nano-devkit-wrynose
```
---

## 2.6. QEMU and Reference BSPs

In addition to hardware BSPs, the registry ships emulated QEMU targets. They require no hardware
and are the fastest way to validate the toolchain, a feature fragment, or a new Yocto release.

| Preset | Device | Framework | Releases | Notes |
|--------|--------|-----------|----------|-------|
| `poky-qemux86-64` | `qemux86-64` | Yocto | kirkstone, nanbield, mickledore, scarthgap, styhead, walnascar, whinlatter, wrynose, master | Poky reference build; widest release coverage in the registry |
| `poky-qemuarm64` | `qemuarm64` | Yocto | kirkstone, nanbield, mickledore, scarthgap, styhead, walnascar, whinlatter | Poky reference build for ARM64 |
| `poky-qemuarm-scarthgap` | `qemuarm` | Yocto | scarthgap | Poky reference build for ARM 32-bit |
| `poky-harden-qemux86-64-scarthgap` | `qemux86-64` | Yocto | scarthgap | Hardened Poky distro (`poky-harden`) with the `security` feature |
| `poky-qemux86-64-ros2` | `qemux86-64` | Yocto | ros2-humble-scarthgap | ROS 2 Humble on Scarthgap |
| `isar-qemuamd64` | `qemuamd64` | Isar | ubuntu-noble, ubuntu-jammy, debian-trixie | Debian-based build, see [§2.2](#22-isar-build-system-support) |
| `isar-qemuarm64` | `qemuarm64` | Isar | debian-trixie | Debian-based build, see [§2.2](#22-isar-build-system-support) |

### 2.6.1. Building QEMU BSPs

```bash
# List the emulated targets
bsp list | grep -E 'qemu|poky'

# Poky reference build on the latest release
bsp build poky-qemux86-64-wrynose

# Hardened Poky (the release is already part of the preset name)
bsp build poky-harden-qemux86-64-scarthgap

# ROS 2 Humble on Scarthgap
bsp build poky-qemux86-64-ros2-ros2-humble-scarthgap
```

Isar-built images can be booted with the helper script `isar/scripts/isar-runqemu.sh`; see the
[Isar scripts README](isar/scripts/README.md).

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
```

## 3.4. Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List all available BSPs | `bsp list` |
| `tree` | Show all available BSPs as a tree | `bsp tree` |
| `build <bsp_name>` | Build a specific BSP | `bsp build imx8mpevk` |
| `build <bsp_name> --checkout` | Checkout and validate BSP configuration without building (fast) | `bsp build imx8mpevk --checkout` |
| `shell <bsp_name>` | Enter interactive shell | `bsp shell imx8mpevk` |
| `export <bsp_name>` | Export KAS configuration | `bsp export imx8mpevk` |
| `containers` | List available containers | `bsp containers` |

### 3.4.1. Checkout and Validation

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
bsp build modular-bsp-rsb3720-6g-walnascar --checkout
```

---

# 4. HowTo Assemble BSPs

This chapter explains how to assemble modular BSPs using KAS configuration files. It provides step‑by‑step instructions for setting up prerequisites, selecting the right configuration, and running builds to generate reproducible BSP images tailored to specific hardware platforms.

## 4.1. Host System dependencies

The host system must provide essential tools and libraries required for building BSPs, including compilers, version control systems, and scripting environments. Ensuring these dependencies are installed and up to date guarantees a stable build process and consistent results across different development environments.

**Host system initial setup must include:**

* Python 3.x
  * Including python virtual environment module
* `pip` package manager is available
* Docker
* Git

The build have been tested on the following host systems: `Ubuntu 22.04`, `Ubuntu 24.04`

### 4.1.1. Setup Python virtual environment

It is recommended to install python based tools and packages in a separate python virtual envronment, which could be created
using python virtualenv package.

```bash
python3 -m venv venv
```

To activate virtual environment use following command:

```bash
source venv/bin/activate
```

#### 4.1.1.1. Advanced Tools for Managing Multiple Python Environments

While venv and virtualenv cover most basic needs, advanced tools provide additional functionality for dependency management, reproducibility, and handling multiple Python versions.

* [pipenv](https://pipenv.pypa.io/en/latest/)
* [pyenv](https://github.com/pyenv/pyenv)
* [conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html) 

#### 4.1.1.2. Install Python packages dependencies

Install the `bsp-registry-tools` package to get the `bsp` CLI tool:

```bash
pip3 install bsp-registry-tools
```

### 4.1.2. Setting up Docker engine

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

## 4.3. HowTo build a BSP using KAS

To assemble BSP images using KAS tool following commands can be used

```bash
# activate python virtual environment
source venv/bin/activate

# add proper KAS configuration variables to your environment
export KAS_CONTAINER_ENGINE=docker
export KAS_CONTAINER_IMAGE=advantech/bsp-registry/ubuntu:22.04
export GITCONFIG_FILE=$HOME/.gitconfig
export DL_DIR=$HOME/cache/downloads/
export SSTATE_DIR=$HOME/cache/sstate/
 

# run the build
# kas build <path-to-kas-yaml-file>
kas build kas-configuration.yaml
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
kas-container build kas-configuration.yaml
```

### 4.3.2. Bitbake development shell

Using pure `kas` it is possible to enter bitbake shell via command:

```bash
kas shell kas-configuration.yaml
```

or in a `docker` container using following command:

```bash
kas-container shell kas-configuration.yaml
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

# 5. Advanced Topics

This chapter provides overview of advanced topics working with KAS build configurations.

## 5.1. Export KAS configuration

kas tool can dump final configuration in standart output with `kas dump` command

```bash
kas dump kas-configuration-file.yaml > final.yaml
```

For details check https://kas.readthedocs.io/en/latest/userguide/plugins.html#module-kas.plugins.dump

`final.yaml` would contain all the included `yaml` configuration files and can be reused later.

## 5.2. Lock KAS configuration

Similar to `kas dump` there is a `kas lock` command, it would generate a yaml file with all layer revisions. 
For datailed overview check official kas documentation https://kas.readthedocs.io/en/latest/userguide/plugins.html#module-kas.plugins.lock

## 5.3. Reusing BSP Registry configurations

It is possible to include BSP registry YAML configurations in your images (provided your project uses kas to assemble OS images). An example KAS configuration 

To extend an existing BSP with a custom Yocto layer create a following kas config:

```yaml
header:
  version: 19
  includes:
    - repo: bsp-registry
      file: adv-mbsp-oenxp-whinlatter-rsb3720-6g.yaml

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

# 6. Patches

The BSP registry uses patches to fix build issues, add hardware support, and ensure compatibility across different Yocto releases. Patches are organized by vendor and Yocto version to maintain stability and reproducibility.

The repository contains **24 patches** organized into:

* **NXP vendor patches** (20 patches): Address build failures, dependency corrections, and hardware-specific configurations for NXP i.MX platforms across Kirkstone, Mickledore, Scarthgap, Styhead, Walnascar, Whinlatter and Wrynose
* **OTA feature patches** (2 patches): Enable OSTree-based over-the-air updates for the Styhead and Walnascar releases
* **MediaTek vendor patches** (2 patches): Fix recipe and git checkout issues specific to the MediaTek Rity Scarthgap BSP

All patches are documented with:

* Purpose and rationale
* Affected layers and recipes
* Yocto release compatibility

For detailed information about each patch, including what they fix and which components they affect, see the **[Patches Documentation](patches/README.md)**.

---

# 7. Links

* [Building Modular BSP using Repo Tool](BUILDING_WITH_REPO.md) - Alternative build method using Google's repo tool
* [KAS Container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html)
* [KAS](https://kas.readthedocs.io/en/latest/intro.html)
