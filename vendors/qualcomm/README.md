# Qualcomm BSP (QLI)

This directory contains the **Qualcomm vendor BSP integration** for the Advantech BSP Registry.
The current integration is based on **Qualcomm Linux (QLI) v1.5** for **Yocto Scarthgap** and is
intended to be built through the registry manager (the `bsp` CLI from the `bsp-registry-tools`
package) which takes care of container selection, cache variables, and the build directory layout.

## What's included

### KAS fragments (layers + pins)

- `qcom-6.6.97-qli.1.6-ver.1.2-scarthgap.yml`
  - Pulls Qualcomm layers from GitHub and pins them to specific commits matching the
    [QLI 1.5 Ver.1.1 manifest](https://github.com/qualcomm-linux/qcom-manifest/blob/qcom-linux-scarthgap/qcom-6.6.97-QLI.1.6-Ver.1.2.xml):
    - `meta-qcom` (Linaro upstream)
    - `meta-qcom-hwe` (Qualcomm hardware enablement)
    - `meta-qcom-distro` (Qualcomm distribution layer)
  - Enables extra build features used by this registry:
    - `compilers/clang/clang.yml`
    - `features/deep-learning/tensorflow.yml`
    - `vendors/qualcomm/qualcomm-common.yml`

- `qualcomm-common.yml`
  - Sets the default distro (`qcom-wayland`) and target image (`qcom-console-image`).

### Reference machine configs

One include per upstream `meta-qcom-hwe` machine, each simply selecting the corresponding
`MACHINE`:

| Config | Machine | Evaluation kit |
| ------ | ------- | -------------- |
| `machine/qcm6490-idp.yml` | `qcm6490-idp` | QCM6490 IDP Beta EVK |
| `machine/qcs615-adp-air.yml` | `qcs615-adp-air` | QCS615 ADP Air Beta EVK |
| `machine/qcs615-iq-615-evk.yml` | `qcs615-iq-615-evk` | IQ-615 EVK |
| `machine/qcs6490-rb3gen2-core-kit.yml` | `qcs6490-rb3gen2-core-kit` | RB3 Gen2 Core Kit |
| `machine/qcs6490-rb3gen2-industrial-kit.yml` | `qcs6490-rb3gen2-industrial-kit` | RB3 Gen2 Industrial Kit |
| `machine/qcs6490-rb3gen2-vision-kit.yml` | `qcs6490-rb3gen2-vision-kit` | RB3 Gen2 Vision Kit |
| `machine/qcs8275-iq-8275-evk.yml` | `qcs8275-iq-8275-evk` | IQ-8275 EVK |
| `machine/qcs8275-iq-8275-evk-ifp.yml` | `qcs8275-iq-8275-evk-ifp` | IQ-8275 EVK, IFP variant |
| `machine/qcs8275-iq-8275-evk-pro-sku.yml` | `qcs8275-iq-8275-evk-pro-sku` | IQ-8275 EVK, Pro SKU |
| `machine/qcs8275-iq-8275-evk-pro-sku-ifp.yml` | `qcs8275-iq-8275-evk-pro-sku-ifp` | IQ-8275 EVK, Pro SKU IFP variant |
| `machine/qcs8300-ride-sx.yml` | `qcs8300-ride-sx` | Ride SX Beta EVK (QCS8300) |
| `machine/monaco-monza.yml` | `monaco-monza` | IQ-8300 EVK (Monaco Monza) |
| `machine/qcs9075-iq-9075-evk.yml` | `qcs9075-iq-9075-evk` | IQ-9075 EVK |
| `machine/qcs9075-iq-9075-evk-ifp.yml` | `qcs9075-iq-9075-evk-ifp` | IQ-9075 EVK, IFP variant |
| `machine/qcs9075-ride-sx.yml` | `qcs9075-ride-sx` | Ride SX Beta EVK (QCS9075) |
| `machine/qcs9100-ride-sx.yml` | `qcs9100-ride-sx` | Ride SX Beta EVK (QCS9100) |

## BSPs in the registry

The top-level registry file `bsp-registry.yml` exposes one preset per machine listed above, named
after the machine, e.g. `qcs6490-rb3gen2-vision-kit`. A preset that declares `releases:` is
addressed on the command line as `<preset>-<release>`, so the buildable names are suffixed with the
release, e.g. `qcs6490-rb3gen2-vision-kit-scarthgap`. Run `bsp list | grep -i qualcomm` for the
full list.

### Preview devices (no preset yet)

The following device is defined in the registry but is not yet wired into a preset, so it
does not appear in `bsp list` and cannot be built with `bsp build`:

| Device | Description | Machine config |
|--------|-------------|----------------|
| `aom2721` | Advantech AOM-2721 (Qualcomm) | `vendors/advantech-europe/qualcomm/machine/aom2721.yml` |

## Build instructions (recommended)

From the repository root:

```bash
# List available Qualcomm BSPs
bsp list | grep -i qualcomm

# Fast config checkout/validation (no build)
bsp build qcs6490-rb3gen2-vision-kit-scarthgap --checkout

# Full build
bsp build qcs6490-rb3gen2-vision-kit-scarthgap

# Enter an interactive build shell
bsp shell qcs6490-rb3gen2-vision-kit-scarthgap
```

Build artifacts follow the standard Yocto layout under the registry build directory, e.g.:

`build/<bsp-name>/build/tmp/deploy/images/<machine>/`

## References

- Qualcomm Linux developer portal:
  https://docs.qualcomm.com/bundle/publicresource/topics/80-70015-254/introduction.html
- Upstream Qualcomm layers (referenced by `qcom-6.6.97-qli.1.6-ver.1.2-scarthgap.yml`):
  - https://github.com/Linaro/meta-qcom
  - https://github.com/qualcomm-linux/meta-qcom-hwe
  - https://github.com/qualcomm-linux/meta-qcom-distro
- QLI 1.5 Ver.1.1 manifest:
  [https://github.com/qualcomm-linux/qcom-manifest/blob/qcom-linux-scarthgap/qcom-6.6.97-qli.1.6-ver.1.2.xml](https://github.com/qualcomm-linux/qcom-manifest/blob/qcom-linux-scarthgap/qcom-6.6.97-QLI.1.6-Ver.1.2.xml)
