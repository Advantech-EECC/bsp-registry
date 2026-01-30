# Advantech NXP i.MX BSP Configurations

This directory contains Advantech-customized Board Support Package (BSP) configurations for NXP i.MX-based Advantech embedded computing platforms. These configurations extend the base NXP BSP with Advantech-specific hardware support, drivers, and features.

## Overview

Advantech is a global leader in embedded computing platforms. This BSP registry provides configurations for Advantech's industrial-grade boards built on NXP i.MX processors, including COM Express modules, single-board computers, and specialized IoT platforms.

```
Advantech BSP Structure
├── NXP i.MX Configurations
│   ├── Base Releases (extends vendors/nxp/*)
│   │   ├── Kirkstone (Yocto 4.0 LTS)
│   │   │   ├── bsp-imx-5.15.52-2.1.0-kirkstone.yml
│   │   │   └── imx-5.15.71-2.2.2-kirkstone.yml
│   │   ├── Mickledore (Yocto 4.2)
│   │   │   └── bsp-imx-6.1.22-2.0.0-mickledore.yml
│   │   ├── Scarthgap (Yocto 5.0 LTS)
│   │   │   ├── bsp-imx-6.6.23-2.0.0-scarthgap.yml
│   │   │   ├── bsp-imx-6.6.36-2.1.0-scarthgap.yml
│   │   │   └── imx-6.6.52-2.2.0-scarthgap.yml
│   │   ├── Styhead (Yocto 5.1)
│   │   │   └── imx-6.12.3-1.0.0-styhead.yml
│   │   └── Walnascar (Yocto 5.2)
│   │       ├── bsp-imx-6.12.20-2.0.0-walnascar.yml
│   │       ├── imx-6.12.20-2.0.0-walnascar.yml
│   │       ├── imx-6.12.34-2.1.0-walnascar.yml
│   │       └── imx-6.12.49-2.2.0-walnascar.yml
│   └── Machine Configurations
│       ├── i.MX 8 Platforms (imx8/)
│       │   ├── rsb3720.yml           # RSB-3720 SBC
│       │   ├── rsb3720-4g.yml        # RSB-3720 4GB variant
│       │   ├── rsb3720-6g.yml        # RSB-3720 6GB variant
│       │   ├── rom2620-ed91.yml      # ROM-2620 COM Express
│       │   ├── rom5720-db5901.yml    # ROM-5720 COM Express
│       │   ├── rom5721-db5901.yml    # ROM-5721 COM Express
│       │   ├── rom5721-1g-db5901.yml # ROM-5721 1GB variant
│       │   ├── rom5721-2g-db5901.yml # ROM-5721 2GB variant
│       │   └── rom5722-db2510.yml    # ROM-5722 COM Express
│       └── i.MX 9 Platforms (imx9/)
│           └── rom2820-ed93.yml      # ROM-2820 COM Express
└── Advantech Layer
    └── meta-eecc-nxp               # Advantech-specific recipes
```

## Supported Hardware

### i.MX 8 Based Platforms

