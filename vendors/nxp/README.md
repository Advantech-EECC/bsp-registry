# NXP i.MX BSP Configurations

This directory contains Board Support Package (BSP) configurations for NXP i.MX processors. These configurations provide the base reference implementations for building Yocto-based Linux distributions on NXP evaluation boards.

📖 **For detailed information about the NXP i.MX boot process and bootable image generation, see [BOOT_PROCESS.md](BOOT_PROCESS.md)**

## Overview

NXP i.MX processors are a family of applications processors built on Arm Cortex-A cores, designed for industrial and embedded applications. The BSP configurations in this directory enable building complete Linux distributions using the Yocto Project build system.

```
NXP i.MX BSP Structure
├── common.yml                  # Common NXP i.MX configurations
├── Release Configurations
│   ├── Kirkstone (Yocto 4.0 LTS)
│   │   ├── imx-5.15.52-2.1.0-kirkstone.yml
│   │   └── imx-5.15.71-2.2.0-kirkstone.yml
│   ├── Mickledore (Yocto 4.2)
│   │   └── imx-6.1.22-2.0.0-mickledore.yml
│   ├── Scarthgap (Yocto 5.0 LTS)
│   │   ├── imx-6.6.23-2.0.0-scarthgap.yml
│   │   ├── imx-6.6.36-2.1.0-scarthgap.yml
│   │   └── imx-6.6.52-2.2.0-scarthgap.yml
│   ├── Styhead (Yocto 5.1)
│   │   └── imx-6.12.3-1.0.0-styhead.yml
│   └── Walnascar (Yocto 5.2)
│       ├── imx-6.12.20-2.0.0-walnascar.yml
│       ├── imx-6.12.34-2.1.0-walnascar.yml
│       └── imx-6.12.49-2.2.0-walnascar.yml
└── Machine Configurations
    ├── imx8mpevk.yml              # i.MX 8M Plus EVK
    ├── imx8mq-lpddr4-wevk.yml     # i.MX 8M Quad EVK
    ├── imx8ulp-lpddr4-evk.yml     # i.MX 8ULP EVK
    └── imx93-11x11-lpddr4x-evk.yml # i.MX 93 EVK
```

## Supported Hardware

The following NXP evaluation boards are supported:

| Board | Processor | Description |
|-------|-----------|-------------|
| **imx8mpevk** | i.MX 8M Plus | NXP i.MX 8M Plus Evaluation Kit with quad-core Cortex-A53 |
| **imx8mq-lpddr4-wevk** | i.MX 8M Quad | NXP i.MX 8M Quad Evaluation Kit with quad-core Cortex-A53 |
| **imx8ulp-lpddr4-evk** | i.MX 8ULP | NXP i.MX 8ULP Evaluation Kit with low-power features |
| **imx93-11x11-lpddr4x-evk** | i.MX 93 | NXP i.MX 93 Evaluation Kit with dual-core Cortex-A55 |

## Release Information

### Yocto Release Overview

```
Timeline: Yocto Releases
│
├─ Kirkstone (4.0 LTS) ──────── Long Term Support until April 2026
│  └─ Linux Kernel: 5.15.x
│
├─ Mickledore (4.2) ──────────── Standard Release (EOL)
│  └─ Linux Kernel: 6.1.x
│
├─ Scarthgap (5.0 LTS) ───────── Long Term Support until April 2028
│  └─ Linux Kernel: 6.6.x
│
├─ Styhead (5.1) ────────────── Standard Release
│  └─ Linux Kernel: 6.12.x
│
└─ Walnascar (5.2) ──────────── Latest Release
   └─ Linux Kernel: 6.12.x
```

### Available Releases

#### Kirkstone (Yocto 4.0 LTS)
- **imx-5.15.52-2.1.0-kirkstone** - NXP BSP release 2.1.0 with Linux 5.15.52
- **imx-5.15.71-2.2.0-kirkstone** - NXP BSP release 2.2.0 with Linux 5.15.71

#### Mickledore (Yocto 4.2)
- **imx-6.1.22-2.0.0-mickledore** - NXP BSP release 2.0.0 with Linux 6.1.22

