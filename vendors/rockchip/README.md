# Rockchip BSP (community `meta-rockchip`)

This directory contains the **Rockchip vendor BSP integration** for the Advantech BSP Registry.
It is based on the community
[`meta-rockchip`](https://git.yoctoproject.org/meta-rockchip) layer maintained by Trevor Woerner
on `git.yoctoproject.org`, which builds **mainline U-Boot and `linux-yocto`** and uses
**Mesa (Panfrost/Panthor)** for graphics.

> **Which `meta-rockchip`?** Two actively maintained layers share that name. This registry uses
> the Yocto-hosted, upstream-first one. The vendor layer
> [`github.com/JeffyCN/meta-rockchip`](https://github.com/JeffyCN/meta-rockchip) is a different
> layer (Rockchip BSP kernel 6.1, U-Boot 2017.09, proprietary `rockchip-libmali`) providing only
> `rockchip-*-evb` machines. It is **not** integrated here — see
> [Not integrated: the vendor layer](#not-integrated-the-vendor-layer).

## What's included

### KAS fragments (layers + pins)

- `rockchip-common.yml` — shared settings: image targets `core-image-base` and
  `core-image-full-cmdline`. No `distro` is set; the registry release supplies `poky`.
- `rockchip-scarthgap.yml` / `rockchip-walnascar.yml` / `rockchip-wrynose.yml` — pin
  `meta-rockchip` to the matching upstream branch and commit, and include `rockchip-common.yml`.

The layer depends only on `core` and `meta-arm` (`conf/layer.conf`:
`LAYERDEPENDS_rockchip = "core meta-arm"`). Both `meta-arm` and `meta-arm-toolchain` are already
provided by [`yocto/yocto.yaml`](../../yocto/yocto.yaml) and pinned per release by
[`yocto/releases/`](../../yocto/releases), so no extra layers are needed.

No patches from this repository are applied to the Rockchip layers.

### Reference machine configs

| File | MACHINE | SoC | Board |
|------|---------|-----|-------|
| `machine/rock-5b.yml` | `rock-5b` | RK3588 | Radxa ROCK 5B |
| `machine/rock-3a.yml` | `rock-3a` | RK3568 | Radxa ROCK 3A |
| `machine/rock-pi-4c.yml` | `rock-pi-4c` | RK3399 | Radxa ROCK Pi 4C |

All three are listed as *"builds and boots wic image"* in the upstream layer's `README`.

## BSPs in the registry

| Preset | Releases | Device | Machine config |
|--------|----------|--------|----------------|
| `rock-5b` | scarthgap, walnascar, wrynose | `rock-5b` | `vendors/rockchip/machine/rock-5b.yml` |
| `rock-3a` | scarthgap, walnascar, wrynose | `rock-3a` | `vendors/rockchip/machine/rock-3a.yml` |
| `rock-pi-4c` | scarthgap, walnascar, wrynose | `rock-pi-4c` | `vendors/rockchip/machine/rock-pi-4c.yml` |

A preset that declares `releases:` is addressed on the command line as `<preset>-<release>`, so
the buildable names are `rock-5b-scarthgap`, `rock-5b-walnascar`, and so on. All presets select
the `rockchip` vendor release.

## Build instructions

From the repository root:

```bash
# List available Rockchip BSPs
bsp list | grep -iE 'rock-'

# Fast config checkout/validation (no build)
bsp build rock-5b-scarthgap --checkout

# Full build
bsp build rock-5b-scarthgap

# Interactive build shell
bsp shell rock-5b-scarthgap
```

Build artifacts follow the standard Yocto layout:

`build/<bsp-name>/build/tmp/deploy/images/<machine>/`

## Flashing

`conf/machine/include/rockchip-wic.inc` sets `IMAGE_FSTYPES += "wic wic.bmap"`, so each build
produces a full GPT disk image plus its block map. This matches the registry's default
`flash.image_patterns` and `deploy.patterns` with no configuration changes:

```bash
bsp flash rock-5b-scarthgap
```

which is equivalent to `bmaptool copy <image>.wic <device>`. Plain `dd` also works. The bootloader
is written into the raw `loader1` (`idbloader.img`) and `loader2` (`u-boot.itb`) partitions by the
`rockchip.wks` layout, so no separate bootloader step is needed for SD/eMMC boot.

## Binary blobs and licensing

The graphics stack is open source — this layer ships no `libmali` and uses Mesa — but the boot
chain is not uniformly open:

| SoC | `ROCKCHIP_CLOSED_TPL` | TF-A / OP-TEE | Notes |
|-----|-----------------------|---------------|-------|
| RK3399 (`rock-pi-4c`) | not set | built from source (`meta-arm` TF-A, `TFA_PLATFORM = "rk3399"`) | **fully open-source boot path** |
| RK3568 (`rock-3a`) | `"1"` | `rockchip-rkbin` | proprietary DDR init, TF-A and OP-TEE blobs |
| RK3588/RK3588S (`rock-5b`) | `"1"` | `rockchip-rkbin` | proprietary DDR init, TF-A and OP-TEE blobs |

The blobs come from the `rockchip-rkbin` recipes under `recipes-bsp/rkbin` in the layer
(`LICENSE = "Proprietary"`), fetched from
[`rockchip-linux/rkbin`](https://github.com/rockchip-linux/rkbin). The upstream licence text does
permit redistribution, so no `LICENSE_FLAGS_ACCEPTED` entry is required, but the blobs must still
be reviewed before shipping a product image.

## Notes and limitations

- **Layer priority.** Upstream sets `BBFILE_PRIORITY_rockchip = "1"`, which is unusually low. It
  is left untouched here because nothing in this registry overlays the layer. Any future Rockchip
  overlay layer must raise the priority, or its `.bbappend` files will lose.
- **Release coverage.** Presets cover `scarthgap`, `walnascar` and `wrynose`. The layer also has
  `styhead` and `whinlatter` branches, but both are deliberately skipped: `styhead` is an EOL
  non-LTS release, and the `whinlatter` branch is a stub whose only commit is the
  `LAYERSERIES_COMPAT` bump, so it lacks fixes (notably the TF-A deploy fix) that later branches
  carry.
- **Board coverage varies per branch.** `soquartz-model-a` exists on `walnascar` but not
  `scarthgap`; `nanopc-t6` and `orangepi-3b` exist only on `wrynose` and `master`, so they would
  need their own `releases: [wrynose]` presets rather than being added to the existing ones. Check
  `conf/machine/` on the target branch before adding a board to a preset's `releases:` list.
- **No RK3576.** This layer has no RK3576 support; only the vendor layer provides it.
- **Features.** Presets enable only `systemd` and `ipv6`. Other registry features
  (`security`, `virtualization`, `ostree`, `rauc`) are untested on Rockchip and should be added
  per feature after a successful build. The layer does carry an optional RAUC A/B demo
  (`rk-rauc-demo`), which is not wired into the registry.

## Not integrated: the vendor layer

[`github.com/JeffyCN/meta-rockchip`](https://github.com/JeffyCN/meta-rockchip) would add RK3576
and the `rockchip-*-evb` machines plus vendor GPU/VPU support, but it requires
`INHERIT += "rockchip-image"`, emits `update.img`/`loader.bin` instead of `u-boot.itb`, generates
no `.bmap`, and pulls in `rockchip-libmali` with `LICENSE = "CLOSED"`. Adding it would be a
separate `rockchip-vendor` vendor release with its own licensing sign-off.

## References

- meta-rockchip (this layer): https://git.yoctoproject.org/meta-rockchip
- Rockchip partition layout: https://opensource.rock-chips.com/wiki_Partitions
- rkbin binaries: https://github.com/rockchip-linux/rkbin
- Radxa ROCK 5B: https://radxa.com/products/rock5/5b
- Radxa ROCK 3A: https://radxa.com/products/rock3/3a
- Radxa ROCK Pi 4: https://radxa.com/products/rock4