| Board Model | Processor | Form Factor | RAM Options | Status | Product Link |
|-------------|-----------|-------------|-------------|--------|--------------|
| **RSB-3720** | i.MX 8M Plus | 3.5" SBC | 2GB/4GB/6GB | 🟢 Stable | [Product Page](https://www.advantech.com/en-us/products/5912096e-f242-4b17-993a-1acdcaada6f6/rsb-3720/mod_d2f1b0bc-650b-449a-8ef7-b65ce4f69949) |
| **RSB-3720 4G** | i.MX 8M Plus | 3.5" SBC | 4GB | 🟢 Stable | (Variant) |
| **RSB-3720 6G** | i.MX 8M Plus | 3.5" SBC | 6GB | 🟢 Stable | (Variant) |
| **ROM-2620** | i.MX 8M Mini | COM Express Compact | 2GB | 🟢 Stable | [Product Page](https://www.advantech.com/en-eu/products/8fc6f753-ca1d-49f9-8676-10d53129570f/rom-2620/mod_294031c8-4a21-4b95-adf2-923c412ef761) |
| **ROM-5720** | i.MX 8M Plus | COM Express Compact | 4GB/8GB | 🟢 Stable | [Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5720/mod_4fbfe9fa-f5b2-4ba8-940e-e47585ad0fef) |
| **ROM-5721** | i.MX 8M Plus | COM Express Compact | 1GB/2GB/4GB | 🟢 Stable | [Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5721/mod_271dbc68-878b-486d-85cf-30cc9f1f8f16) |
| **ROM-5722** | i.MX 8M Plus | COM Express Compact | 4GB | 🟢 Stable | [Product Page](https://www.advantech.com/en-eu/products/77b59009-31a9-4751-bee1-45827a844421/rom-5722/mod_11aa0c77-868e-4014-8151-ac7a7a1c5c1b) |

### i.MX 9 Based Platforms

| Board Model | Processor | Form Factor | RAM Options | Status | Product Link |
|-------------|-----------|-------------|-------------|--------|--------------|
| **ROM-2820** | i.MX 93 | COM Express Compact | 2GB | 🟢 Stable | [Product Page](https://www.advantech.com/en-eu/products/8fc6f753-ca1d-49f9-8676-10d53129570f/rom-2820/mod_bb82922e-d3a2-49d7-80ff-dc57f400185e) |

**Status Legend:**
- 🟢 **Stable**: Production-ready, fully tested and supported
- 🟡 **Development**: Under active development, may have limitations
- 🔴 **EOL**: End of Life, not recommended for new projects

## Release Information

### Yocto Release Support Matrix

| Board | Walnascar | Styhead | Scarthgap | Mickledore | Kirkstone |
|-------|:---------:|:-------:|:---------:|:----------:|:---------:|
| **RSB-3720** | ✅ | ✅ | ✅ | ❌ | 🟡 |
| **RSB-3720 4G** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **RSB-3720 6G** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **ROM-2620** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ROM-5720** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ROM-5721** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ROM-5721 1G** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **ROM-5721 2G** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **ROM-5722** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **ROM-2820** | ✅ | ✅ | ✅ | ❌ | ❌ |

### Available Releases

#### Kirkstone (Yocto 4.0 LTS)
- **bsp-imx-5.15.52-2.1.0-kirkstone** - Advantech BSP with Linux 5.15.52
- **imx-5.15.71-2.2.2-kirkstone** - Advantech BSP with Linux 5.15.71

#### Mickledore (Yocto 4.2)
- **bsp-imx-6.1.22-2.0.0-mickledore** - Advantech BSP with Linux 6.1.22

#### Scarthgap (Yocto 5.0 LTS)
- **bsp-imx-6.6.23-2.0.0-scarthgap** - Advantech BSP with Linux 6.6.23
- **bsp-imx-6.6.36-2.1.0-scarthgap** - Advantech BSP with Linux 6.6.36
- **imx-6.6.52-2.2.0-scarthgap** - Advantech BSP with Linux 6.6.52

#### Styhead (Yocto 5.1)
- **imx-6.12.3-1.0.0-styhead** - Advantech BSP with Linux 6.12.3

#### Walnascar (Yocto 5.2)
- **bsp-imx-6.12.20-2.0.0-walnascar** - Advantech BSP with Linux 6.12.20
- **imx-6.12.20-2.0.0-walnascar** - Advantech BSP with Linux 6.12.20
- **imx-6.12.34-2.1.0-walnascar** - Advantech BSP with Linux 6.12.34
- **imx-6.12.49-2.2.0-walnascar** - Advantech BSP with Linux 6.12.49

## Architecture

### Advantech BSP Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Advantech Platform Image                   │
│         (Custom images with Advantech features)         │
├─────────────────────────────────────────────────────────┤
│             Advantech BSP Layers                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │ meta-eecc-nxp (Advantech layer)                  │   │
│  │  ├─ Board-specific configurations                │   │
│  │  ├─ Hardware enablement recipes                  │   │
│  │  ├─ Advantech utilities and tools                │   │
│  │  ├─ Custom device drivers                        │   │
│  │  └─ Industry-specific features                   │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                  NXP i.MX BSP                           │
│           (Base BSP from vendors/nxp/*)                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │ meta-imx, meta-freescale                         │   │
│  │ meta-nxp-connectivity, meta-nxp-demo-experience  │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│              OpenEmbedded & Yocto                       │
│         (Core build system and recipes)                 │
└─────────────────────────────────────────────────────────┘
```

### Relationship to NXP BSP

```
Dependency Flow
│
NXP Base BSP (vendors/nxp/imx-*.yml)
│
├─ Defines: Core NXP layer commits
├─ Provides: Reference machine support
└─ Includes: meta-imx, meta-freescale, etc.
   │
   └─> Advantech BSP (vendors/advantech/nxp/*)
       │
       ├─ Inherits: All NXP BSP configurations
       ├─ Adds: meta-eecc-nxp layer
       ├─ Customizes: Machine configurations
       └─ Extends: Board-specific features
```

## OTA Update Support

Advantech boards support Over-The-Air (OTA) updates using multiple technologies:

### Supported OTA Technologies

- **RAUC** - Robust Auto-Update Controller with atomic updates
- **SWUpdate** - Flexible software update framework
- **OSTree** - Git-like upgrade system for complete filesystem trees (⚠️ Under Development)

### OTA Support Matrix

| Board | RAUC | SWUpdate | OSTree | Supported Releases |
|-------|:----:|:--------:|:------:|-------------------|
| **RSB-3720** | ✅ | ✅ | 🟡 | walnascar, styhead, scarthgap |
| **RSB-3720-4G** | ✅ | ✅ | ❌ | walnascar |
| **RSB-3720-6G** | ✅ | ✅ | ❌ | walnascar |
| **ROM-2620** | ✅ | ✅ | 🟡 | walnascar, styhead, scarthgap |
| **ROM-2820** | ✅ | ✅ | 🟡 | walnascar, styhead, scarthgap |
| **ROM-5720** | ✅ | ✅ | 🟡 | walnascar, styhead, scarthgap |
| **ROM-5721** | ✅ | ✅ | 🟡 | walnascar, styhead, scarthgap |
| **ROM-5721-1G** | ✅ | ✅ | 🟡 | walnascar |
| **ROM-5721-2G** | ✅ | ✅ | 🟡 | walnascar |
| **ROM-5722** | ✅ | ✅ | 🟡 | walnascar, styhead, scarthgap |

**Legend:**
- ✅ Stable and production-ready
- 🟡 Under development
- ❌ Not supported

## Usage

### Building Standard BSP Images

```bash
# Build standard BSP for RSB-3720 with Walnascar
just bsp rsb3720 walnascar

# Build standard BSP for ROM-5720 with Scarthgap LTS
just bsp rom5720-db5901 scarthgap

# Build for ROM-2820 (i.MX 93) with Styhead
just bsp rom2820-ed93 styhead
```

### Building Modular BSP Images

Modular BSP provides enhanced flexibility with feature composition:

```bash
# Build modular BSP for RSB-3720
just mbsp rsb3720 walnascar

# Build modular BSP for ROM-5722
just mbsp rom5722-db2510 scarthgap
```

### Building with OTA Support

```bash
# Build with RAUC OTA support
just ota-mbsp rsb3720 rauc walnascar

# Build with SWUpdate OTA support
just ota-mbsp rom5720-db5901 swupdate scarthgap

# Build with OSTree OTA support (⚠️ Under Development)
just ota-mbsp rom5722-db2510 ostree styhead
```

## Advantech-Specific Features

The `meta-eecc-nxp` layer provides:

### Hardware Enablement
- Board-specific device tree configurations
- Custom peripheral drivers
- Power management optimizations
- Thermal management configurations

### Industrial Features
- Extended temperature range support
- Watchdog timer configurations
- GPIO and industrial I/O support
- CAN bus and industrial protocol support

### Security Features
- Secure boot configurations
- Hardware security module (HSM) support
- TPM (Trusted Platform Module) integration
- Encrypted storage support

### Customization
- Advantech-specific utilities and tools
- Board diagnostics and testing utilities
- Manufacturing and provisioning tools
- Custom recovery mechanisms

## Configuration Files

### BSP Configuration Files

Advantech BSP configuration files extend NXP base configurations:

```yaml
# Example: vendors/advantech/nxp/imx-6.12.49-2.2.0-walnascar.yml
header:
  includes:
    - vendors/nxp/imx-6.12.49-2.2.0-walnascar.yml  # Inherit NXP BSP

repos:
  meta-eecc-nxp:  # Add Advantech layer
    url: "https://github.com/Advantech-EECC/meta-eecc-nxp.git"
    branch: "walnascar"
    # Advantech-specific configurations
```

### Machine Configuration Files

Machine files define Advantech board-specific settings:

```yaml
# Example: vendors/advantech/nxp/machine/imx8/rsb3720.yml
header:
  version: 14

machine: "rsb3720"

local_conf_header:
  ostree-rsb3720: |
    SOTA_MACHINE:rsb3720 ?= "rsb3720"
```

## Technical Specifications

### RSB-3720 Series (i.MX 8M Plus)
- **CPU**: Quad-core Arm Cortex-A53 @ 1.8 GHz
- **GPU**: Vivante GC7000UL
- **NPU**: 2.3 TOPS Machine Learning accelerator
- **Display**: LVDS, HDMI 2.0, MIPI-DSI
- **Networking**: Dual GbE, optional Wi-Fi/BT
- **Storage**: eMMC, SD card, SATA
- **Industrial**: -20°C to 60°C operating temperature

### ROM Series (COM Express Compact)
- **Form Factor**: COM Express Compact Type 6
- **Processors**: i.MX 8M Mini, i.MX 8M Plus, i.MX 93
- **Industrial Grade**: Wide temperature range support
- **Long Lifecycle**: 10+ years product availability
- **Customization**: ODM services available

## Resources

### Advantech Resources
- [Advantech Embedded Computing](https://www.advantech.com/products/embedded-boards)
- [Advantech BSP Wiki](https://ess-wiki.advantech.com.tw/)
- [Advantech GitHub](https://github.com/Advantech-EECC)
- [Technical Support](https://www.advantech.com/support)

### NXP Resources
- [NXP i.MX Software and Tools](https://www.nxp.com/design/software/embedded-software/i-mx-software:IMX-SW)
- [NXP i.MX Yocto Project User's Guide](https://www.nxp.com/docs/en/user-guide/IMX_YOCTO_PROJECT_USERS_GUIDE.pdf)

### Yocto Project
- [Yocto Project Documentation](https://docs.yoctoproject.org/)
- [Yocto Release Information](https://www.yoctoproject.org/development/releases/)

## Support

For Advantech-specific BSP support:
- **Email**: Contact your Advantech sales representative
- **GitHub Issues**: [Advantech-EECC/bsp-registry](https://github.com/Advantech-EECC/bsp-registry/issues)
- **Documentation**: [BSP Registry Main README](../../README.md)

## License

The configuration files in this directory are provided under the terms specified in the repository's LICENSE file. Advantech BSP configurations may include proprietary software requiring additional license agreements. See individual layer repositories for specific licensing information.
