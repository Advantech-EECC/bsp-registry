# Advantech Qualcomm BSPs

## Modular BSP for AOM-5721

Preliminary support for the AOM-5721-A1-QCS6490 (8 GB) on the AOM-DB6700-A1
SMARC 2.2 carrier. The preset uses Yocto Wrynose, Qualcomm Linux 2.0,
the `qcom-distro` distribution and the
[Advantech overlay](https://github.com/Advantech-EECC/meta-modular-bsp-qcom/tree/4ef8934db02277944b7d7830367bf2c72f1651f2).

The preset composes the registry's `wrynose` release with the `qli-2.0`
vendor release (`vendors/advantech-europe/qualcomm/qcom-6.18.30-qli.2.0-wrynose.yml`). That
file includes the upstream QLI 2.0 layer set (`vendors/qualcomm/qcom-6.18.30-qli.2.0-wrynose.yml`,
pinned to the `qli-2.0` lock of `meta-qcom-releases`) plus the Advantech overlay
(`modular-bsp-qcom.yml`). The `qcom-distro` distribution is selected by the
`qualcomm` SoC-vendor override of the `wrynose` release in `bsp-registry.yml`.

From the registry root, run:

```sh
bsp build modular-bsp-aom5721-qcs6490-db6700-wrynose
```

The preset builds `core-image-minimal` and `qcom-multimedia-proprietary-image`.
See the [QLI 2.0 host requirements](https://github.com/qualcomm-linux/meta-qcom-releases/tree/qli-2.0).

### Flash the multimedia image to UFS

Set SW2 on the AOM-DB6700 to `100100` (recovery) and power-cycle the board.
From the registry root, run:

```sh
cd build/modular-bsp-aom5721-qcs6490-db6700/build/tmp/deploy/images/aom5721-qcs6490-db6700
cd qcom-multimedia-proprietary-image-aom5721-qcs6490-db6700.rootfs.qcomflash
qdl --storage ufs prog_firehose_ddr.elf rawprogram[0-9].xml patch[0-9].xml
```

Set SW2 to `100000` (UFS boot) and power-cycle again.

## Legacy BSP for AOM-2721

- `machine/aom2721.yml`
  - Sets `machine: "aom2721"` for the Advantech AOM-2721 module (QCS6490-based).

### Where it is used

Machine config `vendors/advantech-europe/qualcomm/machine/aom2721.yml` selects the Advantech
AOM-2721 board when composing a full BSP alongside
`vendors/qualcomm/qcom-6.6.97-qli.1.6-ver.1.2-scarthgap.yml`. It is registered as the `aom2721`
device in `bsp-registry.advantech-europe.yaml`.

### Status: preview

The `aom2721` device is defined in the registry but is **not yet wired into a preset**. It
therefore does not appear in `bsp list` and cannot be built with `bsp build <name>` yet. Until a
preset is added, compose the configuration manually with KAS (see below).

### Build

The registry ships Qualcomm presets for the upstream QCS/QCM machines (see
`vendors/qualcomm/README.md`); the closest match for this board is the QCS6490
RB3 Gen2 Vision Kit. From the repository root:

```bash
# List available Qualcomm BSPs
bsp list | grep -i qcs

# Fast config checkout/validation (no build)
bsp build qcs6490-rb3gen2-vision-kit-scarthgap --checkout

# Full build
bsp build qcs6490-rb3gen2-vision-kit-scarthgap

# Enter an interactive build shell
bsp shell qcs6490-rb3gen2-vision-kit-scarthgap
```

To exercise the AOM-2721 machine override before a preset exists, compose it directly with KAS:

```bash
kas build vendors/qualcomm/qcom-6.6.97-qli.1.6-ver.1.2-scarthgap.yml:vendors/advantech-europe/qualcomm/machine/aom2721.yml
```

### References

- Advantech AOM-2721 product page:
  [https://www.advantech.com/en/products/som/aom-2721](https://www.advantech.com/en-us/products/8fc6f753-ca1d-49f9-8676-10d53129570f/aom-2721/)
- Qualcomm QCS6490 SoC:
  [https://www.qualcomm.com/products/internet-of-things/industrial/building-enterprise/qcs6490](https://www.qualcomm.com/internet-of-things/products/q6-series/qcs6490)