#### Scarthgap (Yocto 5.0 LTS)
- **imx-6.6.23-2.0.0-scarthgap** - NXP BSP release 2.0.0 with Linux 6.6.23
- **imx-6.6.36-2.1.0-scarthgap** - NXP BSP release 2.1.0 with Linux 6.6.36
- **imx-6.6.52-2.2.0-scarthgap** - NXP BSP release 2.2.0 with Linux 6.6.52

#### Styhead (Yocto 5.1)
- **imx-6.12.3-1.0.0-styhead** - NXP BSP release 1.0.0 with Linux 6.12.3

#### Walnascar (Yocto 5.2)
- **imx-6.12.20-2.0.0-walnascar** - NXP BSP release 2.0.0 with Linux 6.12.20
- **imx-6.12.34-2.1.0-walnascar** - NXP BSP release 2.1.0 with Linux 6.12.34
- **imx-6.12.49-2.2.0-walnascar** - NXP BSP release 2.2.0 with Linux 6.12.49

## Architecture

### BSP Layer Stack

```
┌─────────────────────────────────────────────────────────┐
│                   Target Image                          │
│           (imx-image-core/multimedia/full)              │
├─────────────────────────────────────────────────────────┤
│                  NXP BSP Layers                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ meta-imx (NXP i.MX BSP layer)                    │   │
│  │  ├─ meta-imx-bsp    (Board support)              │   │
│  │  ├─ meta-imx-sdk    (SDK components)             │   │
│  │  ├─ meta-imx-ml     (Machine learning)           │   │
│  │  └─ meta-imx-v2x    (V2X communication)          │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ meta-freescale (Community BSP)                   │   │
│  ├──────────────────────────────────────────────────┤   │
│  │ meta-freescale-distro (Distro configs)           │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│              OpenEmbedded Core Layers                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ meta-openembedded                                │   │
│  │  ├─ meta-oe         (Additional recipes)         │   │
│  │  ├─ meta-python     (Python packages)            │   │
│  │  ├─ meta-networking (Network protocols)          │   │
│  │  └─ meta-multimedia (Media libraries)            │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                    Poky (Yocto)                         │
│             Reference Distribution Layer                │
└─────────────────────────────────────────────────────────┘
```

## Configuration Files

### common.yml

The `common.yml` file contains base configuration settings shared across all NXP i.MX BSP releases:

- **Distro**: `fsl-imx-xwayland` (Wayland-based graphics stack)
- **EULA**: Accepts the Freescale EULA for proprietary components
- **Features**: OpenGL, Vulkan, seccomp security
- **Target Images**: imx-image-core, imx-image-multimedia, imx-image-full

### Release Configuration Files

Each release configuration file (e.g., `imx-6.12.49-2.2.0-walnascar.yml`) includes:

1. **Header**: KAS version and included configurations
2. **Repository commits**: Specific git commits for all meta-layers
3. **Layer definitions**: Which BSP layers to include
4. **Patches**: Any necessary fixes for the release

### Machine Configuration Files

Machine files define board-specific settings:

- Hardware platform identifier
- Boot configuration
- Kernel device tree
- Hardware features and capabilities

## Usage

### Building a BSP Image

To build an image for an NXP evaluation board, use the BSP registry manager:

```bash
# Example: Build for i.MX 8M Plus EVK with Walnascar release
just bsp <board-name> <yocto-release>
```

### Customization

To customize a BSP:

1. Select the appropriate release configuration
2. Choose the target machine configuration
3. Add feature layers as needed (from `features/` directory)
4. Include the configuration files in your top-level KAS YAML

## Resources

**Local Documentation**:
- [Boot Process and Bootable Image Generation](BOOT_PROCESS.md) - Detailed low-level overview of NXP i.MX boot process

**NXP Official Resources**:
- [NXP i.MX Software and Tools](https://www.nxp.com/design/software/embedded-software/i-mx-software:IMX-SW)
- [NXP i.MX Yocto Project User's Guide](https://www.nxp.com/docs/en/user-guide/IMX_YOCTO_PROJECT_USERS_GUIDE.pdf)
- [Yocto Project Documentation](https://docs.yoctoproject.org/)
- [meta-freescale Layer](https://github.com/Freescale/meta-freescale)
- [meta-imx Layer](https://github.com/nxp-imx/meta-imx)

## License

The configuration files in this directory are provided under the terms specified in the repository's LICENSE file. Note that building images may include software components with various licenses, including proprietary NXP software requiring EULA acceptance.
