# Advantech Qualcomm BSP overlays

This directory contains **Advantech-specific KAS configuration fragments and machine overrides**
for Qualcomm-based BSPs in this registry.

Use these fragments when you need to:

- Add Advantech-owned overlay layers on top of the upstream Qualcomm QLI BSP.
- Select Advantech product machines (e.g. AOM-2721) while still using upstream Qualcomm layer sets.

If you are looking for the **upstream Qualcomm QLI** layer definitions and EVK configs, see:

- `vendors/qualcomm/`

## What's included

### Machine overrides

- `machine/aom2721.yml`
  - Sets `machine: "aom2721"` for the Advantech AOM-2721 module (QCS6490-based).

## Where it is used

Machine config `vendors/advantech/qualcomm/machine/aom2721.yml` selects the Advantech AOM-2721
board when composing a full BSP alongside `vendors/qualcomm/qcom-6.6.97-qli.1.6-ver.1.2-scarthgap.yml`.

## Build

From the repository root:

```bash
# List available Qualcomm BSPs
python bsp.py list | grep -i qcom

# Fast config checkout/validation (no build)
python bsp.py build bsp-oeqcom-scarthgap-qcs6490-evk --checkout

# Full build
python bsp.py build bsp-oeqcom-scarthgap-qcs6490-evk

# Enter an interactive build shell
python bsp.py shell bsp-oeqcom-scarthgap-qcs6490-evk
```

## References

- Advantech AOM-2721 product page:
  [https://www.advantech.com/en/products/som/aom-2721](https://www.advantech.com/en-us/products/8fc6f753-ca1d-49f9-8676-10d53129570f/aom-2721/)
- Qualcomm QCS6490 SoC:
  [https://www.qualcomm.com/products/internet-of-things/industrial/building-enterprise/qcs6490](https://www.qualcomm.com/internet-of-things/products/q6-series/qcs6490)
