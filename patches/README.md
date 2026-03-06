# BSP Patches Documentation

This directory contains patches that are applied to various layers in the BSP build process. Patches are organized by vendor and Yocto release version to ensure compatibility and maintainability.

## Table of Contents

1. [Directory Structure](#1-directory-structure)
2. [NXP Vendor Patches](#2-nxp-vendor-patches)
   - 2.1. [Kirkstone Release](#21-kirkstone-release)
   - 2.2. [Mickledore Release](#22-mickledore-release)
   - 2.3. [Scarthgap Release](#23-scarthgap-release)
   - 2.4. [Styhead Release](#24-styhead-release)
   - 2.5. [Walnascar Release](#25-walnascar-release)
3. [Feature Patches](#3-feature-patches)
   - 3.1. [OTA (Over-The-Air Updates)](#31-ota-over-the-air-updates)
     - 3.1.1. [OSTree Patches](#311-ostree-patches)
4. [How Patches Are Applied](#4-how-patches-are-applied)
5. [Contributing Patches](#5-contributing-patches)
6. [Maintenance Notes](#6-maintenance-notes)
7. [Author](#7-author)
8. [License](#8-license)

## 1. Directory Structure

```
patches/
├── nxp/                    # NXP vendor-specific patches
│   ├── kirkstone/         # Patches for Yocto Kirkstone release
│   ├── mickledore/        # Patches for Yocto Mickledore release
│   ├── scarthgap/         # Patches for Yocto Scarthgap release
│   ├── styhead/           # Patches for Yocto Styhead release
│   └── walnascar/         # Patches for Yocto Walnascar release
└── features/              # Feature-specific patches
    └── ota/               # Over-The-Air update features
        └── ostree/        # OSTree OTA implementation patches
```

## 2. NXP Vendor Patches

Patches in the `nxp/` directory address build issues, compatibility fixes, and hardware-specific configurations for NXP i.MX platforms across different Yocto releases.

### 2.1. Kirkstone Release

| Patch | Description | Affected Layer/Recipe |
|-------|-------------|----------------------|
| `0001-Fix-vulkan-loader-recipe.patch` | Adds `nobranch=1` to SRC_URI to fix git fetch error in vulkan-loader recipe | meta-sdk/recipes-graphics/vulkan |

**Purpose**: Resolves git fetch issues when building Vulkan graphics support.

### 2.2. Mickledore Release

| Patch | Description | Affected Layer/Recipe |
|-------|-------------|----------------------|
| `0001-Fix-deepview-rt-package-installation.patch` | Fixes shebang in deepview-modelclient script for proper Python 3 execution | meta-ml/recipes-libraries/deepview-rt |

**Purpose**: Ensures proper installation and execution of DeepView RT (runtime) package.

### 2.3. Scarthgap Release

| Patch | Description | Affected Layer/Recipe |
|-------|-------------|----------------------|
| `0001-Fix-dependency-names.patch` | Corrects dependency names (`sof-imx` to `firmware-sof-imx`) | meta-fsl-imx/conf/layer.conf |
| `0002-Fix-imx-image-full-postinstall-step.patch` | Creates missing `/lib/firmware/nxp/` directory before installing firmware files | meta-fsl-imx/recipes-fsl/images |

**Purpose**: Addresses build failures related to renamed firmware packages and image generation issues.

### 2.4. Styhead Release

| Patch | Description | Affected Layer/Recipe |
|-------|-------------|----------------------|
| `0001-Add-alsa-tools-to-dependencies-to-fix-build.patch` | Adds alsa-tools to mx93 build dependencies in gstreamer plugin | meta-imx-bsp/recipes-multimedia/gstreamer |

**Purpose**: Resolves missing dependency issues during audio stack builds for i.MX93.

### 2.5. Walnascar Release

The Walnascar release contains the most patches due to active development and support for newer hardware platforms.

| Patch | Description | Affected Layer/Recipe |
|-------|-------------|----------------------|
| `0001-meta-imx-folder-name-walnascar.patch` | Fixes folder path from `sources/` to `layers/` for meta-virtualization | meta-imx-sdk/dynamic-layers/virtualization-layer |
| `0002-Add-alsa-tools-to-dependencies-to-fix-build.patch` | Adds alsa-tools to mx93/mx943 build dependencies in gstreamer plugin | meta-imx-bsp/recipes-multimedia/gstreamer |
| `0003-Add-dependencies-for-imx95.patch` | Adds alsa-tools dependency for i.MX95 platform support | meta-imx-bsp/recipes-multimedia/gstreamer |
| `0004-Add-build-fix-for-mpv-package.patch` | Adds upstream status header to mplayer build fix patch | meta-oe/recipes-multimedia/mplayer |
| `0006-Add-upstream-status-for-a-patch.patch` | Adds upstream status header to fsl-rc-local autorun patch | meta-fsl-imx/recipes-fsl/fsl-rc-local |
| `0007-Add-imx95-aom5521-a1-machine-for-walnascar.patch` | Adds machine configuration for Advantech AOM-5521 A1 board | meta-fsl-imx/conf/machine |
| `0008-AOM5521-Backport-OEI-patches-from-scarthgap-for-A1.patch` | Backports OEI (OpenEmbedded Industrial) patches for AOM-5521 A1 board | meta-fsl-imx/recipes-bsp/imx-oei |
| `0009-Use-lf-6.12.34_2.1.0-branch.patch` | Updates onnxruntime recipe to use lf-6.12.34_2.1.0 branch | meta-imx-ml/recipes-libraries/onnxruntime |

**Purpose**: Supports i.MX95 hardware platforms, particularly the Advantech AOM-5521 boards, and ensures compatibility with the Walnascar Yocto release.

## 3. Feature Patches

### 3.1. OTA (Over-The-Air Updates)

Patches in the `features/ota/` directory enable and fix OTA update functionality using OSTree technology.

#### 3.1.1. OSTree Patches

| Patch | Description | Yocto Release |
|-------|-------------|---------------|
| `0001-Make-layer-compatible-with-yocto-styhead-release.patch` | Updates meta-updater layer for Styhead compatibility | Styhead |
| `0001-Make-layer-compatible-with-yocto-walnascar-release.patch` | Updates meta-updater layer for Walnascar compatibility | Walnascar |

**Key Changes**:
- Updates `WORKDIR` references to `UNPACKDIR` (new Yocto variable naming convention)
- Updates `LAYERSERIES_COMPAT` to match release codenames
- Fixes path references in image build classes and test cases
- Ensures proper OSTree repository and commit handling

**Affected Components**:
- `classes/image_types_ostree.bbclass` - OSTree image generation
- `classes/image_types_ota.bbclass` - OTA image packaging
- `conf/layer.conf` - Layer compatibility settings
- `lib/oeqa/selftest/cases/updater_qemux86_64.py` - OTA test cases
- `recipes-sota/aktualizr/aktualizr_git.bb` - Aktualizr OTA client recipe

## 4. How Patches Are Applied

Patches are automatically applied during the BSP build process based on:
1. **Vendor selection** - Determines which vendor subdirectory to use
2. **Yocto release** - Selects patches matching the target release version
3. **Features enabled** - Applies feature-specific patches when features are activated

The build system applies patches in numerical order (e.g., `0001-`, `0002-`, etc.) to ensure proper dependency resolution.

## 5. Contributing Patches

When adding new patches:

1. **Use descriptive names**: Follow the pattern `NNNN-Brief-description.patch`
2. **Include patch metadata**: Ensure Subject, From, and Date fields are present
3. **Organize by version**: Place patches in the appropriate Yocto release directory
4. **Document changes**: Update this README with patch description and purpose
5. **Test thoroughly**: Verify patches apply cleanly and don't break existing builds

## 6. Maintenance Notes

- Patches are maintained per Yocto release to ensure stability
- When upgrading to a new Yocto release, review and update patches as needed
- Some patches may become obsolete when issues are fixed upstream
- Regular review of patches is recommended to keep the patch set minimal

## 7. Author

All patches in this repository are authored by:
- **Mikhail Tsukerman** <mikhail.tsukerman@advantech.de>

Patches are maintained by the Advantech RISC SW Team.

## 8. License

Patches follow the same licensing as the components they modify. Refer to individual layer licenses for details.
