# MediaTek BSP (Rity)

This directory contains the **MediaTek vendor BSP integration** for the Advantech BSP Registry.
The current integration is based on **MediaTek AIoT Rity** for **Yocto Scarthgap** and is intended
to be built through the registry manager (`bsp` CLI from `bsp-registry-tools`) which takes care of container selection,
cache variables, and the build directory layout.

## What’s included

### KAS fragments (layers + pins)

- `mtk-rity-v25.0-scarthgap.yml`
  - Pulls MediaTek Rity layers from GitLab and pins them to `refs/tags/rity-scarthgap-v25.0`.
  - Enables extra build features used by this registry:
    - `yocto/releases/scarthgap.yml` (base Yocto Scarthgap repos)
    - `compilers/clang/clang.yml`
    - `features/deep-learning/tensorflow.yml`
  - Applies local patches from this repository:
    - `patches/mediatek/scarthgap/0001-Fix-recipe-dtbo-name.patch`
    - `patches/mediatek/scarthgap/0002-Fix-git-checkout-for-arm-compute-library.patch`

### Reference machine configs

- `machine/genio-1200-evk.yml`
  - Machine: `genio-1200-evk`
  - Target image: `rity-demo-image`
  - Adds distro features required by the Rity demo distro:
    - `DISTRO_FEATURES += "wayland opengl vulkan"`
    - `LICENSE_FLAGS_ACCEPTED += "commercial"`

## BSPs in the registry

The top-level registry file `bsp-registry.yml` currently exposes the following MediaTek BSP build targets:

| Preset | Releases | Device | Machine config |
|--------|----------|--------|----------------|
| `mediatek-genio-1200-evk` | scarthgap | `genio-1200-evk` | `vendors/mediatek/machine/genio-1200-evk.yml` |
| `modular-bsp-rsb3810` | scarthgap | `rsb3810` | `vendors/advantech-europe/mediatek/machine/rsb3810.yaml` |

A preset that declares `releases:` is addressed on the command line as `<preset>-<release>`, so
the buildable names are `mediatek-genio-1200-evk-scarthgap` and `modular-bsp-rsb3810-scarthgap`.
The `modular-bsp-rsb3810` preset additionally selects the `mtk-rity-v25.0` vendor release, which
layers the Advantech overlay described in the
[Advantech MediaTek overlay README](../advantech-europe/mediatek/README.md) on top of upstream Rity.

## Build instructions (recommended)

From the repository root:

```bash
# List available BSPs
bsp list | grep -iE 'genio|rsb3810'

# Fast config checkout/validation (no build)
bsp build mediatek-genio-1200-evk-scarthgap --checkout

# Full build
bsp build mediatek-genio-1200-evk-scarthgap

# Enter an interactive build shell
bsp shell mediatek-genio-1200-evk-scarthgap

# Advantech RSB-3810 (upstream Rity + Advantech overlay)
bsp build modular-bsp-rsb3810-scarthgap
```

Build artifacts follow the standard Yocto layout under the registry build directory, e.g.:

`build/<bsp-name>/build/tmp/deploy/images/<machine>/`

## References

- MediaTek Genio 1200 EVK documentation:
  https://mediatek.gitlab.io/aiot/doc/aiot-dev-guide/master/hw/g1200-evk.html
- Upstream Rity layers (referenced by `mtk-rity-v25.0-scarthgap.yml`):
  - https://gitlab.com/mediatek/aiot/rity/
