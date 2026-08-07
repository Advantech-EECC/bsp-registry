# Secure Boot for Advantech Europe NXP Boards

This document describes how to enable and use the **`secure-boot`** BSP feature for
Advantech Europe NXP-based boards. The feature activates boot-image signing via
NXP's HAB (i.MX8 family) or AHAB (i.MX9 / i.MX95 family) technology.

---

## Table of Contents

- [Overview](#overview)
- [HAB vs AHAB](#hab-vs-ahab)
- [Supported Boards](#supported-boards)
- [Prerequisites](#prerequisites)
  - [Obtaining the NXP Code Signing Tool (CST)](#obtaining-the-nxp-code-signing-tool-cst)
  - [Generating SRK Keys and Certificates](#generating-srk-keys-and-certificates)
- [Environment Variables](#environment-variables)
- [Building a Signed Image](#building-a-signed-image)
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

---

## Supported Boards

Support is listed at two levels:

* **🅿️ Preset** — a ready-made secure-boot preset is shipped by the registry
* **➕ Composable** — the board supports signing; enable it by adding the `secure-boot` feature to
  the preset's `features:` list in `bsp-registry.yml`, or by composing
  `features/secure-boot/secure-boot.yml` with KAS

The releases listed are those for which the board has a preset the `secure-boot` feature can be
added to.

### i.MX8 — HAB

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

### i.MX9 / i.MX95 — AHAB

| Board              | Support | Yocto releases                                    |
|--------------------|:-------:|---------------------------------------------------|
| ROM-2820 (ed93)    | ➕ | scarthgap, styhead, walnascar, whinlatter, wrynose |
| AOM-5521 (db2510)  | ➕ | walnascar, whinlatter, wrynose                    |

The only secure-boot preset shipped today is `modular-bsp-rom5721-2g-db5901-secureboot`
(walnascar).

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

---

## Environment Variables

Set the following variables in your shell or CI vault **before** starting a build.
All values default to empty strings so that unsigned development builds continue to
work without signing infrastructure.

### Common

| Variable        | Description                                       |
|-----------------|---------------------------------------------------|
| `IMX_CST_BIN`   | Absolute path to the `cst` binary (required)      |

### i.MX8 — HAB

| Variable                  | Description                                                       |
|---------------------------|-------------------------------------------------------------------|
| `IMX_HAB_SRK_TABLE`       | Path to `SRK_1_2_3_4_table.bin` (SRK hash table for fusing)      |
| `IMX_HAB_CSF_KEY`         | Path to the CSF private key PEM file                              |
| `IMX_HAB_IMG_KEY`         | Path to the IMG private key PEM file                              |
| `IMX_HAB_SRK_REVOKE_MASK` | Bitmask of revoked SRK slots (e.g., `0x0` — none revoked)        |

### i.MX9 / i.MX95 — AHAB

| Variable                   | Description                                                      |
|----------------------------|------------------------------------------------------------------|
| `IMX_AHAB_SRK_TABLE`       | Path to `SRK_1_2_3_4_table.bin` (SRK hash table for fusing)     |
| `IMX_AHAB_SRK_KEY`         | Path to the SRK private key PEM file used for signing            |
| `IMX_AHAB_SRK_REVOKE_MASK` | Bitmask of revoked SRK slots (e.g., `0x0` — none revoked)       |

---

## Building a Signed Image

### Using the `bsp` CLI

```bash
# Export signing environment
export IMX_CST_BIN=/opt/nxp/cst/linux64/bin/cst
export IMX_HAB_SRK_TABLE=/path/to/keys/SRK_1_2_3_4_table.bin
export IMX_HAB_CSF_KEY=/path/to/keys/CSF1_1_sha256_4096_65537_v3_usr_key.pem
export IMX_HAB_IMG_KEY=/path/to/keys/IMG1_1_sha256_4096_65537_v3_usr_key.pem

# Build with the secure-boot feature enabled
bsp build <bsp-name> --feature secure-boot
```

Replace `<bsp-name>` with the target BSP preset (e.g., `rom5720-walnascar-imx-6.12.49-2.2.0`).

### Using KAS directly

```bash
kas build <generated-kas-config>.yml
```

The generated KAS configuration already includes the secure-boot feature YAML files
when the feature is activated through the BSP registry.

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

---

## References

- [NXP HAB Code Signing Tool User Guide](https://www.nxp.com/docs/en/user-guide/HABCST_UG.pdf)
- [NXP Application Note AN4581 — Secure Boot on i.MX50, i.MX53, and i.MX6 (HAB)](https://www.nxp.com/docs/en/application-note/AN4581.pdf)
- [NXP Application Note AN12838 — AHAB Introduction (i.MX8ULP, i.MX9)](https://www.nxp.com/docs/en/application-note/AN12838.pdf)
- [meta-nxp-security-reference-design (Advantech)](https://github.com/Advantech-EECC/meta-nxp-security-reference-design)
- [NXP i.MX Linux BSP Reference Manual](https://www.nxp.com/docs/en/user-guide/IMX_LINUX_USERS_GUIDE.pdf)
- [Yocto Project Security Guide](https://docs.yoctoproject.org/dev/dev-manual/securing-images.html)
