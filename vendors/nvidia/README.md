# NVIDIA Jetson BSP (OE4T meta-tegra / tegra-demo)

This directory contains the **NVIDIA Jetson vendor BSP integration** for the Advantech BSP
Registry. It is based on the community **[OE4T](https://github.com/OE4T)** layers
(`meta-tegra`, `meta-tegra-community`) and the full **`tegra-demo-distro`** distribution
(`tegrademo`). Builds are driven through the registry manager (`bsp`) which selects the
container, cache variables and build directory layout.

## What's included

### Vendor common (`nvidia-common.yml`)

- Sets the distro to `tegrademo` (the full OE4T demo distribution).
- Default image targets: `demo-image-base` and `demo-image-full`.
- Accepts the `commercial` license flag required by the proprietary NVIDIA L4T / CUDA
  components.

### KAS layer-pin fragments

Each fragment pins `meta-tegra`, `meta-tegra-community` and `tegra-demo-distro` (which also
provides `meta-tegrademo`, `meta-tegra-support` and `meta-demo-ci`) to a specific commit on
the matching OE4T branch, and enables `meta-virtualization` (disabled by default) for the
docker demo images.

| Fragment | OE4T branch | JetPack / L4T | Boards |
|----------|-------------|---------------|--------|
| `tegra-jp5-scarthgap.yml` | `scarthgap-l4t-r35.x` | JetPack 5 / L4T r35.x | Xavier + Orin |
| `tegra-jp6-scarthgap.yml` | `scarthgap`           | JetPack 6 / L4T r36.x | Orin |
| `tegra-styhead.yml`       | `styhead`             | JetPack 6 / L4T r36.x | Orin |
| `tegra-walnascar.yml`     | `walnascar`           | JetPack 6 / L4T r36.x | Orin |
| `tegra-whinlatter.yml`    | `whinlatter`          | JetPack 6 / L4T r36.x | Orin |
| `tegra-wrynose.yml`       | `wrynose`             | JetPack 6 / L4T r36.x | Orin |

> **Xavier is JetPack 5 only.** NVIDIA's Xavier (T194) support lives on the OE4T
> `*-l4t-r35.x` branches, which only exist for `kirkstone` and `scarthgap`. There is no
> `styhead`/`walnascar`/`whinlatter`/`wrynose` r35.x branch, so Xavier is exposed on
> `scarthgap` (JetPack 5) only. Orin (JetPack 6) is available across scarthgap → wrynose.

### Reference machine configs (`machine/`)

- Orin: `jetson-agx-orin-devkit`, `jetson-orin-nano-devkit`, `jetson-orin-nano-devkit-nvme`
- Xavier (JetPack 5 only): `jetson-agx-xavier-devkit`, `jetson-xavier-nx-devkit`

## BSPs in the registry

The top-level `bsp-registry.yml` exposes these NVIDIA presets:

| Preset | Releases | Vendor release |
|--------|----------|----------------|
| `jetson-agx-orin-devkit`       | scarthgap, styhead, walnascar, whinlatter, wrynose | `tegra` (JetPack 6) |
| `jetson-orin-nano-devkit`      | scarthgap, styhead, walnascar, whinlatter, wrynose | `tegra` (JetPack 6) |
| `jetson-orin-nano-devkit-nvme` | scarthgap, styhead, walnascar, whinlatter, wrynose | `tegra` (JetPack 6) |
| `jetson-agx-xavier-devkit`     | scarthgap | `tegra-jp5` (JetPack 5) |
| `jetson-xavier-nx-devkit`      | scarthgap | `tegra-jp5` (JetPack 5) |

## Build instructions

From the repository root:

```bash
# List available NVIDIA BSPs
bsp --local list | grep -i jetson

# Fast config checkout/validation (no build)
bsp --local build jetson-agx-orin-devkit-scarthgap --checkout

# Full build
bsp --local build jetson-agx-orin-devkit-scarthgap

# Interactive build shell
bsp --local shell jetson-agx-orin-devkit-scarthgap
```

Build artifacts follow the standard Yocto layout, e.g.:

`build/<bsp-name>/build/tmp/deploy/images/<machine>/`

## Notes and limitations

- **Proprietary components / licensing:** the Jetson BSP downloads NVIDIA L4T binaries that
  require accepting NVIDIA's end-user license. Some components are fetched from NVIDIA's
  servers; fully reproducible/CI builds may need a mirror (`NVIDIA_DEVNET_MIRROR`) and
  additional host setup.
- **Flashing:** Jetson devices use NVIDIA's `tegraflash` workflow, which differs from the
  registry's generic `bmaptool`/`wic` flash flow. Producing a flashable bundle may require
  follow-up configuration.

## References

- OE4T project: https://github.com/OE4T
- meta-tegra: https://github.com/OE4T/meta-tegra
- meta-tegra-community: https://github.com/OE4T/meta-tegra-community
- tegra-demo-distro: https://github.com/OE4T/tegra-demo-distro
- OE4T documentation: https://oe4t.github.io/master/
