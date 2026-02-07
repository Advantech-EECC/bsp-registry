# Vendor BSP Configurations

This directory contains vendor-specific Board Support Package (BSP) configurations for various hardware platforms. Each vendor subdirectory provides customized configurations, machine definitions, and layer integrations specific to their hardware ecosystem.

## Table of Contents

1. [Overview](#1-overview)
2. [Directory Structure](#2-directory-structure)
3. [Supported Vendors](#3-supported-vendors)
   - 3.1 [NXP](#31-nxp)
   - 3.2 [Advantech](#32-advantech)
4. [Configuration Organization](#4-configuration-organization)
   - 4.1 [Vendor Configuration Files](#41-vendor-configuration-files)
   - 4.2 [Machine Configurations](#42-machine-configurations)
   - 4.3 [Yocto Release Support](#43-yocto-release-support)
5. [Adding a New Vendor](#5-adding-a-new-vendor)
6. [Usage](#6-usage)
   - 6.1 [Building Vendor BSPs](#61-building-vendor-bsps)
   - 6.2 [Configuration Inheritance](#62-configuration-inheritance)
7. [Resources](#7-resources)
8. [License](#8-license)

---

## 1. Overview

The vendors directory organizes BSP configurations by silicon vendor and platform manufacturer. This structure enables:

- **Hardware-specific optimizations**: Vendor configurations include optimized settings for specific processors and platforms
- **Layer management**: Each vendor manages their own Yocto meta-layers and dependencies
- **Release tracking**: Vendor-specific release versions aligned with Yocto Project releases
- **Documentation**: Comprehensive documentation for each vendor's hardware and BSP ecosystem

```
Vendor Configuration Hierarchy
┌─────────────────────────────────────────────────────────┐
│                  BSP Registry Root                      │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │           Yocto Base Configurations            │    │
│  │   (yocto/kirkstone.yml, scarthgap.yml, etc.)   │    │
│  └────────────────┬───────────────────────────────┘    │
│                   │                                      │
│                   ▼                                      │
│  ┌────────────────────────────────────────────────┐    │
│  │        Vendor-Specific Configurations          │    │
│  │                                                 │    │
│  │  ┌──────────────┐        ┌──────────────┐     │    │
│  │  │     NXP      │        │  Advantech   │     │    │
│  │  │              │        │              │     │    │
│  │  │ • Base BSP   │        │ • Extends    │     │    │
│  │  │ • NXP EVKs   │        │   NXP BSP    │     │    │
│  │  │ • meta-imx   │        │ • Industrial │     │    │
│  │  │              │        │   boards     │     │    │
│  │  └──────────────┘        │ • meta-eecc  │     │    │
│  │                          └──────────────┘     │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 2. Directory Structure

```
vendors/
├── README.md                    # This file
├── nxp/                         # NXP vendor configurations
│   ├── README.md                # NXP-specific documentation
│   ├── BOOT_PROCESS.md          # Detailed boot process guide
│   ├── common.yml               # Common NXP configurations
│   ├── imx-*.yml                # Release-specific configurations
│   └── machine/                 # NXP evaluation board configs
│       ├── imx8mpevk.yml
│       ├── imx8mq-lpddr4-wevk.yml
│       ├── imx8ulp-lpddr4-evk.yml
│       └── imx93-11x11-lpddr4x-evk.yml
└── advantech/                   # Advantech vendor configurations
    ├── README.md                # Advantech-specific documentation
    └── nxp/                     # Advantech NXP-based platforms
        ├── ADDING_NEW_BOARD.md  # Guide for adding new boards
        ├── bsp-imx-*.yml        # BSP release configurations
        ├── imx-*.yml            # Release configurations
        └── machine/             # Advantech board configs
            ├── imx8/            # i.MX 8 based boards
            │   ├── rsb3720*.yml
            │   ├── rom2620*.yml
            │   ├── rom5720*.yml
            │   ├── rom5721*.yml
            │   └── rom5722*.yml
            └── imx9/            # i.MX 9 based boards
                └── rom2820*.yml
```

## 3. Supported Vendors

### 3.1 NXP

**Description**: NXP Semiconductors i.MX processor family configurations

**Hardware Platforms**:
- i.MX 8M Plus Evaluation Kit (imx8mpevk)
- i.MX 8M Quad Evaluation Kit (imx8mq-lpddr4-wevk)
- i.MX 8ULP Evaluation Kit (imx8ulp-lpddr4-evk)
- i.MX 93 Evaluation Kit (imx93-11x11-lpddr4x-evk)

**Key Features**:
- Official NXP BSP releases
- meta-imx and meta-freescale layer support
- Multiple Yocto release support (Kirkstone through Walnascar)
- Comprehensive boot process documentation

**Documentation**: [vendors/nxp/README.md](nxp/README.md)

**Special Guides**:
- [Boot Process and Image Generation](nxp/BOOT_PROCESS.md) - Detailed low-level overview of NXP i.MX boot process

### 3.2 Advantech

**Description**: Advantech industrial computing platforms based on NXP i.MX processors

**Hardware Platforms**:
- **i.MX 8 Based**:
  - RSB-3720 Series (3.5" SBC, 2GB/4GB/6GB variants)
  - ROM-2620 (COM Express Compact, i.MX 8M Mini)
  - ROM-5720/5721/5722 (COM Express Compact, i.MX 8M Plus)

- **i.MX 9 Based**:
  - ROM-2820 (COM Express Compact, i.MX 93)

**Key Features**:
- Industrial-grade platforms
- Extends NXP base BSP with Advantech-specific drivers
- meta-eecc-nxp layer for Advantech customizations
- OTA update support (RAUC, SWUpdate, OSTree)
- Wide temperature range and industrial certifications

**Documentation**: [vendors/advantech/README.md](advantech/README.md)

**Special Guides**:
- [Adding New Boards](advantech/nxp/ADDING_NEW_BOARD.md) - Comprehensive guide for adding new boards to meta-eecc-nxp

## 4. Configuration Organization

### 4.1 Vendor Configuration Files

Each vendor directory contains configuration files organized by Yocto release:

**NXP Example**:
```yaml
# vendors/nxp/imx-6.12.49-2.2.0-walnascar.yml
header:
  version: 14
  includes:
    - yocto/walnascar.yml        # Inherits Yocto base
    - vendors/nxp/common.yml     # NXP common settings

repos:
  meta-imx:
    url: "https://github.com/nxp-imx/meta-imx.git"
    branch: "walnascar-6.12.49-2.2.0"
    commit: "..."
```

**Advantech Example**:
```yaml
# vendors/advantech/nxp/imx-6.12.49-2.2.0-walnascar.yml
header:
  version: 14
  includes:
    - vendors/nxp/imx-6.12.49-2.2.0-walnascar.yml  # Inherits NXP base

repos:
  meta-eecc-nxp:
    url: "https://github.com/Advantech-EECC/meta-eecc-nxp.git"
    branch: "walnascar"
    commit: "..."
    # Advantech-specific customizations
```

### 4.2 Machine Configurations

Machine configurations define board-specific settings:

```yaml
# vendors/nxp/machine/imx8mpevk.yml
header:
  version: 14

machine: "imx8mpevk"
```

```yaml
# vendors/advantech/nxp/machine/imx8/rsb3720.yml
header:
  version: 14

machine: "rsb3720"

local_conf_header:
  ostree-rsb3720: |
    SOTA_MACHINE:rsb3720 ?= "rsb3720"
```

### 4.3 Yocto Release Support

Vendors support multiple Yocto Project releases:

| Yocto Release | Version | NXP | Advantech | LTS |
|---------------|---------|:---:|:---------:|:---:|
| **Walnascar** | 5.2     | ✅  | ✅        | ❌  |
| **Styhead**   | 5.1     | ✅  | ✅        | ❌  |
| **Scarthgap** | 5.0     | ✅  | ✅        | ✅  |
| **Mickledore**| 4.2     | ✅  | ✅        | ❌  |
| **Kirkstone** | 4.0     | ✅  | ✅        | ✅  |

## 5. Adding a New Vendor

To add a new vendor to the BSP registry:

1. **Create Vendor Directory**:
   ```bash
   mkdir -p vendors/<vendor-name>
   ```

2. **Create README.md**:
   - Document vendor overview
   - List supported hardware platforms
   - Include Yocto release support matrix
   - Add usage examples

3. **Add Configuration Files**:
   - Create release-specific YAML files
   - Define machine configurations
   - Document layer dependencies

4. **Inherit from Yocto Base**:
   ```yaml
   header:
     includes:
       - yocto/<release>.yml
   ```

5. **Update Registry**:
   - Add vendor BSP entries to `bsp-registry.yml`
   - Create top-level configuration files
   - Add build and container definitions

6. **Documentation**:
   - Update this README with vendor information
   - Create vendor-specific documentation
   - Add examples and quick start guides

## 6. Usage

### 6.1 Building Vendor BSPs

**Using BSP Registry Manager**:
```bash
# List available BSP configurations
python bsp.py list

# Build NXP EVK BSP
python bsp.py build nxp-bsp-oenxp-walnascar-imx8mpevk

# Build Advantech modular BSP
python bsp.py build adv-mbsp-oenxp-walnascar-rsb3720
```

**Using Justfile**:
```bash
# Build modular BSP for Advantech board
just mbsp rsb3720 walnascar

# Build with OTA support
just ota-mbsp rsb3720 rauc walnascar
```

**Using KAS Directly**:
```bash
# Build using vendor configuration
kas build vendors/advantech/nxp/imx-6.12.49-2.2.0-walnascar.yml
```

### 6.2 Configuration Inheritance

Vendor configurations follow an inheritance hierarchy:

```
1. Yocto Base Configuration
   └─> yocto/walnascar.yml
       ├─ Poky base layers
       ├─ OpenEmbedded layers
       └─ Common Yocto settings

2. Vendor Base Configuration
   └─> vendors/nxp/imx-6.12.49-2.2.0-walnascar.yml
       ├─ Inherits: yocto/walnascar.yml
       ├─ Adds: meta-imx, meta-freescale
       └─ NXP-specific settings

3. Platform-Specific Configuration
   └─> vendors/advantech/nxp/imx-6.12.49-2.2.0-walnascar.yml
       ├─ Inherits: vendors/nxp/imx-6.12.49-2.2.0-walnascar.yml
       ├─ Adds: meta-eecc-nxp
       └─ Advantech-specific customizations

4. Machine Configuration
   └─> vendors/advantech/nxp/machine/imx8/rsb3720.yml
       ├─ Machine: rsb3720
       └─ Board-specific settings
```

## 7. Resources

### General Resources
- [Main BSP Registry README](../README.md) - Complete BSP registry documentation
- [KAS Documentation](https://kas.readthedocs.io/) - KAS build tool reference
- [Yocto Project Documentation](https://docs.yoctoproject.org/) - Official Yocto documentation

### Vendor-Specific Resources

**NXP**:
- [NXP i.MX Software and Tools](https://www.nxp.com/design/software/embedded-software/i-mx-software:IMX-SW)
- [NXP i.MX Yocto Project User's Guide](https://www.nxp.com/docs/en/user-guide/IMX_YOCTO_PROJECT_USERS_GUIDE.pdf)
- [meta-imx Layer](https://github.com/nxp-imx/meta-imx)
- [meta-freescale Layer](https://github.com/Freescale/meta-freescale)

**Advantech**:
- [Advantech Embedded Computing](https://www.advantech.com/products/embedded-boards)
- [Advantech GitHub](https://github.com/Advantech-EECC)
- [Advantech BSP Wiki](https://ess-wiki.advantech.com.tw/)

### Development Resources
- [Adding New Boards Guide](advantech/nxp/ADDING_NEW_BOARD.md)
- [Boot Process Documentation](nxp/BOOT_PROCESS.md)
- [Yocto Mega-Manual](https://docs.yoctoproject.org/singleindex.html)

## 8. License

This BSP configuration registry is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

Individual vendor configurations and meta-layers may have different licenses. Please refer to vendor-specific documentation and layer LICENSE files.

---

**Related Documentation**:
- [NXP Vendor README](nxp/README.md)
- [Advantech Vendor README](advantech/README.md)
- [NXP Boot Process Guide](nxp/BOOT_PROCESS.md)
- [Adding New Boards Guide](advantech/nxp/ADDING_NEW_BOARD.md)

For questions or support:
- **GitHub Issues**: [Advantech-EECC/bsp-registry](https://github.com/Advantech-EECC/bsp-registry/issues)
- **Main Documentation**: [BSP Registry README](../README.md)

---

*Document Version: 1.0*  
*Last Updated: 2026-02-07*
