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

- `mtk-rity-v25.0-scarthgap.yaml`
  - Adds Advantech overlay layer:
    - `meta-modular-bsp-mediatek` from `https://gitlab.com/Advantech-EECC/meta-modular-bsp-mediatek.git`.

This fragment is intentionally small and is meant to be composed with the upstream vendor fragment
(`vendors/mediatek/mtk-rity-v25.0-scarthgap.yml`) and a board machine selection.

### Machine overrides

- `machine/rsb3810.yaml`
  - Sets `machine: "rom3810"` for the RSB-3810 product family.

## Where it is used

The registry BSP `adv-mbsp-oemtk-scarthgap-rsb3810` (configured by `adv-mbsp-oemtk-scarthgap-rsb3810.yaml`)
includes `vendors/advantech/mediatek/machine/rsb3810.yaml` to select the machine.

## Build

From the repository root:

```bash
# Fast config checkout/validation (no build)
python bsp.py build adv-mbsp-oemtk-scarthgap-rsb3810 --checkout

# Full build
python bsp.py build adv-mbsp-oemtk-scarthgap-rsb3810

# Enter an interactive build shell
python bsp.py shell adv-mbsp-oemtk-scarthgap-rsb3810
```

## References

- Advantech RSB-3810 BSP notes:
  https://ess-wiki.advantech.com.tw/view/AIM-Linux/RSB-3810
