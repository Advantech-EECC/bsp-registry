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
    `https://github.com/miketsukerman/meta-modular-bsp-rockchip.git`, pinned to an explicit
    commit.

- `rk3568-1.0.0-wrynose.yml`
  - Pulls in the upstream fragment [`vendors/rockchip/rockchip-wrynose.yml`](../../rockchip/rockchip-wrynose.yml)
    *and* the overlay above.
  - This is the fragment referenced by the `rk3568-1.0.0` vendor release in `bsp-registry.yml`.

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
- `LAYERSERIES_COMPAT` lists only `wrynose`, which is why the preset below offers that release
  and no other.

## BSPs in the registry

| Preset | Releases | Device | MACHINE | Machine config |
|--------|----------|--------|---------|----------------|
| `modular-bsp-rsb4810` | wrynose | `rsb4810` | `rsb4810` | `vendors/advantech-europe/rockchip/machine/rsb4810.yml` |

The buildable target name is `modular-bsp-rsb4810-wrynose`. It selects the `rk3568-1.0.0` vendor
release and enables the `systemd`, `ipv6` and `usrmerge` features.

## Hardware: Advantech RSB-4810

3.5" SBC built on the Rockchip RK3568 (quad-core Cortex-A55, arm64), with mainline `linux-yocto`
and mainline U-Boot. Debug console is `ttyS2` at 1500000 baud.

### Peripheral support

Status as reported by the overlay layer's own README. **Nothing in this table has been validated
on hardware by this registry.**

| Device | Status | Comment |
|--------|--------|---------|
| eMMC | ⚠️ | Not tested |
| SD card | ⚠️ | Not tested |
| ETH0 | ⚠️ | 1 Gbps (GMAC0, RTL8211F PHY), not tested |
| ETH1 | ⚠️ | 1 Gbps (GMAC1, RTL8211F PHY), not tested |
| USB 2.0 / USB 3.0 | ⚠️ | Not tested |
| HDMI | ⚠️ | Not tested |
| PCIe / M.2 / Mini-PCIe | ⚠️ | Not tested |
| UART | ⚠️ | Debug console expected on `ttyS2` @ 1500000 |
| I2C | ⚠️ | Not tested |
| Watchdog | ⚠️ | Internal watchdog not tested; EC watchdog needs porting |
| LVDS / eDP | ❌ | Needs porting from the vendor kernel |
| CAN | ❌ | Needs porting from the vendor kernel |
| RTC | ❌ | External RTC needs porting |
| Wi-Fi / Bluetooth | ❌ | M.2 module firmware packaging needed |

Legend: ✅ working, ⚠️ untested or partial, ❌ not yet supported.

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

## Status and limitations

- **Preliminary.** The overlay layer describes itself as preliminary support. No build or boot
  test of this preset has been performed; the peripheral table above is the layer author's own
  assessment.
- **`wrynose` only.** `LAYERSERIES_COMPAT_eecc-rockchip` lists no other release. Offering
  `scarthgap` or `walnascar` would require widening that and re-testing against the older
  upstream `meta-rockchip` branches.
- **Pinned to a feature branch.** The overlay is currently pinned by commit on the layer's
  `copilot/research-support-for-advantech-rsb-4810` branch, because the layer's `wrynose` branch
  does not yet carry the board support. The pinned commit is what KAS checks out, so builds are
  reproducible, but `branch:` in `modular-bsp-rockchip.yml` should be repointed to `wrynose` once
  the content is merged there.
- **Devicetree is not upstream.** `rk3568-rsb4810.dts` is carried by the overlay layer rather
  than by mainline Linux or U-Boot, and has not been verified against Advantech schematics.
- **U-Boot reuses the EVB defconfig.** `UBOOT_MACHINE = "evb-rk3568_defconfig"`, with the
  RSB-4810 devicetree substituted into the `OF_UPSTREAM` subtree.
- **No board-revision handling.** A single `rsb4810` machine is provided; Advantech's own naming
  suggests per-revision (A1/A2) board files may eventually be needed. RAM and storage variants
  would follow the per-variant machine pattern used by `meta-modular-bsp-nxp`.

## References

- Advantech RSB-4810 product page:
  https://www.advantech.com/en-us/products/single-board-computers/rsb-4810
- Overlay layer: https://github.com/miketsukerman/meta-modular-bsp-rockchip
- Upstream community Rockchip layer: https://git.yoctoproject.org/meta-rockchip
- rkbin binaries: https://github.com/rockchip-linux/rkbin
