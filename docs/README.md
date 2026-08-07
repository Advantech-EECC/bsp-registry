# Documentation Index

| Document | Contents |
|----------|----------|
| [Registry Data Model](registry-model.md) | Structure of `bsp-registry.yml`, preset name expansion, override resolution order, the `include:` mechanism |
| [Adding a Board](adding-a-board.md) | The four wiring points needed to make a new board appear in `bsp list`, plus vendor-specific gotchas |
| [Feature Catalogue](features.md) | Registered features, preview fragments, vendor-bundled fragments, manual KAS composition |
| [Flash, Deploy and LAVA](flash-deploy-lava.md) | Containers, environments, and the `flash` / `deploy` / `lava` configuration blocks |
| [Secure Boot](secure-boot.md) | NXP HAB/AHAB signing, supported boards, key management |

Other documentation elsewhere in the repository:

| Document | Contents |
|----------|----------|
| [Root README](../README.md) | Overview, hardware compatibility matrices, quick start, CLI reference |
| [CONTRIBUTING](../CONTRIBUTING.md) | Repository layout, local checks, CI |
| [Patches](../patches/README.md) | Inventory of the 24 downstream patches and which fragment applies each |
| [Isar](../isar/README.md) | Debian-based builds with Isar |
| [Building with `repo`](../BUILDING_WITH_REPO.md) | Alternative workflow using Google `repo` manifests |

Vendor documentation lives under `vendors/<vendor>/README.md`:
[Qualcomm](../vendors/qualcomm/README.md),
[MediaTek](../vendors/mediatek/README.md),
[NVIDIA](../vendors/nvidia/README.md),
[Advantech Europe / Qualcomm](../vendors/advantech-europe/qualcomm/README.md),
[Advantech Europe / MediaTek](../vendors/advantech-europe/mediatek/README.md).

NXP boards do not have a dedicated vendor README; they are covered by the compatibility matrix in
the [root README](../README.md#21-nxp-boards-compatibility-matrix) and by
[patches/README.md](../patches/README.md).
