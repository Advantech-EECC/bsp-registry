# Secure Boot for Advantech Europe NXP Boards

This document describes the **two secure-boot implementations** available for
Advantech Europe NXP-based boards, plus optional **root filesystem encryption**.
Both implementations activate boot-image signing via NXP's HAB (i.MX8 family) or
AHAB (i.MX9 / i.MX95 family) technology:

* **`secure-boot`** — the original feature, based on NXP's `meta-secure-boot` layer
  from `meta-nxp-security-reference-design`.
* **`adv-secure-boot`** and **`rootfs-encryption`** — based on the Advantech
  [meta-modular-bsp-extra](https://github.com/Advantech-EECC/meta-modular-bsp-extra)
  layers (`meta-secure-boot-nxp`, `meta-rootfs-enc-core`, `meta-rootfs-enc-nxp`).

| | `secure-boot` | `adv-secure-boot` / `rootfs-encryption` |
|---|---|---|
| Layer | `meta-secure-boot` (meta-nxp-security-reference-design) | `meta-secure-boot-nxp` (+ `meta-rootfs-enc-*`) from meta-modular-bsp-extra |
| Signing inputs | `CST_TOOL_PATH` | `CST_TOOL_PATH`, `SIG_DATA_PATH`, `FACTORY_KEYS_DIR` (encryption) |
| Build targets | `imx-image-*-secure-boot` | normal targets (`imx-image-full`, `core-image-minimal`, …) |
| Rootfs encryption | no | yes (`rootfs-encryption`) |
| Container env | `ubuntu-22.04-csb` | `ubuntu-22.04-adv-sb` |

> ⚠️ **Never combine the two implementations in one preset.** Both layer sets
> bbappend `u-boot-imx`, `imx-boot` and `linux-imx`; enabling `secure-boot`
> together with `adv-secure-boot` or `rootfs-encryption` produces duplicate,
> conflicting signing steps.

---

## Table of Contents

- [Overview](#overview)
- [HAB vs AHAB](#hab-vs-ahab)
- [Advantech Secure Boot (meta-modular-bsp-extra)](#advantech-secure-boot-meta-modular-bsp-extra)
- [Root Filesystem Encryption](#root-filesystem-encryption)
- [Supported Boards](#supported-boards)
- [Prerequisites](#prerequisites)
  - [Obtaining the NXP Code Signing Tool (CST)](#obtaining-the-nxp-code-signing-tool-cst)
  - [Generating SRK Keys and Certificates](#generating-srk-keys-and-certificates)
- [Environment Variables](#environment-variables)
- [Building a Signed Image](#building-a-signed-image)
- [Flashing](#flashing)
- [Fusing / Provisioning the Board](#fusing--provisioning-the-board)
  - [i.MX8 HAB Fusing](#imx8-hab-fusing)
  - [i.MX9 / i.MX95 AHAB Fusing](#imx9--imx95-ahab-fusing)
- [CI / Azure Pipelines](#ci--azure-pipelines)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## Overview

Secure boot ensures that only cryptographically signed firmware runs on the SoC,
preventing execution of unauthorised code from the moment the ROM bootstrap loader
runs. The chain of trust covers:

```
ROM (immutable, on-chip)
  └─► SPL / First-stage bootloader  (signed)
        └─► U-Boot / ATF / OP-TEE  (signed)
              └─► Linux kernel       (optionally signed via IMA or UEFI Secure Boot)
```

The `secure-boot` feature activates the `meta-secure-boot` Yocto layer from the
`meta-nxp-security-reference-design` repository, which is already referenced (but
disabled by default) in `vendors/advantech-europe/nxp/modular-bsp-nxp.yml`.

The `adv-secure-boot` and `rootfs-encryption` features activate the
`meta-secure-boot-nxp`, `meta-rootfs-enc-core` and `meta-rootfs-enc-nxp` layers
from the `meta-modular-bsp-extra` repository, which is likewise declared (and
disabled by default) in the same vendor fragment and pinned per release. The
layers are activated purely by being added to `bblayers` — there is no
`DISTRO_FEATURES` switch. They support the scarthgap, styhead, walnascar,
whinlatter and wrynose releases (**not** kirkstone).

---

## HAB vs AHAB

| **Feature**          | HAB (High Assurance Boot)         | AHAB (Advanced High Assurance Boot) |
|------------------|-----------------------------------|-------------------------------------|
| **SoC family**   | i.MX8 (mx8m, mx8mp, mx8ulp, …)   | i.MX9, i.MX93, i.MX95              |
| **CST version**  | 3.x (any)                         | 3.4.0 or later                      |
| **Signed images**| SPL, U-Boot, kernel FIT           | Container images (SPL, ATF, U-Boot) |
| **Key type**     | RSA-4096 / ECDSA-521              | RSA-4096 / ECDSA-521                |
| **BitBake var**  | `IMX_HAB_ENABLE = "1"`            | `IMX_AHAB_ENABLE = "1"`             |
| **BB override**  | `:mx8-nxp-bsp`                    | `:mx9-nxp-bsp`                      |

The BSP registry selects the correct path automatically via the BSP-specific BitBake
machine overrides (`:mx8-nxp-bsp` / `:mx9-nxp-bsp` injected by
`MACHINEOVERRIDES_EXTENDER` in `meta-freescale`). The old plain `:mx8` / `:mx9`
overrides are filtered out and will produce a QA error if used. No manual selection
is needed.

> For the Advantech layers, AHAB works best on Yocto ≥ walnascar; that is why the
> shipped AHAB presets only list walnascar, whinlatter and wrynose.

---

## Advantech Secure Boot (meta-modular-bsp-extra)

The `adv-secure-boot` feature enables the `meta-secure-boot-nxp` layer, a drop-in
replacement for NXP's `meta-secure-boot`. It signs the **bootloader**
(SPL/U-Boot via `imx-boot` on HABv4, the boot container on AHAB) and the
**kernel**. On AHAB it additionally adds the signed Application OS container to
`IMAGE_BOOT_FILES` so the kernel is authenticated by AHAB at boot.

Unlike the NXP reference design, the layer bbappends the **standard** image
recipes (`core-image-minimal`, `core-image-base`, `core-image-sato`,
`fsl-image-machine-test`, `imx-image-core`, `imx-image-multimedia`,
`imx-image-full`), so you build the normal image names — there are no
`imx-image-*-secure-boot` targets.

The feature is wired through the registry as an advantech-europe/NXP vendor
override of `features/secure-boot/adv-secure-boot-nxp.yml`, which enables the
layer and sets defaults for the two required BitBake inputs:

* **`SIG_TOOL_PATH`** — directory of the NXP CST signer (e.g. `/opt/cst-4.0.1`
  on the host; `/opt/cst` inside the build container).
* **`SIG_DATA_PATH`** — your PKI directory. For **HABv4** it must contain
  `csf_hab4.cfg` plus the CST `crts/` and `keys/` subdirectories; for **AHAB**
  it must contain `csf_ahab.cfg` (and optionally an
  [`spsdk_ahab.yaml`](https://github.com/Advantech-EECC/meta-modular-bsp-extra/tree/main/meta-secure-boot-nxp)
  to use the SPSDK signer instead of CST). See the
  [`meta-secure-boot-nxp/README.md`](https://github.com/Advantech-EECC/meta-modular-bsp-extra/blob/main/meta-secure-boot-nxp/README.md)
  in the extra repository for the full PKI generation walk-through, and NXP's
  u-boot HABv4/AHAB guides (see [References](#references)).

> **CST vs SPSDK:** both signers are supported on AHAB. CST is recommended for
> rootfs-encryption builds because SPSDK is slow when signing large images.

---

## Root Filesystem Encryption

The `rootfs-encryption` feature enables the `meta-rootfs-enc-core` and
`meta-rootfs-enc-nxp` layers **on top of** `meta-secure-boot-nxp`
(`meta-rootfs-enc-nxp` declares `LAYERDEPENDS` on both), so
**rootfs encryption always implies Advantech Secure Boot** — the registry
feature includes both KAS fragments automatically.

What it provides:

* The root filesystem is encrypted with **dm-crypt**. The volume key is
  protected by the **CAAM** backend on HABv4 and AHAB-CAAM SoCs, or by a
  **trusted-key TEE** backend on AHAB-ELE SoCs (e.g. i.MX93).
* An **initramfs** unlocks and mounts the encrypted rootfs at boot.
* A **rootfs integrity hash** is signed with the factory key and verified
  before the rootfs is trusted.
* On HABv4, the **device trees are signed** with the factory key as well.

### Factory keys

Rootfs encryption requires a factory signing keypair, provided to the build via
**`FACTORY_KEYS_DIR`**. Generate it with
[`tools/gen-factory-signing-keys.sh`](https://github.com/Advantech-EECC/meta-modular-bsp-extra/blob/main/tools/gen-factory-signing-keys.sh)
from the extra repository; the directory must contain:

```
factory-signing.key.pem      # private signing key
factory-validation.pub.pem   # public validation key (built into the image)
```

If the directory or keys are missing, the build fails with
`FACTORY_KEYS_DIR not given`.

---

## Supported Boards

Support is listed at two levels:

* **🅿️ Preset** — a ready-made preset is shipped by the registry
* **➕ Composable** — the board supports the feature; enable it by adding the
  feature slug to the preset's `features:` list in `bsp-registry.yml`, or by
  composing the KAS fragment manually
* **⚠️ Work in progress** — known limitation, see footnotes

### `secure-boot` (NXP reference design)

The releases listed are those for which the board has a preset the `secure-boot` feature can be
added to.

#### i.MX8 — HAB

| Board              | Support | Yocto releases                                    |
|--------------------|:-------:|---------------------------------------------------|
| ROM-2620 (ed91)    | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| ROM-5720 (db5901)  | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| ROM-5721 (db5901)  | ➕ | scarthgap, styhead, walnascar                     |
| ROM-5721 1G        | ➕ | walnascar, whinlatter, wrynose                    |
| ROM-5721 2G        | 🅿️ | walnascar (preset), whinlatter, wrynose           |
| ROM-5722 (db2510)  | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| RSB-3720           | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| RSB-3720 4G        | ➕ | walnascar, whinlatter, wrynose                    |
| RSB-3720 6G        | ➕ | walnascar, whinlatter, wrynose                    |

#### i.MX9 / i.MX95 — AHAB

| Board              | Support | Yocto releases                                    |
|--------------------|:-------:|---------------------------------------------------|
| ROM-2820 (ed93)    | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| AOM-5521 (db2510)  | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |

The only `secure-boot` preset shipped today is `modular-bsp-rom5721-2g-db5901-secureboot`
(walnascar).

### `adv-secure-boot` / `rootfs-encryption` (meta-modular-bsp-extra)

Kirkstone is **not** supported (the layers' `LAYERSERIES_COMPAT` covers
scarthgap through wrynose only). Releases listed are those for which the board
has a base preset the feature can be added to.

| Board              | Scheme | `adv-secure-boot` | `rootfs-encryption` | Yocto releases                                     |
|--------------------|--------|:-----------------:|:-------------------:|-----------------------------------------------------|
| ROM-2620 (ed91)    | HABv4  | ➕ | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| ROM-5720 (db5901)  | HABv4  | ➕ | ➕ ¹ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| ROM-5721 (db5901)  | HABv4  | ➕ | ➕ | scarthgap, styhead, walnascar                      |
| ROM-5721 1G / 2G   | HABv4  | ➕ | ➕ | walnascar, whinlatter, wrynose                     |
| ROM-5722 (db2510)  | HABv4  | 🅿️ | 🅿️ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| RSB-3720 (all)     | HABv4  | ➕ | ➕ | per base preset                                    |
| ECU-150A1          | HABv4  | ⚠️ ² | ⚠️ ² | walnascar                                          |
| ROM-2820 (ed93)    | AHAB   | 🅿️ | 🅿️ | walnascar, whinlatter, wrynose                     |
| AOM-5521 A1 (db2510) | AHAB | ➕ | ➕ | walnascar, whinlatter                              |
| AOM-5521 A2 (db2510) | AHAB | ➕ | ⚠️ ³ | walnascar, wrynose                                 |
| AOM-2521 B0        | AHAB   | ➕ | ➕ | walnascar, whinlatter, wrynose                     |

> ¹ Rootfs encryption on ROM-5620 (db5901) is work in progress on **wrynose**
>   (per the meta-modular-bsp-extra README).
> ² Secure boot on ECU-150A1 is work in progress on all releases **except
>   walnascar**.
> ³ Rootfs encryption on AOM-5521 A2 (db2510) is work in progress on **all
>   releases**; no rootfs-enc preset is shipped for this board.

The shipped meta-modular-bsp-extra presets are:

* `modular-bsp-rom5722-db2510-adv-secureboot` (scarthgap … wrynose)
* `modular-bsp-rom5722-db2510-rootfs-enc` (scarthgap … wrynose)
* `modular-bsp-rom2820-ed93-adv-secureboot` (walnascar, whinlatter, wrynose)
* `modular-bsp-rom2820-ed93-rootfs-enc` (walnascar, whinlatter, wrynose)

---

## Prerequisites

### Obtaining the NXP Code Signing Tool (CST)

The NXP Code Signing Tool is proprietary software distributed under NXP's licence.

1. Create or log in to a free account on [NXP.com](https://www.nxp.com/).
2. Navigate to **Software & Tools → Security → HAB/AHAB Tools** or search for
   *"i.MX Code Signing Tool"*.
3. Download the latest CST archive (v3.4.0 or later recommended for AHAB support).
4. Extract the archive to a known path (e.g., `/opt/nxp/cst`).
5. Set `IMX_CST_BIN` to the absolute path of the `cst` binary:
   ```bash
   export IMX_CST_BIN=/opt/nxp/cst/linux64/bin/cst
   ```

> **Licence note:** The CST binary must not be committed to any source repository.
> Store it in a CI secrets vault or a controlled path on your signing host.

### Generating SRK Keys and Certificates

Use the key generation script bundled with CST:

```bash
cd /opt/nxp/cst/keys

# i.MX8 (HAB) — generates RSA-4096 SRK/CSF/IMG keypairs
./hab4_pki_tree.sh \
  -existing-ca n \
  -ca-key-pass-in-env y \
  -use-ecc n \
  -kl 4096 \
  -duration 10 \
  -num-srk 4 \
  -srk-ca y

# i.MX9 / i.MX95 (AHAB) — generates RSA-4096 SRK keypairs
./ahab_pki_tree.sh \
  -existing-ca n \
  -ca-key-pass-in-env y \
  -use-ecc n \
  -kl 4096 \
  -duration 10 \
  -num-srk 4 \
  -srk-ca y
```

After generation, the `crts/` and `keys/` subdirectories contain all certificates
and private keys. Keep private keys **offline** or in an HSM; only the SRK table
(public) is embedded in fuses.

For the Advantech path, `SIG_DATA_PATH` must point at the directory that contains
these `crts/` and `keys/` subdirectories together with the signer configuration
(`csf_hab4.cfg` for HABv4, `csf_ahab.cfg` for AHAB); see the
[`meta-secure-boot-nxp/README.md`](https://github.com/Advantech-EECC/meta-modular-bsp-extra/blob/main/meta-secure-boot-nxp/README.md)
for a complete PKI generation guide.

---

## Environment Variables

Set the following variables in your shell or CI vault **before** starting a build.
All values default to empty strings so that unsigned development builds continue to
work without signing infrastructure.

### `secure-boot` (NXP reference design)

#### Common

| Variable        | Description                                       |
|-----------------|---------------------------------------------------|
| `IMX_CST_BIN`   | Absolute path to the `cst` binary (required)      |

#### i.MX8 — HAB

| Variable                  | Description                                                       |
|---------------------------|-------------------------------------------------------------------|
| `IMX_HAB_SRK_TABLE`       | Path to `SRK_1_2_3_4_table.bin` (SRK hash table for fusing)      |
| `IMX_HAB_CSF_KEY`         | Path to the CSF private key PEM file                              |
| `IMX_HAB_IMG_KEY`         | Path to the IMG private key PEM file                              |
| `IMX_HAB_SRK_REVOKE_MASK` | Bitmask of revoked SRK slots (e.g., `0x0` — none revoked)        |

#### i.MX9 / i.MX95 — AHAB

| Variable                   | Description                                                      |
|----------------------------|------------------------------------------------------------------|
| `IMX_AHAB_SRK_TABLE`       | Path to `SRK_1_2_3_4_table.bin` (SRK hash table for fusing)     |
| `IMX_AHAB_SRK_KEY`         | Path to the SRK private key PEM file used for signing            |
| `IMX_AHAB_SRK_REVOKE_MASK` | Bitmask of revoked SRK slots (e.g., `0x0` — none revoked)       |

### `adv-secure-boot` / `rootfs-encryption` (meta-modular-bsp-extra)

These builds use the `ubuntu-22.04-adv-sb` environment, which mounts host
directories into the container and exports the container-side paths to BitBake:

| Host variable       | Container mount     | Description                                                        |
|---------------------|---------------------|--------------------------------------------------------------------|
| `CST_TOOL_PATH`     | `/opt/cst`          | NXP CST installation directory (becomes `SIG_TOOL_PATH`)          |
| `SIG_DATA_PATH`     | `/opt/keys/nxp`     | PKI directory: `csf_hab4.cfg` / `csf_ahab.cfg`, `crts/`, `keys/`  |
| `FACTORY_KEYS_DIR`  | `/opt/keys/factory` | Factory signing keys (rootfs encryption only)                     |

> **Note:** all three host variables must point to **existing directories** —
> an unset variable produces an invalid empty volume mount. For
> `adv-secure-boot`-only builds, point `FACTORY_KEYS_DIR` at an (possibly
> empty) existing directory.

---

## Building a Signed Image

### `secure-boot` (NXP reference design)

```bash
# Export signing environment
export IMX_CST_BIN=/opt/nxp/cst/linux64/bin/cst
export IMX_HAB_SRK_TABLE=/path/to/keys/SRK_1_2_3_4_table.bin
export IMX_HAB_CSF_KEY=/path/to/keys/CSF1_1_sha256_4096_65537_v3_usr_key.pem
export IMX_HAB_IMG_KEY=/path/to/keys/IMG1_1_sha256_4096_65537_v3_usr_key.pem

# Build with the secure-boot feature enabled
bsp build <bsp-name> --feature secure-boot
```

Replace `<bsp-name>` with the target BSP preset (e.g., `modular-bsp-rom5722-db2510-walnascar`).

### `adv-secure-boot` / `rootfs-encryption` (meta-modular-bsp-extra)

HABv4 example (ROM-5722, walnascar, RSA-2048 PKI):

```bash
export CST_TOOL_PATH=/opt/cst-4.0.1
export SIG_DATA_PATH=/opt/private/keys/nxp/hab4_rsa2048_sha256
export FACTORY_KEYS_DIR=/opt/private/keys/factory   # existing dir; may be empty for secure-boot-only

bsp build modular-bsp-rom5722-db2510-adv-secureboot-walnascar
```

AHAB example with rootfs encryption (ROM-2820, wrynose, ECC-256 PKI):

```bash
export CST_TOOL_PATH=/opt/cst-4.0.1
export SIG_DATA_PATH=/opt/private/keys/nxp/ahab_ecc256_sha256_no_ca_flag
export FACTORY_KEYS_DIR=/opt/private/keys/factory

bsp build modular-bsp-rom2820-ed93-rootfs-enc-wrynose
```

The build targets are the standard image names (`core-image-minimal`,
`imx-image-core`, `imx-image-full`) — the layers sign them in place.

### Using KAS directly

```bash
kas build <generated-kas-config>.yml
```

The generated KAS configuration already includes the secure-boot feature YAML files
when the feature is activated through the BSP registry.

---

## Flashing

Flash the signed `.wic` image like any other registry image:

```bash
# SD card / eMMC via bmaptool (fastest)
bmaptool copy build/tmp/deploy/images/<machine>/<image>-<machine>.rootfs.wic.zst /dev/mmcblk0

# Or via NXP UUU in serial-download mode
uuu -b sd_all   <boot-image> <wic-image>   # SD card
uuu -b emmc_all <boot-image> <wic-image>   # eMMC
```

For rootfs-encryption images, the first boot re-encrypts/provisions the rootfs
key via CAAM or the TEE; allow it to complete before power-cycling.

---

## Fusing / Provisioning the Board

> ⚠️ **Warning:** Fusing is a one-way, irreversible operation. Writing incorrect
> values will permanently brick the board. Test the signed image on an open board
> before fusing.

### i.MX8 HAB Fusing

1. Boot the signed image on an **open** (un-fused) board and verify HAB events:
   ```
   U-Boot => hab_status
   ```
   Confirm: `Secure boot disabled` with **no HAB events** (no errors).

2. Write the SRK hash fuses using `imx_usb_loader` or U-Boot `fuse` commands:
   ```bash
   # First, obtain the SRK hash words from the NXP srktool utility:
   srktool --hab_ver 4 --certs SRK_1_2_3_4_crt.pem --table SRK_1_2_3_4_table.bin \
           --efuses SRK_1_2_3_4_fuse.bin --digest sha256
   # The output SRK_1_2_3_4_fuse.bin contains 8 x 32-bit words in big-endian order.
   # Convert and program each word (example for i.MX8MP — bank 6, words 0-7;
   # adapt bank/word addresses per your SoC reference manual):
   hexdump -e '"%08X\n"' SRK_1_2_3_4_fuse.bin | \
     awk '{print NR-1, $1}' | \
     while read word val; do
       echo "fuse prog -y 6 $word 0x$val"
     done
   ```
   Run each printed `fuse prog` command in the U-Boot console.

3. Lock the HAB configuration by programming the SEC_CONFIG fuse:
   ```
   fuse prog -y 1 3 0x2000000
   ```
   After reboot, only images signed with matching keys will execute.

### i.MX9 / i.MX95 AHAB Fusing

1. Boot the signed container image on an open board and check AHAB events:
   ```
   U-Boot => ahab_status
   ```
   Confirm: no AHAB events.

2. Program the SRK hash using U-Boot `fuse` commands or `uuu` (Universal Update
   Utility):
   ```
   ahab_close
   ```
   After `ahab_close`, the device enters closed (secure) mode on the next reset.

Refer to NXP application notes **AN4581** (HAB) and **AN12838** (AHAB) for
complete fusing procedures.

---

## CI / Azure Pipelines

Secure-boot builds require NXP's proprietary CST binary and private signing keys
and **must not** run on shared cloud agents. The `azure-pipelines.yml` in this
repository defines a dedicated `BuildSecureBootBSP` job that:

- Runs only on the `aeu.de.secure` self-hosted agent pool.
- Is gated to **manual** pipeline runs (`Build.Reason == Manual`).
- Receives all key paths via Azure DevOps **secret pipeline variables** (marked as
  secret so they are never printed in logs).

The job builds the NXP reference-design preset as well as the
meta-modular-bsp-extra presets. For the latter it maps three secret variables
into the build environment: `CST_TOOL_PATH`, `SIG_DATA_PATH` and
`FACTORY_KEYS_DIR` (host paths on the signing agent; see
[Environment Variables](#environment-variables)).

### Setting Up Secret Variables

In Azure DevOps, navigate to:
**Pipelines → Your Pipeline → Edit → Variables**

Add each variable from the [Environment Variables](#environment-variables) table
and enable the **"Keep this value secret"** toggle.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Build fails: `cst: command not found` | `IMX_CST_BIN` not set or wrong path | Verify the path and that the binary is executable |
| `HAB event: 0x33` in `hab_status` | Image was not signed or signed with the wrong keys | Re-sign the image; check CST output for errors |
| Board hangs after fusing | SRK hash mismatch | Confirm SRK table matches the keys used to sign |
| `AHAB: 0x16` error | AHAB container not signed | Ensure `IMX_AHAB_ENABLE = "1"` is active and CST ran |
| Empty `IMX_CST_BIN` in build log | `$ENV{}` expansion failed | Export the variable before invoking `bsp build` |
| `FACTORY_KEYS_DIR not given (required for rootfs-enc)` | `FACTORY_KEYS_DIR` not set or keys missing | Generate the factory keypair with the extra repo's key-generation script and export `FACTORY_KEYS_DIR` |
| Signer fails: `csf_hab4.cfg` / `csf_ahab.cfg` not found | `SIG_DATA_PATH` does not point at a complete PKI directory | Verify the directory contains the signer config plus `crts/` and `keys/` |
| Duplicate signing steps / conflicting bbappends for `u-boot-imx`, `imx-boot`, `linux-imx` | `secure-boot` and `adv-secure-boot` (or `rootfs-encryption`) enabled together | Use exactly one secure-boot implementation per preset |
| `Layer ... not found` / `LAYERSERIES_COMPAT` error on kirkstone | meta-modular-bsp-extra does not support kirkstone | Use scarthgap or newer, or the NXP reference-design `secure-boot` feature |

---

## References

- [NXP HAB Code Signing Tool User Guide](https://www.nxp.com/docs/en/user-guide/HABCST_UG.pdf)
- [NXP Application Note AN4581 — Secure Boot on i.MX50, i.MX53, and i.MX6 (HAB)](https://www.nxp.com/docs/en/application-note/AN4581.pdf)
- [NXP Application Note AN12838 — AHAB Introduction (i.MX8ULP, i.MX9)](https://www.nxp.com/docs/en/application-note/AN12838.pdf)
- [U-Boot HABv4 guide (imx/habv4)](https://github.com/nxp-imx/uboot-imx/blob/master/doc/imx/habv4/introduction_habv4.txt)
- [U-Boot AHAB guide (imx/ahab)](https://github.com/nxp-imx/uboot-imx/blob/master/doc/imx/ahab/introduction_ahab.txt)
- [meta-nxp-security-reference-design (Advantech)](https://github.com/Advantech-EECC/meta-nxp-security-reference-design)
- [meta-modular-bsp-extra (Advantech)](https://github.com/Advantech-EECC/meta-modular-bsp-extra)
- [meta-secure-boot-nxp layer README](https://github.com/Advantech-EECC/meta-modular-bsp-extra/blob/main/meta-secure-boot-nxp/README.md)
- [meta-rootfs-enc-core layer README](https://github.com/Advantech-EECC/meta-modular-bsp-extra/blob/main/meta-rootfs-enc-core/README.md)
- [meta-rootfs-enc-nxp layer README](https://github.com/Advantech-EECC/meta-modular-bsp-extra/blob/main/meta-rootfs-enc-nxp/README.md)
- [NXP i.MX Linux BSP Reference Manual](https://www.nxp.com/docs/en/user-guide/IMX_LINUX_USERS_GUIDE.pdf)
- [Yocto Project Security Guide](https://docs.yoctoproject.org/dev/dev-manual/securing-images.html)
