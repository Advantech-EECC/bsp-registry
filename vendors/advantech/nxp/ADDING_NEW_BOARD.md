# Adding a New Board to meta-eecc-nxp Yocto Layer

This comprehensive guide provides step-by-step instructions for adding support for a new Advantech board to the meta-eecc-nxp Yocto layer and integrating it into the BSP registry.

## Table of Contents

1. [Overview](#1-overview)
   - 1.1 [Prerequisites](#11-prerequisites)
   - 1.2 [Workflow Summary](#12-workflow-summary)
2. [Understanding the Architecture](#2-understanding-the-architecture)
   - 2.1 [Layer Structure](#21-layer-structure)
   - 2.2 [Configuration Hierarchy](#22-configuration-hierarchy)
   - 2.3 [Repository Organization](#23-repository-organization)
3. [Preparing the Board Information](#3-preparing-the-board-information)
   - 3.1 [Hardware Specifications](#31-hardware-specifications)
   - 3.2 [Naming Conventions](#32-naming-conventions)
   - 3.3 [Required Documentation](#33-required-documentation)
4. [Creating Machine Configuration](#4-creating-machine-configuration)
   - 4.1 [Machine Configuration File Structure](#41-machine-configuration-file-structure)
   - 4.2 [Device Tree Selection](#42-device-tree-selection)
   - 4.3 [Kernel Configuration](#43-kernel-configuration)
   - 4.4 [U-Boot Configuration](#44-u-boot-configuration)
5. [Adding Board to meta-eecc-nxp](#5-adding-board-to-meta-eecc-nxp)
   - 5.1 [Creating Machine Directory](#51-creating-machine-directory)
   - 5.2 [Machine Configuration File](#52-machine-configuration-file)
   - 5.3 [Device Tree Customization](#53-device-tree-customization)
   - 5.4 [Kernel Customization](#54-kernel-customization)
   - 5.5 [U-Boot Customization](#55-u-boot-customization)
   - 5.6 [Image Recipes](#56-image-recipes)
6. [Creating BSP Registry Configuration](#6-creating-bsp-registry-configuration)
   - 6.1 [Machine Configuration in bsp-registry](#61-machine-configuration-in-bsp-registry)
   - 6.2 [BSP Configuration Files](#62-bsp-configuration-files)
   - 6.3 [Registry Entry](#63-registry-entry)
7. [Testing and Validation](#7-testing-and-validation)
   - 7.1 [Local Build Testing](#71-local-build-testing)
   - 7.2 [Boot Testing](#72-boot-testing)
   - 7.3 [Feature Validation](#73-feature-validation)
   - 7.4 [CI/CD Integration](#74-cicd-integration)
8. [Documentation Updates](#8-documentation-updates)
   - 8.1 [README Updates](#81-readme-updates)
   - 8.2 [Hardware Support Matrix](#82-hardware-support-matrix)
   - 8.3 [Release Notes](#83-release-notes)
9. [Advanced Topics](#9-advanced-topics)
   - 9.1 [OTA Update Support](#91-ota-update-support)
   - 9.2 [Multi-Variant Boards](#92-multi-variant-boards)
   - 9.3 [Custom Features](#93-custom-features)
10. [Troubleshooting](#10-troubleshooting)
    - 10.1 [Common Issues](#101-common-issues)
    - 10.2 [Debug Techniques](#102-debug-techniques)
11. [Examples](#11-examples)
    - 11.1 [Example: RSB-3720](#111-example-rsb-3720)
    - 11.2 [Example: ROM-2820](#112-example-rom-2820)
12. [Reference](#12-reference)
    - 12.1 [Related Documentation](#121-related-documentation)
    - 12.2 [Useful Commands](#122-useful-commands)

---

## 1. Overview

### 1.1 Prerequisites

Before adding a new board, ensure you have:

- **Hardware Information**: Complete specifications of the target board
- **NXP Reference**: Base NXP evaluation board the design is based on
- **Yocto Knowledge**: Familiarity with Yocto Project and BitBake
- **Development Environment**: 
  - Ubuntu 20.04/22.04 or compatible Linux distribution
  - Docker installed and configured
  - Python 3.x with virtual environment
  - Git access to Advantech-EECC repositories
- **Access Rights**: Write access to meta-eecc-nxp and bsp-registry repositories

### 1.2 Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│              New Board Addition Workflow                    │
└─────────────────────────────────────────────────────────────┘

1. Gather Hardware Information
   └─> Board specs, NXP SoC, peripherals, memory configuration
        │
        ▼
2. Create Machine Configuration (meta-eecc-nxp)
   └─> conf/machine/<board>.conf
   └─> Device tree files (.dts/.dtsi)
   └─> Kernel configuration fragments
   └─> U-Boot customizations
        │
        ▼
3. Test Local Build
   └─> Build image using bitbake
   └─> Verify artifacts are generated
        │
        ▼
4. Add to BSP Registry (bsp-registry)
   └─> Create machine YAML (vendors/advantech/nxp/machine/)
   └─> Update registry entry (bsp-registry.yml)
   └─> Create top-level configuration file
        │
        ▼
5. Documentation
   └─> Update README files
   └─> Add to hardware support matrix
   └─> Create release notes
        │
        ▼
6. Testing & Validation
   └─> CI/CD pipeline validation
   └─> Boot testing on hardware
   └─> Feature verification
        │
        ▼
7. Submit Pull Request
   └─> meta-eecc-nxp PR
   └─> bsp-registry PR
```

---

## 2. Understanding the Architecture

### 2.1 Layer Structure

The meta-eecc-nxp layer follows standard Yocto layer conventions:

```
meta-eecc-nxp/
├── conf/
│   ├── layer.conf                    # Layer configuration
│   └── machine/                      # Machine configurations
│       ├── rsb3720.conf             # Example: RSB-3720 board
│       ├── rom2820-ed93.conf        # Example: ROM-2820 board
│       └── <new-board>.conf         # Your new board config
├── recipes-bsp/
│   ├── u-boot/                      # U-Boot customizations
│   │   ├── u-boot-imx_%.bbappend
│   │   └── files/
│   │       └── <board>/             # Board-specific U-Boot files
│   └── imx-boot/                    # Boot image customizations
├── recipes-kernel/
│   ├── linux/                       # Kernel customizations
│   │   ├── linux-imx_%.bbappend
│   │   └── files/
│   │       └── <board>/             # Board-specific kernel files
│   └── linux-firmware/              # Firmware blobs
├── recipes-core/
│   └── images/                      # Custom image recipes
└── README.md
```

### 2.2 Configuration Hierarchy

Understanding the configuration inheritance:

```
┌─────────────────────────────────────────────────────────┐
│         Configuration Inheritance Flow                  │
└─────────────────────────────────────────────────────────┘

NXP Base BSP (meta-imx)
│   └─ Provides: Core i.MX support, base machine configs
│
├─> Yocto Release (poky)
│   └─ Provides: Build system, core recipes
│
├─> meta-freescale
│   └─ Provides: Freescale/NXP community support
│
├─> meta-eecc-nxp (Advantech Layer)
│   └─ Provides: Advantech board-specific customizations
│       ├─ Machine configurations (.conf)
│       ├─ Device tree overlays/modifications
│       ├─ Kernel configuration fragments
│       └─ U-Boot customizations
│
└─> BSP Registry Configuration
    └─ Combines: All layers with specific commits/branches
        └─> Final BSP Image
```

### 2.3 Repository Organization

```
BSP Registry Structure:
├── vendors/nxp/
│   ├── imx-<version>-<yocto>.yml    # Base NXP release configs
│   └── machine/
│       └── <nxp-board>.yml          # NXP eval board configs
│
├── vendors/advantech/nxp/
│   ├── imx-<version>-<yocto>.yml    # Advantech release configs
│   │                                 # (includes NXP base + meta-eecc-nxp)
│   └── machine/
│       ├── imx8/
│       │   └── <board>.yml          # i.MX 8 based boards
│       └── imx9/
│           └── <board>.yml          # i.MX 9 based boards
│
└── bsp-registry.yml                 # Master registry file
```

---

## 3. Preparing the Board Information

### 3.1 Hardware Specifications

Collect the following information about your new board:

**Essential Information:**
- Board name and model number
- NXP SoC variant (e.g., i.MX 8M Plus, i.MX 93)
- Base NXP evaluation board (e.g., imx8mpevk, imx93evk)
- RAM configuration (size, type: LPDDR4, DDR4, etc.)
- Storage options (eMMC, SD card, QSPI NOR)
- Display interfaces (LVDS, HDMI, MIPI-DSI)
- Network interfaces (Ethernet, WiFi, Cellular)
- Serial console (UART port and baud rate)

**Additional Information:**
- Power management requirements
- GPIO usage and pin assignments
- I2C/SPI device configurations
- USB port configurations
- PCIe devices
- Audio interfaces
- Camera interfaces

**Example Specification Sheet:**
```yaml
Board: ROM-5720
SoC: NXP i.MX 8M Plus
Base Reference: imx8mpevk
RAM: 4GB LPDDR4
Storage:
  - 32GB eMMC
  - SD card slot
Display:
  - LVDS (dual channel)
  - HDMI 2.0
Network:
  - 2x Gigabit Ethernet
  - Optional WiFi/BT module
Serial: UART1, 115200 baud
Form Factor: COM Express Compact Type 6
```

### 3.2 Naming Conventions

Follow Advantech naming conventions:

**Board Names:**
- Use lowercase with hyphens: `rsb3720`, `rom5720-db5901`
- Include variant suffixes if needed: `rsb3720-4g`, `rom5721-2g-db5901`
- Use consistent naming across all files

**File Naming:**
- Machine config: `<board>.conf` (e.g., `rsb3720.conf`)
- Device tree: `imx8mp-<board>.dts` (e.g., `imx8mp-rsb3720.dts`)
- YAML config: `<board>.yml` (e.g., `rsb3720.yml`)

**Machine Identifier:**
- Must match across all configuration files
- Used in MACHINE variable
- Example: `MACHINE = "rsb3720"`

### 3.3 Required Documentation

Prepare documentation before starting:

1. **Hardware Design Documents**
   - Schematics (if available)
   - Board layout diagrams
   - Pin assignment tables
   - Component datasheets

2. **Software Requirements**
   - Supported Yocto releases
   - Kernel version requirements
   - U-Boot version requirements
   - Required firmware blobs

3. **Testing Criteria**
   - Boot success criteria
   - Peripheral functionality checklist
   - Performance benchmarks
   - Known limitations

---

## 4. Creating Machine Configuration

### 4.1 Machine Configuration File Structure

A typical machine configuration file (`conf/machine/<board>.conf`):

```python
#@TYPE: Machine
#@NAME: Advantech <Board Name>
#@SOC: <NXP SoC>
#@DESCRIPTION: Machine configuration for Advantech <Board Name>
#@MAINTAINER: Advantech EECC <email@advantech.com>

# Include base NXP machine configuration
require conf/machine/include/imx-base.inc
require conf/machine/include/arm/armv8a/tune-cortexa53.inc

# Machine identifier
MACHINEOVERRIDES =. "mx8mp:"

# Serial console configuration
SERIAL_CONSOLES = "115200;ttymxc0"

# U-Boot configuration
UBOOT_CONFIG ??= "sd"
UBOOT_CONFIG[sd] = "imx8mp_<board>_defconfig,sdcard"
SPL_BINARY = "spl/u-boot-spl.bin"
UBOOT_DTB_NAME = "imx8mp-<board>.dtb"
UBOOT_MAKE_TARGET = "all"

# Kernel configuration
KERNEL_DEVICETREE = "freescale/imx8mp-<board>.dtb"
KERNEL_IMAGETYPE = "Image"

# Boot image configuration
IMX_BOOT_SEEK = "32"
IMXBOOT_TARGETS = "flash_evk"

# Preferred providers
PREFERRED_PROVIDER_virtual/kernel ??= "linux-imx"
PREFERRED_PROVIDER_virtual/bootloader ??= "u-boot-imx"

# WKS file for disk image creation
WKS_FILE = "imx-imx-boot-bootpart.wks.in"

# Machine features
MACHINE_FEATURES += "usbgadget usbhost pci wifi bluetooth"

# Graphics and multimedia
MACHINE_FEATURES += "gpu opengl vulkan"

# Extra firmware
MACHINE_FIRMWARE:append = " linux-firmware-<board-specific>"

# Default image features
EXTRA_IMAGEDEPENDS += "imx-boot"
```

### 4.2 Device Tree Selection

Determine the appropriate device tree:

1. **Check NXP Reference Device Trees:**
   ```bash
   # In Linux kernel sources
   ls arch/arm64/boot/dts/freescale/imx8mp-*.dts
   ```

2. **Create Custom Device Tree:**
   - Start from closest NXP reference board
   - Example: `imx8mp-evk.dts` for i.MX 8M Plus boards

3. **Device Tree Organization:**
   ```
   arch/arm64/boot/dts/freescale/
   ├── imx8mp.dtsi                    # SoC common
   ├── imx8mp-evk.dtb                # NXP EVK reference
   └── imx8mp-<board>.dts            # Your board (new)
       └─ Includes: imx8mp.dtsi
       └─ Customizes: Board-specific peripherals
   ```

### 4.3 Kernel Configuration

Kernel configuration options:

1. **Configuration Fragment:**
   Create `recipes-kernel/linux/files/<board>/defconfig`:
   ```
   # Board-specific kernel options
   CONFIG_SND_SOC_<BOARD_CODEC>=y
   CONFIG_<BOARD_SPECIFIC_DRIVER>=y
   # ... more configs
   ```

2. **Apply Fragment:**
   In `recipes-kernel/linux/linux-imx_%.bbappend`:
   ```python
   FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
   
   SRC_URI:append:<board> = " \
       file://<board>/defconfig \
   "
   ```

### 4.4 U-Boot Configuration

U-Boot configuration steps:

1. **Create defconfig:**
   Based on NXP reference board:
   ```bash
   # Start from NXP defconfig
   cp configs/imx8mp_evk_defconfig configs/imx8mp_<board>_defconfig
   ```

2. **Customize for board:**
   ```
   CONFIG_TARGET_IMX8MP_<BOARD>=y
   CONFIG_DEFAULT_DEVICE_TREE="imx8mp-<board>"
   CONFIG_ENV_SIZE=0x2000
   # ... board-specific configs
   ```

3. **Add to U-Boot recipe:**
   In `recipes-bsp/u-boot/u-boot-imx_%.bbappend`:
   ```python
   FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
   
   SRC_URI:append:<board> = " \
       file://<board>/imx8mp_<board>_defconfig \
   "
   ```

---

## 5. Adding Board to meta-eecc-nxp

### 5.1 Creating Machine Directory

In the meta-eecc-nxp layer repository:

```bash
# Clone meta-eecc-nxp repository
git clone https://github.com/Advantech-EECC/meta-eecc-nxp.git
cd meta-eecc-nxp

# Create branch for new board
git checkout -b feature/add-<board>-support
```

### 5.2 Machine Configuration File

Create the machine configuration file:

```bash
# Create machine configuration
cat > conf/machine/<board>.conf << 'EOF'
#@TYPE: Machine
#@NAME: Advantech <Board Name>
#@SOC: i.MX 8M Plus
#@DESCRIPTION: Machine configuration for Advantech <Board Name>
#@MAINTAINER: Advantech EECC <email@advantech.com>

require conf/machine/include/imx-base.inc
require conf/machine/include/arm/armv8a/tune-cortexa53.inc

MACHINEOVERRIDES =. "mx8mp:"

SERIAL_CONSOLES = "115200;ttymxc0"

UBOOT_CONFIG ??= "sd"
UBOOT_CONFIG[sd] = "imx8mp_<board>_defconfig,sdcard"

KERNEL_DEVICETREE = "freescale/imx8mp-<board>.dtb"

IMX_BOOT_SEEK = "32"

PREFERRED_PROVIDER_virtual/kernel = "linux-imx"
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-imx"

MACHINE_FEATURES += "usbgadget usbhost pci wifi bluetooth"
EOF
```

### 5.3 Device Tree Customization

Create device tree files:

```bash
# Create directory for device tree files
mkdir -p recipes-kernel/linux/files/<board>

# Create device tree source
cat > recipes-kernel/linux/files/<board>/imx8mp-<board>.dts << 'EOF'
// SPDX-License-Identifier: (GPL-2.0+ OR MIT)
/*
 * Copyright 2024 Advantech Corporation
 */

/dts-v1/;

#include "imx8mp.dtsi"

/ {
    model = "Advantech <Board Name>";
    compatible = "advantech,<board>", "fsl,imx8mp";

    chosen {
        stdout-path = &uart1;
    };

    memory@40000000 {
        device_type = "memory";
        reg = <0x0 0x40000000 0 0x80000000>; /* 2GB */
    };

    /* Board-specific nodes */
};

/* Enable and configure peripherals */
&uart1 {
    pinctrl-names = "default";
    pinctrl-0 = <&pinctrl_uart1>;
    status = "okay";
};

/* More peripheral configurations */
EOF
```

### 5.4 Kernel Customization

Create kernel append recipe:

```bash
# Create kernel bbappend
cat > recipes-kernel/linux/linux-imx_%.bbappend << 'EOF'
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# Add device tree for new board
SRC_URI:append:<board> = " \
    file://<board>/imx8mp-<board>.dts;subdir=git/arch/arm64/boot/dts/freescale \
"

# Add to device tree list
KERNEL_DEVICETREE:append:<board> = " \
    freescale/imx8mp-<board>.dtb \
"

# Add configuration fragment if needed
SRC_URI:append:<board> = " \
    file://<board>/defconfig \
"

# Mark this as compatible with the machine
COMPATIBLE_MACHINE:<board> = "<board>"
EOF
```

### 5.5 U-Boot Customization

Create U-Boot append recipe:

```bash
# Create U-Boot bbappend
cat > recipes-bsp/u-boot/u-boot-imx_%.bbappend << 'EOF'
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# Add defconfig for new board
SRC_URI:append:<board> = " \
    file://<board>/imx8mp_<board>_defconfig;subdir=git/configs \
"

# Add device tree if needed
SRC_URI:append:<board> = " \
    file://<board>/imx8mp-<board>.dts;subdir=git/arch/arm/dts \
"

COMPATIBLE_MACHINE:<board> = "<board>"
EOF

# Create defconfig directory
mkdir -p recipes-bsp/u-boot/files/<board>
```

### 5.6 Image Recipes

Create custom image recipe if needed:

```bash
# Create custom image recipe (optional)
cat > recipes-core/images/<board>-image.bb << 'EOF'
SUMMARY = "Advantech <Board Name> custom image"
LICENSE = "MIT"

require recipes-core/images/imx-image-core.bb

# Add board-specific packages
IMAGE_INSTALL:append = " \
    <board-specific-package> \
    <another-package> \
"

# Board compatibility
COMPATIBLE_MACHINE = "<board>"
EOF
```

---

## 6. Creating BSP Registry Configuration

### 6.1 Machine Configuration in bsp-registry

In the bsp-registry repository, create machine configuration:

```bash
# Clone bsp-registry
git clone https://github.com/Advantech-EECC/bsp-registry.git
cd bsp-registry

# Create branch
git checkout -b feature/add-<board>-support

# Determine processor family (imx8 or imx9)
# For i.MX 8M family boards:
mkdir -p vendors/advantech/nxp/machine/imx8

# For i.MX 93 boards:
# mkdir -p vendors/advantech/nxp/machine/imx9
```

Create machine YAML file:

```bash
# For i.MX 8M Plus board
cat > vendors/advantech/nxp/machine/imx8/<board>.yml << 'EOF'
header:
  version: 14

machine: "<board>"

local_conf_header:
  ostree-<board>: |

    SOTA_MACHINE:<board> ?= "<board>"
EOF
```

**Explanation:**
- `header.version`: KAS configuration version (currently 14)
- `machine`: Machine identifier matching meta-eecc-nxp conf file
- `local_conf_header`: Optional BitBake local.conf additions
  - OTA-specific configuration for OSTree/SOTA support

### 6.2 BSP Configuration Files

Create top-level BSP configuration:

```bash
# Create configuration file for the board with specific Yocto release
cat > adv-mbsp-oenxp-walnascar-<board>.yaml << 'EOF'
header:
  version: 14
  includes:
    - vendors/advantech/nxp/imx-6.12.49-2.2.0-walnascar.yml
    - vendors/advantech/nxp/machine/imx8/<board>.yml
    - features/mbsp/walnascar/mbsp.yml

bblayers_conf_header:
  meta-layers: |
    BBLAYERS_EECC_NXP_<BOARD_UPPER> = "${BSPDIR}/layers/meta-eecc-nxp"
EOF
```

**Multi-Release Support:**

For different Yocto releases, create multiple configuration files:

```bash
# Scarthgap (LTS)
adv-mbsp-oenxp-scarthgap-<board>.yaml

# Styhead
adv-mbsp-oenxp-styhead-<board>.yaml

# Walnascar
adv-mbsp-oenxp-walnascar-<board>.yaml
```

### 6.3 Registry Entry

Add entry to `bsp-registry.yml`:

```yaml
registry:
  mbsp:
    # ... existing entries ...

    # =====================================
    # Advantech <Board Name> Modular BSPs
    # =====================================

    - name: adv-mbsp-oenxp-walnascar-<board>
      description: "Advantech EIoT Yocto Walnascar <Board Name>"
      build:
        path: build/adv-mbsp-oenxp-<board>-walnascar
        environment:
          container: "ubuntu-22.04"
        configuration:
          - adv-mbsp-oenxp-walnascar-<board>.yaml

    - name: adv-mbsp-oenxp-scarthgap-<board>
      description: "Advantech EIoT Yocto Scarthgap <Board Name>"
      build:
        path: build/adv-mbsp-oenxp-<board>-scarthgap
        environment:
          container: "ubuntu-22.04"
        configuration:
          - adv-mbsp-oenxp-scarthgap-<board>.yaml
```

---

## 7. Testing and Validation

### 7.1 Local Build Testing

Test the build locally before committing:

```bash
# Setup environment
cd bsp-registry
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# List BSP configurations to verify
python bsp.py list | grep <board>

# Build the BSP
python bsp.py build adv-mbsp-oenxp-walnascar-<board>

# Alternative: Use just command
just mbsp <board> walnascar
```

**Expected Output:**
```
Building BSP: adv-mbsp-oenxp-walnascar-<board>
Container: ubuntu-22.04
Build path: build/adv-mbsp-oenxp-<board>-walnascar
... (build progress)
Build completed successfully!
```

**Verify Generated Artifacts:**
```bash
# Check build output
ls build/adv-mbsp-oenxp-<board>-walnascar/tmp/deploy/images/<board>/

# Expected files:
# - imx-boot
# - Image (kernel)
# - imx8mp-<board>.dtb
# - *.wic (disk image)
# - *.wic.bmap
```

### 7.2 Boot Testing

Test the image on hardware:

1. **Flash Image to SD Card:**
   ```bash
   # Using bmaptool (recommended)
   sudo bmaptool copy \
       build/.../tmp/deploy/images/<board>/imx-image-core-<board>.wic.zst \
       /dev/sdX

   # Or using dd
   zstd -d imx-image-core-<board>.wic.zst
   sudo dd if=imx-image-core-<board>.wic of=/dev/sdX bs=1M status=progress
   ```

2. **Serial Console Connection:**
   ```bash
   # Connect to serial console (usually /dev/ttyUSB0)
   sudo minicom -D /dev/ttyUSB0 -b 115200
   # or
   sudo picocom -b 115200 /dev/ttyUSB0
   ```

3. **Boot Log Verification:**
   - U-Boot loads successfully
   - Kernel boots without errors
   - Device tree is correctly recognized
   - Root filesystem mounts
   - System reaches login prompt

4. **Boot Checklist:**
   ```
   [ ] U-Boot banner displays board name
   [ ] U-Boot environment loads correctly
   [ ] Kernel decompresses and starts
   [ ] Device tree matches board
   [ ] RAM size is correct
   [ ] All expected peripherals detected
   [ ] Network interfaces present
   [ ] Storage devices accessible
   [ ] Login prompt appears
   ```

### 7.3 Feature Validation

Test board-specific features:

```bash
# Network
ping -c 4 8.8.8.8

# Storage
mount
df -h

# USB
lsusb

# PCI devices
lspci

# GPIO (if applicable)
cat /sys/kernel/debug/gpio

# I2C devices
i2cdetect -l
i2cdetect -y 0

# Display (if applicable)
cat /sys/class/drm/card*/status
```

### 7.4 CI/CD Integration

The BSP registry includes automated validation:

1. **KAS Configuration Validation:**
   - Validates YAML syntax
   - Checks configuration includes
   - Verifies layer references

2. **Build Validation:**
   - Triggered by pull requests
   - Builds in clean container
   - Validates artifacts

3. **Check CI Status:**
   ```bash
   # After pushing to GitHub
   # Check Actions tab in GitHub UI
   # Or use gh CLI:
   gh pr checks
   ```

---

## 8. Documentation Updates

### 8.1 README Updates

Update `vendors/advantech/README.md`:

```markdown
### i.MX 8 Based Platforms

| Board Model | Processor | Form Factor | RAM Options | Status | Product Link |
|-------------|-----------|-------------|-------------|--------|--------------|
| **<Board Name>** | i.MX 8M Plus | <Form Factor> | <RAM> | 🟢 Stable | [Product Page](<URL>) |
```

### 8.2 Hardware Support Matrix

Update support matrix:

```markdown
| Board | Walnascar | Styhead | Scarthgap | Mickledore | Kirkstone |
|-------|:---------:|:-------:|:---------:|:----------:|:---------:|
| **<Board>** | ✅ | ✅ | ✅ | ❌ | ❌ |
```

### 8.3 Release Notes

Create release notes section:

```markdown
## Release Notes - <Board Name> Support

### Added
- Support for Advantech <Board Name>
- i.MX 8M Plus based COM Express module
- Yocto Walnascar/Scarthgap support

### Hardware Features
- 4GB LPDDR4 RAM
- Dual Gigabit Ethernet
- LVDS and HDMI display outputs
- USB 3.0 support

### Known Limitations
- WiFi module requires additional firmware (if applicable)
- Camera interface not yet validated
```

---

## 9. Advanced Topics

### 9.1 OTA Update Support

Add OTA (Over-The-Air) update support:

**RAUC Support:**
```yaml
# In machine YAML configuration
local_conf_header:
  rauc-<board>: |
    DISTRO_FEATURES:append = " rauc"
    PREFERRED_PROVIDER_virtual/bootloader:pn-rauc = "u-boot-imx"
```

**OSTree Support:**
```yaml
local_conf_header:
  ostree-<board>: |
    DISTRO_FEATURES:append = " ostree"
    SOTA_MACHINE:<board> ?= "<board>"
```

**Create OTA Configuration:**
```bash
# Create OTA-enabled configuration
cat > adv-ota-mbsp-oenxp-walnascar-<board>-rauc.yaml << 'EOF'
header:
  version: 14
  includes:
    - vendors/advantech/nxp/imx-6.12.49-2.2.0-walnascar.yml
    - vendors/advantech/nxp/machine/imx8/<board>.yml
    - features/mbsp/walnascar/mbsp.yml
    - features/ota/rauc/walnascar/rauc.yml
EOF
```

### 9.2 Multi-Variant Boards

For boards with multiple variants (e.g., different RAM sizes):

**Option 1: Separate Machine Configs**
```bash
# Create separate configs for each variant
conf/machine/<board>-2g.conf
conf/machine/<board>-4g.conf
conf/machine/<board>-8g.conf
```

**Option 2: Single Config with Overrides**
```python
# In machine config
RAM_SIZE ?= "2G"

# Device tree
KERNEL_DEVICETREE = "freescale/imx8mp-<board>.dtb"
KERNEL_DEVICETREE:append:<board>-4g = " freescale/imx8mp-<board>-4g.dtb"

# U-Boot
UBOOT_CONFIG[sd] = "imx8mp_<board>_${RAM_SIZE}_defconfig,sdcard"
```

### 9.3 Custom Features

Add custom board-specific features:

**Example: Custom Hardware Watchdog**
```python
# In recipes-bsp/watchdog/
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append:<board> = " \
    file://<board>-watchdog.service \
"

do_install:append:<board>() {
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/<board>-watchdog.service \
        ${D}${systemd_system_unitdir}/
}

SYSTEMD_SERVICE:${PN}:append:<board> = " <board>-watchdog.service"
```

---

## 10. Troubleshooting

### 10.1 Common Issues

**Issue 1: Build Fails with "No machine config found"**

**Symptom:**
```
ERROR: No machine configuration found for machine <board>
```

**Solution:**
- Verify machine config exists in meta-eecc-nxp
- Check MACHINE variable in configuration
- Ensure layer is included in bblayers.conf

**Issue 2: Device Tree Not Found**

**Symptom:**
```
ERROR: linux-imx: Could not find freescale/imx8mp-<board>.dtb
```

**Solution:**
- Verify device tree file is in correct location
- Check KERNEL_DEVICETREE variable
- Ensure bbappend includes device tree in SRC_URI

**Issue 3: U-Boot Fails to Build**

**Symptom:**
```
ERROR: u-boot-imx: defconfig imx8mp_<board>_defconfig not found
```

**Solution:**
- Verify defconfig exists in u-boot source
- Check UBOOT_CONFIG variable
- Ensure defconfig is added via bbappend

**Issue 4: Board Doesn't Boot**

**Symptom:**
- No output on serial console
- Or boots but fails to find root filesystem

**Solution:**
1. Check serial console connection (correct UART, baud rate)
2. Verify boot media is correctly flashed
3. Check U-Boot environment variables
4. Verify kernel command line arguments

### 10.2 Debug Techniques

**Enable Verbose Boot:**
```bash
# In U-Boot
setenv bootargs console=ttymxc0,115200 loglevel=8 earlycon
saveenv
boot
```

**BitBake Debug:**
```bash
# Clean specific recipe
bitbake -c cleansstate linux-imx

# Rebuild with debug
bitbake -v linux-imx

# Get recipe info
bitbake -e linux-imx | grep ^KERNEL_DEVICETREE=

# Check do_compile log
bitbake -c compile -f linux-imx
tail -f build/.../tmp/work/.../<board>/linux-imx/*/temp/log.do_compile
```

**Device Tree Debugging:**
```bash
# Decompile device tree on target
dtc -I dtb -O dts /sys/firmware/fdt > /tmp/running.dts
cat /tmp/running.dts

# Check what device tree was loaded
cat /sys/firmware/devicetree/base/compatible
```

**U-Boot Debugging:**
```bash
# In U-Boot console
printenv
bdinfo
fdt print
```

---

## 11. Examples

### 11.1 Example: RSB-3720

Complete example for RSB-3720 board:

**Machine Configuration** (`conf/machine/rsb3720.conf`):
```python
#@TYPE: Machine
#@NAME: Advantech RSB-3720
#@SOC: i.MX 8M Plus
#@DESCRIPTION: Machine configuration for Advantech RSB-3720
#@MAINTAINER: Advantech EECC

require conf/machine/include/imx-base.inc
require conf/machine/include/arm/armv8a/tune-cortexa53.inc

MACHINEOVERRIDES =. "mx8mp:"

SERIAL_CONSOLES = "115200;ttymxc0"

UBOOT_CONFIG ??= "sd"
UBOOT_CONFIG[sd] = "imx8mp_rsb3720_defconfig,sdcard"

KERNEL_DEVICETREE = " \
    freescale/imx8mp-rsb3720.dtb \
"

IMX_BOOT_SEEK = "32"

PREFERRED_PROVIDER_virtual/kernel = "linux-imx"
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-imx"

MACHINE_FEATURES += "usbgadget usbhost pci wifi bluetooth"
MACHINE_FEATURES += "gpu opengl vulkan"
```

**BSP Registry Machine YAML** (`vendors/advantech/nxp/machine/imx8/rsb3720.yml`):
```yaml
header:
  version: 14

machine: "rsb3720"

local_conf_header:
  ostree-rsb3720: |

    SOTA_MACHINE:rsb3720 ?= "rsb3720"
```

**Top-level Configuration** (`adv-mbsp-oenxp-walnascar-rsb3720.yaml`):
```yaml
header:
  version: 14
  includes:
    - vendors/advantech/nxp/imx-6.12.49-2.2.0-walnascar.yml
    - vendors/advantech/nxp/machine/imx8/rsb3720.yml
    - features/mbsp/walnascar/mbsp.yml
```

### 11.2 Example: ROM-2820

Example for i.MX 93 based board:

**Machine Configuration** (`conf/machine/rom2820-ed93.conf`):
```python
#@TYPE: Machine
#@NAME: Advantech ROM-2820
#@SOC: i.MX 93
#@DESCRIPTION: Machine configuration for Advantech ROM-2820
#@MAINTAINER: Advantech EECC

require conf/machine/include/imx-base.inc
require conf/machine/include/arm/armv8-2a/tune-cortexa55.inc

MACHINEOVERRIDES =. "mx93:"

SERIAL_CONSOLES = "115200;ttymxc0"

UBOOT_CONFIG ??= "sd"
UBOOT_CONFIG[sd] = "imx93_rom2820_defconfig,sdcard"

KERNEL_DEVICETREE = " \
    freescale/imx93-rom2820-ed93.dtb \
"

IMX_BOOT_SEEK = "32"

PREFERRED_PROVIDER_virtual/kernel = "linux-imx"
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-imx"

MACHINE_FEATURES += "usbgadget usbhost pci"
```

**BSP Registry Machine YAML** (`vendors/advantech/nxp/machine/imx9/rom2820-ed93.yml`):
```yaml
header:
  version: 14

machine: "rom2820-ed93"

local_conf_header:
  ostree-rom2820-ed93: |

    SOTA_MACHINE:rom2820-ed93 ?= "rom2820-ed93"
```

---

## 12. Reference

### 12.1 Related Documentation

**Internal Documentation:**
- [NXP Vendor README](../../../nxp/README.md)
- [Advantech Vendor README](../../README.md)
- [NXP Boot Process Guide](../../../nxp/BOOT_PROCESS.md)
- [Main BSP Registry README](../../../../README.md)

**External Documentation:**
- [Yocto Project Documentation](https://docs.yoctoproject.org/)
- [NXP i.MX Linux User's Guide](https://www.nxp.com/docs/en/user-guide/IMX_LINUX_USERS_GUIDE.pdf)
- [NXP i.MX Yocto Project User's Guide](https://www.nxp.com/docs/en/user-guide/IMX_YOCTO_PROJECT_USERS_GUIDE.pdf)
- [KAS Documentation](https://kas.readthedocs.io/)
- [meta-imx Layer](https://github.com/nxp-imx/meta-imx)
- [meta-freescale Layer](https://github.com/Freescale/meta-freescale)

### 12.2 Useful Commands

**BSP Registry Commands:**
```bash
# List all BSP configurations
python bsp.py list

# List configurations for specific board
python bsp.py list | grep <board>

# Build BSP
python bsp.py build adv-mbsp-oenxp-walnascar-<board>

# Export KAS configuration
python bsp.py export adv-mbsp-oenxp-walnascar-<board>

# Use just shortcuts
just mbsp <board> walnascar
just ota-mbsp <board> rauc walnascar
```

**BitBake Commands:**
```bash
# List all machine configurations
bitbake-layers show-machines

# Show layers
bitbake-layers show-layers

# Show recipe info
bitbake -e <recipe> | grep ^VARIABLE=

# Clean specific package
bitbake -c cleansstate <recipe>

# Build specific package
bitbake <recipe>

# Build image
bitbake imx-image-core
```

**KAS Commands:**
```bash
# Build using KAS directly
kas build adv-mbsp-oenxp-walnascar-<board>.yaml

# Shell into build environment
kas shell adv-mbsp-oenxp-walnascar-<board>.yaml

# Check configuration
kas dump adv-mbsp-oenxp-walnascar-<board>.yaml
```

**Git Workflow:**
```bash
# meta-eecc-nxp workflow
git checkout -b feature/add-<board>-support
# ... make changes ...
git add conf/machine/<board>.conf
git commit -m "Add support for <board>"
git push origin feature/add-<board>-support

# bsp-registry workflow
git checkout -b feature/add-<board>-support
# ... make changes ...
git add vendors/advantech/nxp/machine/
git add adv-mbsp-oenxp-*-<board>.yaml
git add bsp-registry.yml
git commit -m "Add BSP registry configuration for <board>"
git push origin feature/add-<board>-support
```

---

## Summary

Adding a new board to the meta-eecc-nxp Yocto layer involves:

1. **Preparation**: Gather hardware specs and documentation
2. **meta-eecc-nxp**: Create machine config, device tree, kernel/U-Boot customizations
3. **bsp-registry**: Create KAS configuration files and registry entries
4. **Testing**: Build and validate on hardware
5. **Documentation**: Update README and support matrices
6. **Review**: Submit pull requests for both repositories

Following this guide ensures consistent, maintainable board support that integrates seamlessly with the Advantech BSP ecosystem.

For questions or support, contact:
- **Email**: Contact your Advantech sales representative
- **GitHub Issues**: [Advantech-EECC/bsp-registry](https://github.com/Advantech-EECC/bsp-registry/issues)
- **Documentation**: [BSP Registry Main README](../../../../README.md)

---

*Document Version: 1.0*  
*Last Updated: 2026-02-07*
