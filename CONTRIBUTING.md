# Contributing

Thanks for contributing to the BSP registry. This document covers the repository layout, the
checks that run in CI, and how to run them locally.

## Repository Layout

| Path | Contents |
|------|----------|
| `bsp-registry.yml` | The registry — the single source of truth for all buildable configurations |
| `bsp-registry.nvidia.yaml` | NVIDIA vendor, devices and presets, merged via the top-level `include:` |
| `yocto/` | Framework base, Yocto releases, distros and generic feature fragments |
| `isar/` | Isar framework base, versions, distros and helper scripts |
| `vendors/` | Per-vendor release, machine and feature fragments |
| `features/` | Cross-vendor feature fragments (OTA, secure boot, Qt, ROS 2, SBOM, …) |
| `compilers/` | Alternative toolchains (`clang`) |
| `patches/` | Downstream patches applied to upstream layers |
| `scripts/` | Repository tooling |
| `docs/` | Long-form documentation — start at [`docs/README.md`](docs/README.md) |

See [`docs/registry-model.md`](docs/registry-model.md) for how these fit together, and
[`docs/adding-a-board.md`](docs/adding-a-board.md) for the board-onboarding checklist.

## Local Checks

Install the Python dependencies once:

```bash
pip install -r requirements.txt
```

Then, before opening a pull request:

```bash
# 1. Every YAML file parses
python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('**/*.y*ml', recursive=True)]"

# 2. Documentation matches the registry
python3 scripts/check-docs-consistency.py

# 3. The board you touched still resolves and builds
bsp list | grep <your-board>
bsp build <your-preset>-<release>
```

### `scripts/check-docs-consistency.py`

This script guards against documentation drift. It verifies that:

1. every `bsp <verb> <name>` invocation in a fenced code block names a real preset;
2. every inline-code path and Markdown link in the docs resolves to a file that exists;
3. the `**N patches**` count in `README.md` matches the number of `*.patch` files in the tree;
4. every patch file is documented in [`patches/README.md`](patches/README.md).

If a reference legitimately cannot resolve — a build output, a path inside an upstream layer, or
a naming template — add it to `EXTERNAL_REFERENCES` or `PLACEHOLDER_NAMES` in the script rather
than rewording the documentation to hide it.

## Continuous Integration

[`.github/workflows/validate-kas-configs.yml`](.github/workflows/validate-kas-configs.yml) runs
on pushes and pull requests touching YAML, Markdown or the checker script:

| Job | Blocking | Purpose |
|-----|----------|---------|
| `validate-yaml-syntax` | yes | All `*.yml` / `*.yaml` files parse |
| `validate-docs-consistency` | no (`continue-on-error`) | Runs the doc-consistency checker |
| `validate-kas-configs` | yes | KAS resolves the registry configurations |
| `lint-dockerfiles` | no (`continue-on-error`) | hadolint over the `Dockerfile.*` files |

## Documentation Conventions

* Use plain `bsp <verb> <preset>` in examples. Do not use `bsp --local`; that flag is for working
  against an uncommitted clone and is not the workflow being documented.
* Reference presets by their **expanded** CLI name (`modular-bsp-rsb3720-scarthgap`), not the raw
  `name:` key from the registry. See
  [preset name expansion](docs/registry-model.md#3-presets-and-name-expansion).
* Write paths in inline code so the checker can validate them, and prefer
  [`links`](docs/README.md) when pointing at another document.
* When you add a board, patch or feature, update the corresponding table in the root
  [`README.md`](README.md), the vendor README, and [`patches/README.md`](patches/README.md).

## Commit and Pull Request Guidance

* Keep registry changes and documentation updates in the same commit — the CI doc check exists to
  make that easy to verify.
* Mention which boards and releases you built when adding or changing a BSP; the CI does not
  perform full builds.
