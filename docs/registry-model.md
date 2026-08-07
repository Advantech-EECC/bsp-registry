# Registry Data Model

This document describes the structure of [`bsp-registry.yml`](../bsp-registry.yml), the single
source of truth from which the `bsp` CLI derives every buildable configuration.

## Table of Contents

1. [Top-Level Structure](#1-top-level-structure)
2. [The `registry` Block](#2-the-registry-block)
3. [Presets and Name Expansion](#3-presets-and-name-expansion)
4. [Override Resolution Order](#4-override-resolution-order)
5. [The `include:` Mechanism](#5-the-include-mechanism)

---

## 1. Top-Level Structure

```yaml
specification:          # registry schema version (currently "2.0")
include:                # additional registry files merged into this one
flash:                  # defaults for `bsp flash`
deploy:                 # defaults for `bsp deploy`
lava:                   # defaults for `bsp lava`
environment:            # variables exported into every build
containers:             # container image definitions
environments:           # named build environments (container + variables)
registry:               # the BSP catalogue itself
```

`flash`, `deploy`, `lava`, `environment`, `containers` and `environments` are documented in
[flash-deploy-lava.md](flash-deploy-lava.md).

---

## 2. The `registry` Block

| Key | Purpose |
|-----|---------|
| `frameworks` | Build systems: `yocto` and `isar`. Each supplies the base KAS fragment. |
| `distro` | Distribution definitions (`poky`, `poky-harden`, `tegrademo`, `isar-v0.11`, `isar-v1.0`, …). |
| `vendors` | SoC and board vendors (`nxp`, `qualcomm`, `mediatek`, `nvidia`, `advantech-europe`, `qemu`, …). |
| `devices` | Individual boards. Each has a `slug`, a `vendor`, and `includes` pointing at a machine fragment. |
| `releases` | Yocto/Isar releases (`kirkstone` … `wrynose`, `master`, `ubuntu-noble`, `debian-trixie`, …). |
| `features` | Optional capabilities that can be layered onto a build (see [features.md](features.md)). |
| `bsp` | The preset list — the only entries that appear in `bsp list`. |

> **Note:** the YAML key for presets is `registry.bsp`, not `registry.presets`.

### 2.1. Devices

```yaml
- slug: rsb3720
  vendor: advantech-europe
  soc_vendor: nxp
  includes:
    - vendors/advantech-europe/nxp/machine/rsb3720.yml
```

`soc_vendor` matters because feature `vendor_overrides` are keyed on the pair
(`vendor`, `soc_vendors[].vendor`) — see [§4](#4-override-resolution-order).

### 2.2. Releases

A release carries the base KAS fragment for that Yocto/Isar branch plus per-vendor overrides:

```yaml
- slug: scarthgap
  includes:
    - yocto/releases/scarthgap.yml
  vendor_overrides:
    - vendor: nxp
      releases:
        - slug: nxp-scarthgap
          includes:
            - vendors/nxp/releases/scarthgap.yml
```

The `releases[].slug` here is what a preset references as `vendor_release`.

---

## 3. Presets and Name Expansion

A preset ties a device, a release (or a list of releases), a framework, a distro and a set of
features together:

```yaml
- name: modular-bsp-rsb3720
  device: rsb3720
  framework: yocto
  distro: poky
  vendor_release: nxp-scarthgap
  releases: [scarthgap, styhead, walnascar, whinlatter, wrynose]
  features: [systemd, yocto-ssh]
```

**Name expansion is the single rule that trips people up:**

| Preset key | CLI name |
|------------|----------|
| `releases: [a, b]` (plural) | `<name>-a` and `<name>-b` — the release is appended |
| `release: a` (singular) | `<name>` — used verbatim, **no** suffix |

So `modular-bsp-rsb3720` above is *not* a valid build target; `modular-bsp-rsb3720-scarthgap` is.
Conversely `poky-harden-qemux86-64-scarthgap` already encodes its release and takes no suffix.

Run `bsp list` to see the expanded names; that is always authoritative.

---

## 4. Override Resolution Order

When resolving a preset the CLI concatenates KAS fragments in this order:

1. **Framework** base (`yocto/yocto.yaml` or `isar/isar.yaml`)
2. **Release** `includes` (e.g. `yocto/releases/scarthgap.yml`)
3. **Vendor overrides** for that release — applied **only** when the override's
   `releases[].slug` equals the preset's `vendor_release`
4. **Distro** `includes`
5. **Device** `includes` (the machine fragment)
6. **Feature** `includes`, then feature `release_overrides` matching the release, then feature
   `vendor_overrides` matching (`vendor`, `soc_vendor`)

Because step 3 is gated on `vendor_release`, a preset that omits `vendor_release` silently gets no
vendor layers. This is the most common cause of a "board builds but has no BSP layers" bug.

---

## 5. The `include:` Mechanism

```yaml
include:
  - bsp-registry.nvidia.yaml
```

Included files are merged into the root registry, but **lists are concatenated, not merged by
slug**. Consequences:

* A vendor, device, feature or preset can be defined entirely in an included file.
* An *existing* entry cannot be extended from an included file. This is why NVIDIA's
  release-level `vendor_overrides` live in `bsp-registry.yml` (they extend the shared
  `scarthgap`/`styhead`/… release entries) while its vendors, devices and presets live in
  `bsp-registry.nvidia.yaml`.
* Any tooling that enumerates presets must merge the includes first — see
  [`scripts/check-docs-consistency.py`](../scripts/check-docs-consistency.py).

---

## See Also

* [Adding a Board](adding-a-board.md)
* [Feature Catalogue](features.md)
* [Flash, Deploy and LAVA Configuration](flash-deploy-lava.md)
