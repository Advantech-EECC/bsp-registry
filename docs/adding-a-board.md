# Adding a Board

Adding a new board to the registry requires **four wiring points** in
[`bsp-registry.yml`](../bsp-registry.yml) (or an included registry file) plus one KAS machine
fragment. Miss any one of them and the board will not show up in `bsp list`.

Read [registry-model.md](registry-model.md) first if you are not familiar with the data model.

---

## 1. Write the Machine Fragment

Create a KAS fragment under `vendors/<vendor>/[<soc_vendor>/]machine/<board>.yml`:

```yaml
header:
  version: 14

machine: my-board

repos:
  meta-my-vendor:
    url: "https://github.com/example/meta-my-vendor.git"
    branch: "scarthgap"
    path: "layers/meta-my-vendor"
    layers:
      .:
```

Use the `.yml` extension — the registry loader does not normalise `.yaml`/`.yml`, so a mismatch
between the file on disk and the `includes:` entry is a silent failure.

## 2. Register the Vendor (if new)

```yaml
registry:
  vendors:
    - slug: my-vendor
      name: "My Vendor"
```

## 3. Register the Device

```yaml
registry:
  devices:
    - slug: my-board
      name: "My Board"
      vendor: my-vendor
      soc_vendor: nxp        # the SoC supplier; drives feature vendor_overrides
      includes:
        - vendors/my-vendor/nxp/machine/my-board.yml
```

## 4. Add a `vendor_release` Override

For each Yocto release the board supports, add (or reuse) an entry under that release's
`vendor_overrides`:

```yaml
registry:
  releases:
    - slug: scarthgap
      vendor_overrides:
        - vendor: my-vendor
          releases:
            - slug: my-vendor-scarthgap
              includes:
                - vendors/my-vendor/releases/scarthgap.yml
```

If your vendor's layers are the same across releases you may reuse an existing `vendor_release`
slug (for example NXP boards from Advantech reuse `nxp-scarthgap`).

## 5. Add the Preset

Only presets appear in `bsp list`:

```yaml
registry:
  bsp:
    - name: my-board
      description: "My Board reference BSP"
      device: my-board
      framework: yocto
      distro: poky
      vendor_release: my-vendor-scarthgap
      releases: [scarthgap, walnascar]
      features: [systemd, yocto-ssh]
```

This yields the build targets `my-board-scarthgap` and `my-board-walnascar`. See
[name expansion](registry-model.md#3-presets-and-name-expansion).

---

## 6. Verify

```console
$ bsp list | grep my-board          # the board should now be listed
$ bsp show my-board-scarthgap       # inspect the resolved KAS configuration
$ bsp build my-board-scarthgap      # build it
```

(`my-board` is a placeholder — substitute your own device slug.)

Then run the repository checks locally:

```bash
python3 -c "import yaml,sys,glob;[yaml.safe_load(open(f)) for f in glob.glob('**/*.y*ml', recursive=True)]"
python3 scripts/check-docs-consistency.py
```

---

## 7. Vendor-Specific Gotchas

### NVIDIA Jetson (OE4T `tegra-demo-distro`)

Jetson machine fragments **must** declare a `bblayers_conf_header` carrying
`TD_BBLAYERS_CONF_VERSION`, matching `REQUIRED_TD_BBLAYERS_CONF_VERSION` in the upstream
`tegrademo.inc`. A mismatch fails the `tegra-support-sanity` check at parse time.

| Release | Value |
|---------|-------|
| scarthgap, styhead, walnascar, whinlatter | `tegrademo-5` |
| wrynose | `tegrademo-7` |

See [`vendors/nvidia/README.md`](../vendors/nvidia/README.md).

### NXP i.MX

Most NXP releases need patches applied to `meta-freescale` or the BSP layers. Patches live under
`patches/nxp/<release>/` and are applied by the release fragment's `patches:` block — see
[`patches/README.md`](../patches/README.md).

### Secure boot on NXP

Secure boot requires the `ubuntu-22.04-csb` environment, which provides NXP's Code Signing Tool
at `SIG_TOOL_PATH=/opt/cst`. See [secure-boot.md](secure-boot.md).

---

## 8. Documentation

When you add a board, update:

* The relevant vendor `README.md` under `vendors/`
* The compatibility matrix in the root [`README.md`](../README.md)
* `patches/README.md` if you added patches

`scripts/check-docs-consistency.py` verifies that every `bsp <verb> <name>` invocation in the docs
names a real preset and that referenced paths exist. It runs in CI (informationally) and can be
run locally at any time.
