# BSP Patches Documentation

This directory contains patches that are applied to various layers in the BSP build process. Patches are organized by vendor and Yocto release version to ensure compatibility and maintainability.

Each table lists the KAS fragment that applies the patch, so the patch set can always be traced back to the configuration that consumes it.

## Table of Contents

1. [Directory Structure](#1-directory-structure)
2. [NXP Vendor Patches](#2-nxp-vendor-patches)
   - 2.1. [Kirkstone Release](#21-kirkstone-release)
   - 2.2. [Mickledore Release](#22-mickledore-release)
   - 2.3. [Scarthgap Release](#23-scarthgap-release)
   - 2.4. [Styhead Release](#24-styhead-release)
   - 2.5. [Walnascar Release](#25-walnascar-release)
   - 2.6. [Whinlatter Release](#26-whinlatter-release)
   - 2.7. [Wrynose Release](#27-wrynose-release)
3. [MediaTek Vendor Patches](#3-mediatek-vendor-patches)
   - 3.1. [Scarthgap Release](#31-scarthgap-release)
4. [Feature Patches](#4-feature-patches)
   - 4.1. [OTA (Over-The-Air Updates)](#41-ota-over-the-air-updates)
     - 4.1.1. [OSTree Patches](#411-ostree-patches)
5. [How Patches Are Applied](#5-how-patches-are-applied)
6. [Contributing Patches](#6-contributing-patches)
7. [Maintenance Notes](#7-maintenance-notes)
8. [Author](#8-author)
9. [License](#9-license)

## 1. Directory Structure

```
patches/
├── nxp/                    # NXP vendor-specific patches
│   ├── kirkstone/          # Patches for Yocto Kirkstone release
│   ├── mickledore/         # Patches for Yocto Mickledore release
│   ├── scarthgap/          # Patches for Yocto Scarthgap release
│   ├── styhead/            # Patches for Yocto Styhead release
│   ├── walnascar/          # Patches for Yocto Walnascar release
│   ├── whinlatter/         # Patches for Yocto Whinlatter release
│   └── wrynose/            # Patches for Yocto Wrynose release
├── mediatek/               # MediaTek vendor-specific patches
│   └── scarthgap/          # Patches for the Rity Scarthgap BSP
└── features/               # Feature-specific patches
    └── ota/                # Over-The-Air update features
        └── ostree/         # OSTree OTA implementation patches
```

The repository currently contains **24 patches**: 20 for NXP, 2 for MediaTek and 2 for the OSTree OTA feature.

## 2. NXP Vendor Patches

Patches in the `nxp/` directory address build issues, compatibility fixes, and hardware-specific configurations for NXP i.MX platforms across different Yocto releases.

### 2.1. Kirkstone Release

| Patch | Description | Affected Layer/Recipe | Applied by |
|-------|-------------|----------------------|------------|
| `nxp/kirkstone/0001-Fix-vulkan-loader-recipe.patch` | Adds `nobranch=1` to SRC_URI to fix git fetch error in vulkan-loader recipe | meta-sdk/recipes-graphics/vulkan | `vendors/advantech/nxp/imx-5.15.52-2.1.0-kirkstone.yml` |

**Purpose**: Resolves git fetch issues when building Vulkan graphics support.

### 2.2. Mickledore Release

| Patch | Description | Affected Layer/Recipe | Applied by |
|-------|-------------|----------------------|------------|
| `nxp/mickledore/0001-Fix-deepview-rt-package-installation.patch` | Fixes shebang in deepview-modelclient script for proper Python 3 execution | meta-ml/recipes-libraries/deepview-rt | `vendors/nxp/imx-6.1.22-2.0.0-mickledore.yml` |

**Purpose**: Ensures proper installation and execution of DeepView RT (runtime) package.

### 2.3. Scarthgap Release

| Patch | Description | Affected Layer/Recipe | Applied by |
|-------|-------------|----------------------|------------|
| `nxp/scarthgap/0001-Fix-dependency-names.patch` | Corrects dependency names (`sof-imx` to `firmware-sof-imx`) | meta-fsl-imx/conf/layer.conf | `vendors/advantech/nxp/imx-6.6.23-2.0.0-scarthgap.yml` |
| `nxp/scarthgap/0002-Fix-imx-image-full-postinstall-step.patch` | Creates missing `/lib/firmware/nxp/` directory before installing firmware files | meta-fsl-imx/recipes-fsl/images | `vendors/advantech/nxp/imx-6.6.36-2.1.0-scarthgap.yml` |

**Purpose**: Addresses build failures related to renamed firmware packages and image generation issues.

### 2.4. Styhead Release

| Patch | Description | Affected Layer/Recipe | Applied by |
|-------|-------------|----------------------|------------|
| `nxp/styhead/0001-Add-alsa-tools-to-dependencies-to-fix-build.patch` | Adds alsa-tools to mx93 build dependencies in gstreamer plugin | meta-imx-bsp/recipes-multimedia/gstreamer | `vendors/nxp/imx-6.12.3-1.0.0-styhead.yml` |
| `nxp/styhead/0002-tensorflow-lite-fix-build.patch` | Fixes the TensorFlow Lite 2.18.0 build | meta-imx-ml/recipes-libraries/tensorflow-lite | `vendors/nxp/imx-6.12.3-1.0.0-styhead.yml` |

**Purpose**: Resolves missing dependency issues during audio stack builds for i.MX93 and fixes the machine-learning stack build.

### 2.5. Walnascar Release

The Walnascar release contains the most patches due to active development and support for newer hardware platforms.

| Patch | Description | Affected Layer/Recipe | Applied by |
|-------|-------------|----------------------|------------|
| `nxp/walnascar/0001-meta-imx-folder-name-walnascar.patch` | Fixes folder path from `sources/` to `layers/` for meta-virtualization | meta-imx-sdk/dynamic-layers/virtualization-layer | `vendors/nxp/imx-6.12.20-2.0.0-walnascar.yml`, `vendors/nxp/imx-6.12.34-2.1.0-walnascar.yml` |
| `nxp/walnascar/0004-Add-build-fix-for-mpv-package.patch` | Adds upstream status header to mplayer build fix patch | meta-oe/recipes-multimedia/mplayer | `vendors/advantech/nxp/imx-6.12.20-2.0.0-walnascar.yml`, `vendors/advantech-aim-linux/imx-6.12.20-2.0.0-walnascar.yml` |
| `nxp/walnascar/0006-Add-upstream-status-for-a-patch.patch` | Adds upstream status header to fsl-rc-local autorun patch | meta-fsl-imx/recipes-fsl/fsl-rc-local | `vendors/advantech/nxp/imx-6.12.20-2.0.0-walnascar.yml` |
| `nxp/walnascar/0007-Add-imx95-aom5521-a1-machine-for-walnascar.patch` | Adds machine configuration for Advantech AOM-5521 A1 board | meta-fsl-imx/conf/machine | `vendors/advantech/nxp/imx-6.12.20-2.0.0-walnascar.yml` |
| `nxp/walnascar/0008-AOM5521-Backport-OEI-patches-from-scarthgap-for-A1.patch` | Backports OEI (OpenEmbedded Industrial) patches for AOM-5521 A1 board | meta-fsl-imx/recipes-bsp/imx-oei | `vendors/advantech/nxp/imx-6.12.20-2.0.0-walnascar.yml` |
| `nxp/walnascar/0009-Use-lf-6.12.34_2.1.0-branch.patch` | Updates onnxruntime recipe to use lf-6.12.34_2.1.0 branch | meta-imx-ml/recipes-libraries/onnxruntime | `vendors/advantech/nxp/imx-6.12.20-2.0.0-walnascar.yml`, `vendors/advantech-aim-linux/imx-6.12.20-2.0.0-walnascar.yml` |
| `nxp/walnascar/0010-Add-alsa-tools-to-dependencies-for-imx9.patch` | Adds alsa-tools to the i.MX9 gstreamer plugin and DSPC ASRC dependencies | meta-imx-bsp/recipes-multimedia | `vendors/nxp/imx-6.12.20-2.0.0-walnascar.yml`, `vendors/nxp/imx-6.12.34-2.1.0-walnascar.yml`, `vendors/nxp/imx-6.12.49-2.2.0-walnascar.yml` |
| `nxp/walnascar/0011-Remove-imx95-evk.inc.patch` | Removes the upstream `imx95-evk.inc` machine include so registry machine configs can define it | conf/machine/include | `vendors/nxp/imx-6.12.49-2.2.0-walnascar.yml` |

**Purpose**: Supports i.MX95 hardware platforms, particularly the Advantech AOM-5521 boards, and ensures compatibility with the Walnascar Yocto release.

### 2.6. Whinlatter Release

| Patch | Description | Affected Layer/Recipe | Applied by |
|-------|-------------|----------------------|------------|
| `nxp/whinlatter/0001-Remove-imx95-evk.inc.patch` | Removes the upstream `imx95-evk.inc` machine include so registry machine configs can define it | conf/machine/include | `vendors/nxp/imx-6.18.2-1.0.0-whinlatter.yml` |
| `nxp/whinlatter/0002-Add-alsa-tools-to-dependencies-for-imx9.patch` | Adds alsa-tools to the i.MX9 gstreamer plugin and DSPC ASRC dependencies | meta-imx-bsp/recipes-multimedia | `vendors/nxp/imx-6.18.2-1.0.0-whinlatter.yml` |
| `nxp/whinlatter/0003-gst-plugins-bad-add-alsa-tools-to-dependencies.patch` | Adds alsa-tools to the gst-plugins-bad 1.26.6 dependencies | meta-imx-bsp/recipes-multimedia/gstreamer | `vendors/nxp/imx-6.18.2-1.0.0-whinlatter.yml` |

**Purpose**: Carries the i.MX9 / i.MX95 audio and machine-configuration fixes forward to the Whinlatter release.

### 2.7. Wrynose Release

| Patch | Description | Affected Layer/Recipe | Applied by |
|-------|-------------|----------------------|------------|
| `nxp/wrynose/0001-Remove-imx95-evk.inc.patch` | Removes the upstream `imx95-evk.inc` machine include so registry machine configs can define it | conf/machine/include | `vendors/nxp/imx-6.18.20-2.0.0-wrynose.yml` |
| `nxp/wrynose/0002-Add-alsa-tools-to-dependencies-for-imx9.patch` | Adds alsa-tools to the i.MX9 gstreamer plugin and DSPC ASRC dependencies | meta-imx-bsp/recipes-multimedia | `vendors/nxp/imx-6.18.20-2.0.0-wrynose.yml` |
| `nxp/wrynose/0003-gst-plugins-bad-add-alsa-tools-to-dependencies.patch` | Adds alsa-tools to the gst-plugins-bad 1.26.6 dependencies | meta-imx-bsp/recipes-multimedia/gstreamer | `vendors/nxp/imx-6.18.20-2.0.0-wrynose.yml` |

**Purpose**: Carries the i.MX9 / i.MX95 audio and machine-configuration fixes forward to the Wrynose release.

## 3. MediaTek Vendor Patches

Patches in the `mediatek/` directory fix recipe and fetch issues in the MediaTek AIoT Rity BSP.

### 3.1. Scarthgap Release

| Patch | Description | Affected Layer/Recipe | Applied by |
|-------|-------------|----------------------|------------|
| `mediatek/scarthgap/0001-Fix-recipe-dtbo-name.patch` | Renames the `dtbo` bbappend to `dtbo_%.bbappend` so the append matches the recipe | meta-rity-skeleton/recipes-kernel/dtbo | `vendors/mediatek/mtk-rity-v25.0-scarthgap.yml` |
| `mediatek/scarthgap/0002-Fix-git-checkout-for-arm-compute-library.patch` | Fixes the git checkout of the arm-compute-library 24.02 recipe | recipes-armnn/arm-compute-library | `vendors/mediatek/mtk-rity-v25.0-scarthgap.yml` |

**Purpose**: Makes the Rity v25.0 layer set build cleanly against Yocto Scarthgap.

## 4. Feature Patches

### 4.1. OTA (Over-The-Air Updates)

Patches in the `features/ota/` directory enable and fix OTA update functionality using OSTree technology.

#### 4.1.1. OSTree Patches

| Patch | Description | Yocto Release | Applied by |
|-------|-------------|---------------|------------|
| `features/ota/ostree/0001-Make-layer-compatible-with-yocto-styhead-release.patch` | Updates meta-updater layer for Styhead compatibility | Styhead | `features/ota/ostree/ostree-styhead.yml` |
| `features/ota/ostree/0001-Make-layer-compatible-with-yocto-walnascar-release.patch` | Updates meta-updater layer for Walnascar compatibility | Walnascar | `features/ota/ostree/ostree-walnascar.yml` |

**Key Changes**:
- Updates `WORKDIR` references to `UNPACKDIR` (new Yocto variable naming convention)
- Updates `LAYERSERIES_COMPAT` to match release codenames
- Fixes path references in image build classes and test cases
- Ensures proper OSTree repository and commit handling

**Affected Components** (all inside the upstream `meta-updater` layer):
- `classes/image_types_ostree.bbclass` - OSTree image generation
- `classes/image_types_ota.bbclass` - OTA image packaging
- `conf/layer.conf` - Layer compatibility settings
- `lib/oeqa/selftest/cases/updater_qemux86_64.py` - OTA test cases
- `recipes-sota/aktualizr/aktualizr_git.bb` - Aktualizr OTA client recipe

## 5. How Patches Are Applied

Patches are applied by KAS through the `patches:` key of a repository entry in a KAS fragment, for example:

```yaml
repos:
  meta-imx:
    patches:
      alsa-tools:
        repo: this
        path: patches/nxp/whinlatter/0002-Add-alsa-tools-to-dependencies-for-imx9.patch
```

Which fragment gets included — and therefore which patches get applied — is determined by:

1. **Vendor selection** - The device's `vendor` picks the vendor include set
2. **Yocto release** - The release entry's `vendor_overrides` select the release-specific fragment
3. **Vendor release** - A preset's `vendor_release` selects a specific BSP revision (e.g. `imx-6.12.34-2.1.0`)
4. **Features enabled** - Feature fragments such as `features/ota/ostree/ostree-walnascar.yml` bring their own patches

The build system applies patches in numerical order (e.g., `0001-`, `0002-`, etc.) to ensure proper dependency resolution.

## 6. Contributing Patches

When adding new patches:

1. **Use descriptive names**: Follow the pattern `NNNN-Brief-description.patch`
2. **Include patch metadata**: Ensure Subject, From, and Date fields are present
3. **Organize by version**: Place patches in the appropriate vendor and Yocto release directory
4. **Wire it up**: Reference the patch from the KAS fragment that should apply it
5. **Document changes**: Update this README with the patch description, purpose and applying fragment
6. **Test thoroughly**: Verify patches apply cleanly and don't break existing builds

`scripts/check-docs-consistency.py` fails if a patch file is not mentioned in this README, or if the
patch count stated in the root `README.md` does not match the number of patch files.

## 7. Maintenance Notes

- Patches are maintained per Yocto release to ensure stability
- When upgrading to a new Yocto release, review and update patches as needed
- Some patches may become obsolete when issues are fixed upstream
- Regular review of patches is recommended to keep the patch set minimal
- Patch numbers are not contiguous within a directory; gaps are expected where obsolete patches were dropped

## 8. Author

All patches in this repository are authored by:
- **Mikhail Tsukerman** <mikhail.tsukerman@advantech.de>

Patches are maintained by the Advantech RISC SW Team.

## 9. License

Patches follow the same licensing as the components they modify. Refer to individual layer licenses for details.
