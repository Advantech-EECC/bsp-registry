# Advantech MediaTek BSP overlays

This directory contains **Advantech-specific KAS configuration fragments and machine overrides**
for MediaTek-based BSPs in this registry.

Use these fragments when you need to:

- Add Advantech-owned overlay layers on top of the upstream MediaTek Rity BSP.
- Select Advantech product machines (e.g. RSB-3810) while still using upstream MediaTek layer sets.

If you are looking for the **upstream MediaTek Rity** layer definitions and EVK configs, see:

- `vendors/mediatek/`

## What’s included

### KAS fragments (Advantech layers)

- `mtk-rity-v25.0-scarthgap.yml`
  - Pulls in the upstream vendor fragment `vendors/mediatek/mtk-rity-v25.0-scarthgap.yml`.
  - This is the fragment referenced by the `mtk-rity-v25.0` vendor release in `bsp-registry.yml`.

- `modular-bsp-mediatek.yml`
  - Adds the Advantech overlay layer `meta-modular-bsp-mediatek` from
    `https://github.com/Advantech-EECC/meta-modular-bsp-mediatek.git`.

These fragments are intentionally small and are meant to be composed with a board machine
selection.

### Machine overrides

- `machine/rsb3810.yaml`
  - Sets `machine: "rsb3810"` for the RSB-3810 product family.

## Where it is used

The `rsb3810` device in `bsp-registry.yml` includes
`vendors/advantech-europe/mediatek/machine/rsb3810.yaml` to select the machine. The
`modular-bsp-rsb3810` preset pairs that device with the `mtk-rity-v25.0` vendor release for
Yocto Scarthgap.

## Build

From the repository root:

```bash
# Fast config checkout/validation (no build)
bsp build modular-bsp-rsb3810-scarthgap --checkout

# Full build
bsp build modular-bsp-rsb3810-scarthgap

# Enter an interactive build shell
bsp shell modular-bsp-rsb3810-scarthgap
```

## References

- Advantech RSB-3810 BSP notes:
  https://ess-wiki.advantech.com.tw/view/AIM-Linux/RSB-3810
