# Flash, Deploy and LAVA Configuration

Beyond building, `bsp-registry.yml` configures three post-build workflows plus the container
environments builds run in. These are top-level blocks, siblings of `registry`.

## Table of Contents

1. [Containers](#1-containers)
2. [Environments](#2-environments)
3. [Global Build Environment](#3-global-build-environment)
4. [Flashing](#4-flashing)
5. [Deployment](#5-deployment)
6. [LAVA](#6-lava)

---

## 1. Containers

The `containers:` block defines the images builds run inside. Each entry names a Dockerfile in the repository root ([`Dockerfile.ubuntu`](../Dockerfile.ubuntu),
[`Dockerfile.debian`](../Dockerfile.debian), [`Dockerfile.isar.debian`](../Dockerfile.isar.debian))
plus build arguments.

| Name | Base | KAS | Notes |
|------|------|-----|-------|
| `ubuntu-20.04` | Ubuntu 20.04 | 4.7 | Legacy releases (kirkstone and older BSPs) |
| `ubuntu-22.04` | Ubuntu 22.04 | 5.2 | Default |
| `ubuntu-22.04-csb` | Ubuntu 22.04 | 5.2 | Adds a bind mount of `$CST_TOOL_PATH` → `/opt/cst` for NXP code signing |
| `ubuntu-24.04` | Ubuntu 24.04 | 5.2 | |
| `debian-12` | Debian bookworm | 5.2 | |
| `debian-13` | Debian trixie | 5.2 | |
| `isar-debian-13` | Debian trixie | 5.2 | Isar builds. `privileged: true` plus `runtime_args: -p 2222:2222 --device=/dev/net/tun --cap-add=NET_ADMIN` for `debootstrap` and QEMU networking |

Images are tagged `advantech/bsp-registry/<name>/kas:<KAS_VERSION>`.

## 2. Environments

An *environment* binds a container to extra variables and file copies. A preset selects one via
its `environment:` key; presets that omit it get `default`.

| Environment | Container | Extras |
|-------------|-----------|--------|
| `default` | `ubuntu-22.04` | — |
| `ubuntu-20.04` / `ubuntu-22.04` / `ubuntu-24.04` / `debian-13` | matching container | — |
| `ubuntu-22.04-csb` | `ubuntu-22.04-csb` | `SIG_TOOL_PATH=/opt/cst` — required for [secure boot](secure-boot.md) |
| `isar-build-environment` | `isar-debian-13` | Isar-specific `DL_DIR`/`SSTATE_DIR`; copies `isar/scripts/isar-runqemu.sh` into `build/` |

## 3. Global Build Environment

The top-level `environment.variables` list is exported into **every** build:

| Variable | Default |
|----------|---------|
| `GITCONFIG_FILE` | `$ENV{HOME}/.gitconfig` |
| `DL_DIR` | `$ENV{HOME}/data/cache/downloads` |
| `SSTATE_DIR` | `$ENV{HOME}/data/cache/sstate` |

`$ENV{NAME}` is expanded from the host environment at resolution time. Point `DL_DIR` and
`SSTATE_DIR` at a shared location to reuse downloads and sstate across boards and releases.

---

## 4. Flashing

```yaml
flash:
  tool: bmaptool
  artifact_dirs:
    - build/tmp/deploy/images
  image_patterns:
    - '**/{build_target}-*.wic.zst'
    - '**/*.wic.bz2'
    # …
```

| Key | Meaning |
|-----|---------|
| `tool` | `bmaptool` (default), `dd` or `uuu` |
| `artifact_dirs` | Where to look for images, relative to the build directory |
| `image_patterns` | Glob patterns, tried **in order**; the first match wins. `{build_target}` expands to the resolved machine/image name |
| `extra_args` | Extra arguments passed through to the flashing tool |

```bash
bsp flash modular-bsp-rsb3720-scarthgap --device /dev/sdX
```

`uuu` is the right choice for NXP i.MX boards in serial-download mode; `bmaptool` is fastest for
SD cards and eMMC exposed as block devices.

---

## 5. Deployment

```yaml
deploy:
  provider: azure
  account_url: $ENV{AZURE_STORAGE_ACCOUNT_URL}
  container: bsp-registry-artifacts
  prefix: '{vendor}/{device}/{release}/{date}'
  include_manifest: true
```

| Key | Meaning |
|-----|---------|
| `provider` | `azure` or `aws` |
| `account_url` / `container` | Target storage account and container/bucket |
| `prefix` | Object key prefix. Supports `{vendor}`, `{device}`, `{release}` and `{date}` |
| `artifact_dirs` | Searched for artifacts (`build/tmp/deploy/images` and `…/sdk`) |
| `patterns` | Which artifacts to upload (`*.wic*`, `*.ext4`, `*.img`, `bzImage`, `uImage`, …) |
| `include_manifest` | Upload a manifest describing the build alongside the artifacts |
| `yocto_cache` | When enabled, also publish `downloads` and/or `sstate` |

Credentials come from the environment (`AZURE_STORAGE_ACCOUNT_URL` and the standard Azure or AWS
credential variables). **Never commit credentials to the registry.**

```bash
bsp deploy modular-bsp-rsb3720-scarthgap
```

---

## 6. LAVA

[LAVA](https://www.lavasoftware.org/) runs the built image on real hardware in a board farm.

```yaml
lava:
  server: $ENV{LAVA_SERVER}
  username: $ENV{LAVA_USER}
  token: $ENV{LAVA_TOKEN}
  artifact_server_url: $ENV{LAVA_ARTIFACT_SERVER_URL}
  wait_timeout: 3600
  poll_interval: 30
```

| Key | Meaning |
|-----|---------|
| `server` | LAVA instance URL |
| `username` / `token` | LAVA API credentials, taken from the environment |
| `artifact_server_url` | Where LAVA fetches the image from — usually the same location `bsp deploy` wrote to |
| `wait_timeout` | Seconds to wait for a job to finish (default 3600) |
| `poll_interval` | Seconds between job-status polls (default 30) |

```bash
bsp lava modular-bsp-rsb3720-scarthgap
```

The typical CI order is **build → deploy → lava**: deployment publishes the image to a URL that
the LAVA job definition then references.

---

## See Also

* [Registry Data Model](registry-model.md)
* [Secure Boot](secure-boot.md)
