# NXP i.MX Boot Process and Bootable Image Generation

This document provides a detailed, low-level overview of how bootable images are generated for NXP i.MX boards, covering the boot process architecture, firmware components, and image creation workflow.

## Table of Contents

- [Boot Process Overview](#boot-process-overview)
- [Boot Stages](#boot-stages)
- [Bootable Image Components](#bootable-image-components)
- [Image Generation Process](#image-generation-process)
- [Boot Media Layout](#boot-media-layout)
- [Processor-Specific Variations](#processor-specific-variations)
- [Yocto/BitBake Integration](#yoctobitbake-integration)
- [Troubleshooting](#troubleshooting)

---

## Boot Process Overview

The NXP i.MX processor family uses a multi-stage boot process to initialize the hardware and load the operating system. The boot chain involves several firmware components that execute sequentially:

```
┌─────────────────────────────────────────────────────────────┐
│                    Boot Flow Diagram                        │
└─────────────────────────────────────────────────────────────┘

Power-On / Reset
      │
      ▼
┌──────────────────┐
│   Boot ROM       │  ◄── Hardcoded in SoC (cannot modify)
│  (BootROM)       │      Reads boot device selection
└────────┬─────────┘      Loads from offset 0x400 (SD/eMMC)
         │
         │ Loads SPL/FSBL
         ▼
┌──────────────────┐
│   SPL/FSBL       │  ◄── Secondary Program Loader
│ (u-boot-spl.bin) │      Initializes DDR RAM
└────────┬─────────┘      Minimal hardware setup
         │
         │ Loads ATF (i.MX 8/9)
         ▼
┌──────────────────┐
│   ARM TF (ATF)   │  ◄── ARM Trusted Firmware (BL31)
│   (bl31.bin)     │      EL3 secure monitor
└────────┬─────────┘      Power management
         │
         │ (Optional) Loads TEE
         ▼
┌──────────────────┐
│   OP-TEE         │  ◄── Secure OS (optional)
│   (tee.bin)      │      Trusted execution environment
└────────┬─────────┘
         │
         │ Loads U-Boot
         ▼
┌──────────────────┐
│   U-Boot Proper  │  ◄── Main bootloader
│  (u-boot.bin)    │      Full hardware initialization
└────────┬─────────┘      Boot menu, scripts
         │                Network, USB, storage drivers
         │
         │ Loads kernel
         ▼
┌──────────────────┐
│   Linux Kernel   │  ◄── Operating system
│   (Image/zImage) │      Device drivers
└────────┬─────────┘      System initialization
         │
         ▼
┌──────────────────┐
│   Root Filesystem│  ◄── User space
│   (rootfs)       │      Applications
└──────────────────┘
```

---

## Boot Stages

### Stage 1: Boot ROM

**Location**: Hardcoded in the SoC silicon (cannot be modified)

**Responsibilities**:
- Executes immediately after power-on or reset
- Minimal hardware initialization (clocks, pin muxing)
- Reads boot mode selection pins/fuses
- Determines boot device (SD, eMMC, QSPI, USB, etc.)
- Loads first bootloader stage from fixed offset
- Validates boot image header (IVT - Image Vector Table)
- Transfers control to loaded code

**Boot Device Selection**:
- SD/eMMC: Reads from offset 0x400 (1KB)
- QSPI/NOR: Reads from offset 0x0
- NAND: Reads from first good block
- USB: Enters serial download mode

**Image Format**:
- Must contain IVT (Image Vector Table)
- Boot data structure
- DCD (Device Configuration Data) - optional for i.MX 6/7
- Application code (SPL)

### Stage 2: SPL (Secondary Program Loader)

**File**: `u-boot-spl.bin` or `u-boot-spl-ddr.bin`

**Responsibilities**:
- DDR memory initialization (CRITICAL)
- Basic clock configuration
- UART initialization for debug output
- Load next stage (ATF or U-Boot) into DDR
- Minimal driver support (SD/eMMC)

**Size Constraints**:
- Must fit in internal SRAM (typically 128-256 KB)
- Highly optimized, minimal features
- No user interaction

**i.MX Specific**:
- i.MX 6/7: SPL loads U-Boot directly
- i.MX 8/9: SPL loads ATF first (secure boot chain)

### Stage 3: ARM Trusted Firmware (ATF) [i.MX 8/9 only]

**File**: `bl31.bin`

**Responsibilities**:
- Secure monitor running at EL3 (Exception Level 3)
- Power State Coordination Interface (PSCI)
- System Control and Management Interface (SCMI)
- Secure world initialization
- Load and validate OP-TEE (if present)
- Transfer control to U-Boot in non-secure world

**Build Source**:
- ARM Trusted Firmware repository
- NXP-specific platform code
- Configured for specific i.MX variant

### Stage 4: OP-TEE (Optional Secure OS)

**File**: `tee.bin`

**Responsibilities**:
- Trusted execution environment
- Secure storage
- Cryptographic operations
- DRM support
- Runs in secure world alongside normal world OS

### Stage 5: U-Boot Proper

**File**: `u-boot.bin` or `u-boot-nodtb.bin` + `u-boot.dtb`

**Responsibilities**:
- Complete hardware initialization
- Network, USB, storage drivers
- Boot menu and user interaction
- Environment variable management
- Load kernel, device tree, initramfs
- Pass boot arguments to kernel
- Support for boot scripts (boot.scr)

**Features**:
- FIT image support
- Verified boot (secure boot)
- Fastboot protocol
- DFU (Device Firmware Upgrade)
- Network boot (TFTP, NFS)

### Stage 6: Linux Kernel

**Files**: `Image`, `zImage`, or `uImage` + Device Tree Blob (`.dtb`)

Standard Linux kernel boot process.

---

## Bootable Image Components

### Primary Firmware Components

1. **imx-boot** (or **flash.bin**)
   - Container image combining all boot components
   - Generated by `imx-mkimage` tool
   - Flashed to boot media at specific offset
   - Contains proper headers for Boot ROM

2. **System Controller Firmware (i.MX 8)**
   - **SCFW** (`scfw_tcm.bin`): System Controller Firmware (i.MX 8QM/QXP)
   - **SECO** (`mx8qm-ahab-container.img`): Security Controller
   - Manages power domains, clocks, resources

3. **Cortex-M Firmware (i.MX 8ULP/93)**
   - **m33_image.bin**: Cortex-M33 firmware
   - **upower.bin**: μPower firmware for power management

4. **DDR Firmware (i.MX 8M family)**
   - **lpddr4_pmu_train_*.bin**: DDR training firmware
   - Embedded in SPL or loaded separately

### Component Architecture

```
┌────────────────────────────────────────────────────────┐
│              imx-boot / flash.bin                      │
│  (Composite bootable image for NXP i.MX SoCs)         │
└────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐    ┌──────────┐    ┌──────────┐
   │  IVT    │    │   Boot   │    │   DCD    │
   │ Header  │    │   Data   │    │ (i.MX6/7)│
   └─────────┘    └──────────┘    └──────────┘
        │
        ▼
   ┌─────────────────────────────────────────┐
   │         SPL (u-boot-spl.bin)            │
   │  ┌───────────────────────────────────┐  │
   │  │ DDR initialization code           │  │
   │  │ Basic drivers (SD/eMMC)           │  │
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
        │
        ▼
   ┌─────────────────────────────────────────┐
   │   Firmware (i.MX 8 specific)            │
   │  ┌───────────────────────────────────┐  │
   │  │ SCFW (scfw_tcm.bin)               │  │
   │  │ SECO (ahab-container.img)         │  │
   │  │ DDR Training FW (lpddr4_pmu_*.bin)│  │
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
        │
        ▼
   ┌─────────────────────────────────────────┐
   │     ARM Trusted Firmware (bl31.bin)     │
   │  ┌───────────────────────────────────┐  │
   │  │ Secure monitor (EL3)              │  │
   │  │ PSCI implementation               │  │
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
        │
        ▼
   ┌─────────────────────────────────────────┐
   │   OP-TEE (tee.bin) - Optional           │
   │  ┌───────────────────────────────────┐  │
   │  │ Secure OS                         │  │
   │  │ Trusted Applications              │  │
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
        │
        ▼
   ┌─────────────────────────────────────────┐
   │     U-Boot Proper (u-boot.bin)          │
   │  ┌───────────────────────────────────┐  │
   │  │ Device drivers                    │  │
   │  │ Boot scripts                      │  │
   │  │ Environment variables             │  │
   │  │ u-boot.dtb (device tree)          │  │
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
```

---

## Image Generation Process

### Overview

The bootable image generation involves:
1. Building individual firmware components
2. Using `imx-mkimage` to combine components
3. Creating proper headers and padding
4. Generating final `imx-boot` or `flash.bin`

### Step-by-Step Process

#### Step 1: Build Firmware Components

**U-Boot (SPL + Proper)**:
```bash
# Configure for target board
make imx8mpevk_defconfig

# Build U-Boot
make -j$(nproc)

# Outputs:
# - u-boot-spl.bin (SPL)
# - u-boot-nodtb.bin (U-Boot without device tree)
# - u-boot.dtb (Device tree)
# - u-boot.bin (Combined U-Boot with DTB)
```

**ARM Trusted Firmware**:
```bash
# Build ATF for i.MX 8M Plus
make PLAT=imx8mp ARCH=aarch64 CROSS_COMPILE=aarch64-linux-gnu- bl31

# Output:
# - build/imx8mp/release/bl31.bin
```

**OP-TEE (Optional)**:
```bash
# Build OP-TEE OS
make PLATFORM=imx-mx8mpevk ARCH=arm CFG_ARM64_core=y

# Output:
# - out/arm-plat-imx/core/tee.bin
```

#### Step 2: Obtain NXP Firmware Blobs

NXP provides closed-source firmware required for certain SoCs:

```bash
# Download firmware-imx package
wget https://www.nxp.com/lgfiles/NMG/MAD/YOCTO/firmware-imx-8.x.bin

# Extract
chmod +x firmware-imx-8.x.bin
./firmware-imx-8.x.bin --auto-accept

# Files extracted:
# - firmware/ddr/synopsys/lpddr4_pmu_train_*.bin (DDR training)
# - firmware/hdmi/cadence/signed_*.bin (HDMI firmware)
```

#### Step 3: Use imx-mkimage Tool

The `imx-mkimage` tool combines all components into a bootable image.

**Clone imx-mkimage**:
```bash
git clone https://github.com/nxp-imx/imx-mkimage.git
cd imx-mkimage
```

**Prepare build directory**:
```bash
# Copy firmware files to appropriate directory
# For i.MX 8M Plus:
cd iMX8M

# Copy U-Boot components
cp /path/to/u-boot/u-boot-spl.bin ./
cp /path/to/u-boot/u-boot-nodtb.bin ./u-boot.bin
cp /path/to/u-boot/u-boot.dtb ./fsl-imx8mp-evk.dtb
cp /path/to/u-boot/tools/mkimage ./mkimage_uboot

# Copy ATF
cp /path/to/atf/bl31.bin ./

# Copy DDR firmware
cp /path/to/firmware/ddr/synopsys/lpddr4_pmu_train_*.bin ./
```

**Build imx-boot**:
```bash
# For i.MX 8M Plus EVK
make SOC=iMX8MP flash_evk

# Output:
# - flash.bin (bootable image)
```

**Command variations**:
```bash
# i.MX 8M Quad
make SOC=iMX8MQ flash_evk

# i.MX 8M Mini
make SOC=iMX8MM flash_evk

# i.MX 8M Nano
make SOC=iMX8MN flash_evk

# i.MX 93
make SOC=iMX9 flash_singleboot_m33
```

#### Step 4: Flash to Boot Media

**SD Card**:
```bash
# Flash imx-boot to SD card at offset 33KB (0x400 * 512 = 1KB for some, 33KB typical)
# For i.MX 8M family:
sudo dd if=flash.bin of=/dev/sdX bs=1k seek=33 conv=fsync

# For i.MX 6/7:
sudo dd if=u-boot-with-spl.imx of=/dev/sdX bs=1k seek=1 conv=fsync
```

**eMMC** (from U-Boot):
```bash
# Load flash.bin to RAM via TFTP, USB, or SD
# Write to eMMC
mmc dev 0
setenv fastboot_dev mmc0
tftp ${loadaddr} flash.bin
mmc write ${loadaddr} 0x42 0x2000
```

**QSPI/NOR Flash**:
```bash
# Use U-Boot sf commands
sf probe
sf erase 0 0x200000
tftp ${loadaddr} flash.bin
sf write ${loadaddr} 0 ${filesize}
```

---

## Boot Media Layout

### SD/eMMC Layout

```
┌────────────────────────────────────────────────────────────┐
│                   Boot Media Layout                        │
│                (SD Card / eMMC)                            │
└────────────────────────────────────────────────────────────┘

Offset        Content                  Size        Notes
─────────────────────────────────────────────────────────────
0x0000        MBR/GPT                  512 bytes   Partition table
              (Reserved)               ~32 KB      
0x400         IVT Header               ---         i.MX 6/7
              (1 KB)                                
0x8400        imx-boot/flash.bin       ~1-4 MB     i.MX 8/9 (33 KB offset)
              (33 KB)                               Combined bootloader
              
~4 MB         Partition 1              Variable    Boot partition (FAT32)
              /boot                                 - Image/zImage (kernel)
                                                    - *.dtb (device trees)
                                                    - boot.scr (boot script)
                                                    
~100 MB+      Partition 2              Variable    Root filesystem (ext4)
              /                                     - Linux root filesystem
                                                    
(Optional)    Partition 3+             Variable    Additional partitions
                                                    - /home, /data, etc.
```

### Detailed Boot Region Layout (i.MX 8M Plus example)

```
imx-boot (flash.bin) Internal Structure:
────────────────────────────────────────────
Offset        Component                Size
0x0000        Padding                  ---
0x0000        HDMI/DP Firmware         ~80 KB
0x1F000       SPL (u-boot-spl.bin)     ~150 KB
0x4F000       DDR Training FW          ~40 KB
0x60000       ATF (bl31.bin)           ~60 KB
0x70000       U-Boot (u-boot.bin)      ~800 KB
0x140000      U-Boot DTB               ~50 KB
(sizes are approximate and vary by configuration)
```

---

## Processor-Specific Variations

### i.MX 6 Series (i.MX 6Q, 6DL, 6S, 6SX, 6UL, etc.)

**Boot Process**:
- Boot ROM → SPL → U-Boot → Kernel
- No ATF (single-core or simpler security)

**Image Format**:
- `u-boot-with-spl.imx` or `SPL` + `u-boot.img`
- IVT (Image Vector Table) required
- DCD (Device Configuration Data) for DDR init (optional in SPL)

**Tools**:
- `mkimage` with `-T imximage` option

**Flash Offset**:
- SD/eMMC: 1 KB (0x400 bytes)

### i.MX 7 Series (i.MX 7D, 7S, 7ULP)

**Boot Process**:
- Similar to i.MX 6
- i.MX 7ULP uses imx-mkimage (more like i.MX 8)

**Image Format**:
- `u-boot-with-spl.imx` for i.MX 7D/7S
- imx-boot for i.MX 7ULP

### i.MX 8 QuadMax / QuadXPlus (QM/QXP)

**Boot Process**:
- Boot ROM → SCFW/SECO → SPL → ATF → U-Boot → Kernel

**Special Components**:
- **SCFW** (System Controller Firmware): Manages system resources
- **SECO** (Security Controller): Secure enclave, authentication

**Image Format**:
- Container format with multiple images
- AHAB (Advanced High Assurance Boot) for secure boot

**Tools**:
- `imx-mkimage` with container support

### i.MX 8M Family (8MQ, 8MM, 8MN, 8MP)

**Boot Process**:
- Boot ROM → SPL → ATF → (OP-TEE) → U-Boot → Kernel

**DDR Training**:
- Requires LPDDR4 training firmware
- Embedded in SPL or loaded separately

**HDMI/DisplayPort** (i.MX 8MP):
- Requires HDMI firmware blob
- Loaded by SPL or U-Boot

**Flash Offset**:
- SD/eMMC: 33 KB (0x8400 bytes)

### i.MX 8ULP (Ultra Low Power)

**Boot Process**:
- Boot ROM → SPL → Cortex-M33 FW → ATF → U-Boot → Kernel

**Special Components**:
- **μPower** (upower.bin): Power management firmware
- **Cortex-M33 firmware**: Real-time co-processor

**Dual Boot**:
- Single boot mode (A35 only)
- Dual boot mode (M33 + A35)

### i.MX 9 Series (i.MX 93)

**Boot Process**:
- Boot ROM → SPL → Cortex-M33 FW → ATF → U-Boot → Kernel
- Similar to i.MX 8ULP but newer generation

**Features**:
- EdgeLock secure enclave
- Advanced power management
- Dual Cortex-A55 cores

---

## Yocto/BitBake Integration

### How Yocto Builds imx-boot

In Yocto/OpenEmbedded, the `imx-boot` recipe automates the image generation process.

**Recipe**: `meta-imx/meta-bsp/recipes-bsp/imx-mkimage/imx-boot_*.bb`

**Build Flow**:
```
BitBake Build Process
────────────────────────────────────────────────

1. u-boot recipe (recipes-bsp/u-boot/)
   └─> Builds u-boot-spl.bin, u-boot.bin, u-boot.dtb

2. arm-trusted-firmware recipe
   └─> Builds bl31.bin

3. firmware-imx recipe
   └─> Installs DDR, HDMI firmware blobs

4. imx-boot recipe
   ├─> Depends on: u-boot, atf, firmware-imx
   ├─> Stages all components to build directory
   ├─> Invokes imx-mkimage
   └─> Generates: imx-boot (symlink to flash.bin)

5. Image recipe (e.g., imx-image-full.bb)
   ├─> Includes imx-boot in deploy directory
   ├─> Creates WIC image with partitions
   └─> Output: *.wic (flashable disk image)
```

**Key Variables**:
```bash
# In local.conf or machine config:

# Boot loader type
UBOOT_CONFIG = "sd"  # or "qspi", "nand", "emmc"

# i.MX boot target
IMXBOOT_TARGETS = "flash_evk"

# Boot media
IMAGE_BOOT_FILES = "imx-boot"
```

**WIC Image Creation**:

Yocto uses WIC (Wic Image Creator) to generate complete disk images:

```bash
# WIC file example: imx-imx-boot-bootpart.wks.in
part u-boot --source rawcopy --sourceparams="file=imx-boot" --ondisk mmcblk --no-table --align 33
part /boot --source bootimg-partition --ondisk mmcblk --fstype=vfat --label boot --active --align 4096 --size 64M
part / --source rootfs --ondisk mmcblk --fstype=ext4 --label root --align 4096
```

**Deployment**:
```bash
# After build:
ls tmp/deploy/images/${MACHINE}/

# Files generated:
# - imx-boot (bootloader)
# - Image (kernel)
# - *.dtb (device trees)  
# - imx-image-full-*.wic.zst (complete disk image, compressed)
# - imx-image-full-*.wic.bmap (block map for fast flashing)

# Flash WIC image to SD card:
bmaptool copy imx-image-full-*.wic.zst /dev/sdX
# or
zstd -d imx-image-full-*.wic.zst
sudo dd if=imx-image-full-*.wic of=/dev/sdX bs=1M status=progress conv=fsync
```

### Build Commands

```bash
# Build only bootloader
bitbake imx-boot

# Build complete image
bitbake imx-image-full

# Build with specific configuration
MACHINE=imx8mpevk bitbake imx-image-core
```

---

## Troubleshooting

### Common Boot Issues

#### 1. Board Doesn't Boot (No Output)

**Possible Causes**:
- Wrong boot offset (33KB vs 1KB)
- Corrupted boot media
- Boot mode pins incorrectly set
- Incompatible firmware combination

**Debug Steps**:
```bash
# Verify image was written correctly
sudo dd if=/dev/sdX bs=1k skip=33 count=4096 | hexdump -C | head

# Check for IVT header magic (i.MX 8M):
# Should see: 0x41 0x00 0x00 0xD1 (IVT header)

# Re-flash with verbose output
sudo dd if=flash.bin of=/dev/sdX bs=1k seek=33 conv=fsync status=progress
```

#### 2. SPL Loads but U-Boot Fails

**Symptoms**:
- Serial output shows SPL banner
- Hangs or resets before U-Boot

**Possible Causes**:
- DDR configuration mismatch
- ATF missing or wrong version
- U-Boot address overlap

**Debug**:
- Enable SPL debug: `CONFIG_SPL_DEBUG=y`
- Check ATF is loaded: SPL should print "Jumping to ATF"
- Verify DDR training firmware is present

#### 3. U-Boot Starts but Kernel Fails to Load

**Possible Causes**:
- Wrong kernel format (Image vs zImage vs uImage)
- Missing or wrong device tree
- Boot partition not mounted
- Incorrect boot command

**Debug**:
```bash
# In U-Boot, check boot media:
mmc dev 0
mmc info
ls mmc 0:1  # List boot partition

# Verify kernel is present:
load mmc 0:1 ${loadaddr} Image
md ${loadaddr} 0x40  # Dump memory to verify

# Check device tree:
load mmc 0:1 ${fdt_addr} imx8mp-evk.dtb
fdt addr ${fdt_addr}
fdt print
```

#### 4. Secure Boot / HAB Failures

**Symptoms**:
- Boot stops with HAB event log
- "HAB Configuration: Closed" but image not signed

**Solution**:
- Sign boot images using CST (Code Signing Tool)
- Ensure all components in boot chain are signed
- Burn appropriate fuses (DO NOT DO IN DEVELOPMENT!)

### Debug Techniques

**Serial Console**:
- Always connect serial console for boot debugging
- UART1 is typically debug console
- 115200 8N1 settings

**Enable Verbose Output**:
```bash
# U-Boot build options:
CONFIG_LOG=y
CONFIG_LOGLEVEL=7
CONFIG_SPL_LOG=y

# Kernel command line:
console=ttymxc0,115200 earlycon loglevel=8
```

**Memory Dump**:
```bash
# In U-Boot, dump memory regions:
md.b ${loadaddr} 0x100  # Dump 256 bytes at load address

# Verify boot image components:
md.b 0x40200000 0x40    # SPL location (example)
md.b 0x40300000 0x40    # ATF location (example)
```

**Boot from USB (Serial Download)**:
- Set boot mode pins to serial download
- Use `uuu` (Universal Update Utility) tool
- Load imx-boot over USB for testing

```bash
# Using UUU tool:
sudo uuu -b sd flash.bin

# Or interactive:
sudo uuu
uuu> SDP: boot -f flash.bin
```

---

## References

### Official Documentation

- [NXP i.MX 8M Plus Reference Manual](https://www.nxp.com/docs/en/reference-manual/IMX8MPRM.pdf)
- [NXP i.MX Linux User's Guide](https://www.nxp.com/docs/en/user-guide/IMX_LINUX_USERS_GUIDE.pdf)
- [NXP i.MX Yocto Project User's Guide](https://www.nxp.com/docs/en/user-guide/IMX_YOCTO_PROJECT_USERS_GUIDE.pdf)

### Source Code Repositories

- [U-Boot for i.MX](https://github.com/nxp-imx/uboot-imx)
- [ARM Trusted Firmware](https://github.com/nxp-imx/imx-atf)
- [imx-mkimage Tool](https://github.com/nxp-imx/imx-mkimage)
- [meta-imx Yocto Layer](https://github.com/nxp-imx/meta-imx)

### Tools

- [Universal Update Utility (uuu)](https://github.com/nxp-imx/mfgtools) - USB flashing tool
- [Code Signing Tool (CST)](https://www.nxp.com/webapp/sps/download/license.jsp?colCode=IMX_CST_TOOL) - For secure boot
- [bmaptool](https://github.com/intel/bmap-tools) - Fast image flashing

### Community Resources

- [NXP i.MX Community](https://community.nxp.com/community/imx)
- [Yocto Project Documentation](https://docs.yoctoproject.org/)

---

## Appendix: Quick Reference Commands

### Build imx-boot (Manual)

```bash
# 1. Build U-Boot
cd u-boot-imx
make imx8mpevk_defconfig
make -j$(nproc)

# 2. Build ATF
cd arm-trusted-firmware
make PLAT=imx8mp bl31

# 3. Build imx-boot
cd imx-mkimage/iMX8M
cp u-boot/u-boot-spl.bin .
cp u-boot/u-boot-nodtb.bin u-boot.bin
cp u-boot/u-boot.dtb fsl-imx8mp-evk.dtb
cp atf/build/imx8mp/release/bl31.bin .
cp firmware-imx/firmware/ddr/synopsys/*.bin .
make SOC=iMX8MP flash_evk
```

### Flash to SD Card

```bash
# i.MX 8M family (33KB offset)
sudo dd if=flash.bin of=/dev/sdX bs=1k seek=33 conv=fsync

# i.MX 6/7 (1KB offset)
sudo dd if=u-boot-with-spl.imx of=/dev/sdX bs=1k seek=1 conv=fsync

# Complete WIC image
sudo bmaptool copy image.wic.zst /dev/sdX
```

### Yocto Build

```bash
# Setup build environment
source setup-environment build

# Configure machine
echo 'MACHINE = "imx8mpevk"' >> conf/local.conf

# Build image
bitbake imx-image-full

# Flash result
sudo bmaptool copy tmp/deploy/images/imx8mpevk/imx-image-full*.wic.zst /dev/sdX
```

---

*Document Version: 1.0*  
*Last Updated: 2026-01-30*
