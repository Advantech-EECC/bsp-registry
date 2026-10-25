# Advantech Rockchip BSP overlays

This directory contains **Advantech-specific KAS configuration fragments and machine overrides**
for Rockchip-based BSPs in this registry.

Use these fragments when you need to:

- Add Advantech-owned overlay layers on top of the upstream community Rockchip BSP.
- Select Advantech product machines (e.g. RSB-4810) while still using upstream Rockchip layer sets.

If you are looking for the **upstream community Rockchip** layer definitions and the Radxa
reference boards, see:

- `vendors/rockchip/`

## What's included

### KAS fragments (Advantech layers)

- `modular-bsp-rockchip.yml`
  - Adds the Advantech overlay layer `meta-modular-bsp-rockchip` from
    `https://github.com/Advantech-EECC/meta-modular-bsp-rockchip.git`, pinned to an explicit
    commit.

### Machine overrides

- `machine/rsb4810.yml`
  - Sets `machine: "rsb4810"` for the Advantech RSB-4810.

## Layer stack

| Layer | Source | Role |
|-------|--------|------|
| `meta-rockchip` | `https://git.yoctoproject.org/meta-rockchip` (branch `wrynose`) | community BSP: mainline U-Boot, `linux-yocto`, `rk3568.inc`, rkbin blobs, `wic` images |
| `meta-modular-bsp-rockchip` | `https://github.com/miketsukerman/meta-modular-bsp-rockchip.git` | Advantech machine configs and board devicetree wiring |

The overlay declares its own layer collection so that it can coexist with upstream:

```
BBFILE_COLLECTIONS               += "eecc-rockchip"
BBFILE_PRIORITY_eecc-rockchip     = "9"
LAYERSERIES_COMPAT_eecc-rockchip  = "wrynose"
LAYERDEPENDS_eecc-rockchip        = "core rockchip"
```

Two consequences matter for the registry:

- The collection name is `eecc-rockchip`, **not** `rockchip`, so it does not clash with upstream.
  Priority `9` is above upstream's unusually low `BBFILE_PRIORITY_rockchip = "1"`.

## BSPs in the registry

| Preset | Releases | Device | MACHINE | Machine config |
|--------|----------|--------|---------|----------------|
| `modular-bsp-rsb4810` | wrynose | `rsb4810` | `rsb4810` | `vendors/advantech-europe/rockchip/machine/rsb4810.yml` |

The buildable target name is `modular-bsp-rsb4810-wrynose`. It selects the `adv-rockchip-1.0.0` vendor
release and enables the `systemd`, `ipv6` and `usrmerge` features.

## Build

From the repository root:

```bash
# Fast config checkout/validation (no build)
bsp build modular-bsp-rsb4810-wrynose --checkout

# Full build
bsp build modular-bsp-rsb4810-wrynose

# Enter an interactive build shell
bsp shell modular-bsp-rsb4810-wrynose
```

## Flashing

The RK3568 machine include pulls in `rockchip-wic.inc`, which adds `wic` and `wic.bmap` to
`IMAGE_FSTYPES`. The registry's default flash configuration therefore works unchanged:

```bash
bsp flash modular-bsp-rsb4810-wrynose
```

This is equivalent to `bmaptool copy <image>.wic <device>`. The image can be written to an SD card
or to the eMMC; the `idbloader.img` and `u-boot.itb` stages are embedded in the `.wic` by the
upstream layer.

Note that the Rockchip *vendor* flashing flow (`update.img` with `rkdeveloptool` or
`upgrade_tool`) is **not** used here — this BSP is the mainline path and produces a normal
`wic` image.

## Binary blobs and licensing

`conf/machine/include/rk3568.inc` in upstream `meta-rockchip` sets `ROCKCHIP_CLOSED_TPL ?= "1"`
and routes TF-A and OP-TEE through the prebuilt `rockchip-rkbin` recipes:

| Component | Provider | Licence |
|-----------|----------|---------|
| DDR initialiser (TPL) | `rockchip-rkbin-ddr` | `Proprietary` |
| TF-A (BL31) | `rockchip-rkbin-tf-a` | `Proprietary` |
| OP-TEE | `rockchip-rkbin-optee-os` | `Proprietary` |

These come from [`rockchip-linux/rkbin`](https://github.com/rockchip-linux/rkbin). The upstream
licence text permits redistribution, so no `LICENSE_FLAGS_ACCEPTED` entry is required, but the
blobs must still be reviewed before shipping a product image.

This is exactly the same blob set already accepted by the `rock-3a` preset in
[`vendors/rockchip/README.md`](../../rockchip/README.md#binary-blobs-and-licensing). In
particular, this BSP does **not** pull the proprietary `rockchip-libmali` GPU driver
(`LICENSE = "CLOSED"`) — graphics are handled by Mesa (Panfrost) as on the other mainline
Rockchip presets.

## References

- Advantech RSB-4810 product page:
  https://www.advantech.com/en-us/products/single-board-computers/rsb-4810
- Overlay layer: https://github.com/Advantech-EECC/meta-modular-bsp-rockchip
- Upstream community Rockchip layer: https://git.yoctoproject.org/meta-rockchip
- rkbin binaries: https://github.com/rockchip-linux/rkbin
