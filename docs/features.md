# Feature Catalogue

Features are optional capabilities layered onto a preset. They are declared under
`registry.features` in [`bsp-registry.yml`](../bsp-registry.yml) and referenced by slug from a
preset's `features:` list.

```yaml
- name: my-board
  device: my-board
  features: [systemd, yocto-ssh, rauc]
```

Features are applied **last** in the resolution order, so they can override vendor and machine
settings. See [registry-model.md](registry-model.md#4-override-resolution-order).

---

## 1. Registered Features

All registered features are `compatible_with: [yocto]`.

### 1.1. Base System

| Slug | Fragment | Description |
|------|----------|-------------|
| `systemd` | [`yocto/features/systemd.yaml`](../yocto/features/systemd.yaml) | Use systemd as the init system |
| `udev` | [`yocto/features/udev.yaml`](../yocto/features/udev.yaml) | Enable udev |
| `usrmerge` | [`yocto/features/usrmerge.yaml`](../yocto/features/usrmerge.yaml) | Enable the merged-`/usr` layout |
| `ipv6` | [`yocto/features/ipv6.yaml`](../yocto/features/ipv6.yaml) | Enable IPv6 |
| `virtualization` | [`yocto/features/virtualization.yaml`](../yocto/features/virtualization.yaml) | Enable container/VM support |

### 1.2. Development and Debug

| Slug | Fragment | Description |
|------|----------|-------------|
| `yocto-ssh` | [`yocto/features/ssh.yaml`](../yocto/features/ssh.yaml) | SSH server in the image |
| `debug-tweaks` | [`yocto/features/debug-tweaks.yaml`](../yocto/features/debug-tweaks.yaml) | Passwordless root, dev-friendly defaults |
| `root-login` | [`yocto/features/root-login.yaml`](../yocto/features/root-login.yaml) | Permit root login |
| `ethernet-debug` | [`yocto/features/ethernet-debug.yaml`](../yocto/features/ethernet-debug.yaml) | Ethernet debugging aids |

> `debug-tweaks` and `root-login` disable authentication safeguards. Do not ship them in
> production images.

### 1.3. Graphics

| Slug | Fragment | Description |
|------|----------|-------------|
| `wayland` | [`yocto/features/wayland.yaml`](../yocto/features/wayland.yaml) | Wayland display stack |
| `x11` | [`yocto/features/x11.yaml`](../yocto/features/x11.yaml) | X11 display stack |

### 1.4. Security

| Slug | Fragment | Description |
|------|----------|-------------|
| `security` | [`yocto/features/security.yaml`](../yocto/features/security.yaml) | Hardening options (`meta-security`) |
| `secure-boot` | [`features/secure-boot/secure-boot.yml`](../features/secure-boot/secure-boot.yml) | HAB/AHAB image signing. Overridden to [`vendors/nxp/features/secure-boot/imx-secure-boot.yml`](../vendors/nxp/features/secure-boot/imx-secure-boot.yml) for Advantech boards with NXP SoCs. See [secure-boot.md](secure-boot.md). |

### 1.5. OTA Update

| Slug | Fragment | NXP override |
|------|----------|--------------|
| `rauc` | [`features/ota/rauc/rauc.yml`](../features/ota/rauc/rauc.yml) | [`features/ota/rauc/modular-bsp-ota-nxp.yml`](../features/ota/rauc/modular-bsp-ota-nxp.yml) |
| `swupdate` | [`features/ota/swupdate/swupdate.yml`](../features/ota/swupdate/swupdate.yml) | [`features/ota/swupdate/modular-bsp-ota-nxp.yml`](../features/ota/swupdate/modular-bsp-ota-nxp.yml) |
| `ostree` | [`features/ota/ostree/ostree.yml`](../features/ota/ostree/ostree.yml) | [`features/ota/ostree/modular-bsp-ota-nxp.yml`](../features/ota/ostree/modular-bsp-ota-nxp.yml) |

`ostree` additionally carries `release_overrides` for scarthgap, styhead and walnascar
([`ostree-scarthgap.yml`](../features/ota/ostree/ostree-scarthgap.yml), [`ostree-styhead.yml`](../features/ota/ostree/ostree-styhead.yml), [`ostree-walnascar.yml`](../features/ota/ostree/ostree-walnascar.yml)), because the OSTree layer
API changed between those releases.

### 1.6. Acceleration

| Slug | Fragment | Description |
|------|----------|-------------|
| `hailo` | [`features/deep-learning/hailo.yml`](../features/deep-learning/hailo.yml) | Hailo-8 AI accelerator support (`meta-hailo`) |

---

## 2. Preview Fragments

These KAS fragments exist in the tree but are **not** registered as features and are **not**
referenced by any preset. They are kept as a starting point for future work and can be composed
manually with `kas build`, but they are unvalidated and may not build.

| Fragment | Upstream layer | Purpose |
|----------|----------------|---------|
| [`features/protocols/zenoh.yml`](../features/protocols/zenoh.yml) | `meta-zenoh` | Zenoh pub/sub protocol |
| [`features/cameras/realsense.yml`](../features/cameras/realsense.yml) | `meta-intel-realsense` | Intel RealSense depth cameras |
| [`features/python-ai/python-ai.yml`](../features/python-ai/python-ai.yml) | `meta-python-ai` | Python AI/ML stack |
| [`features/cve/sbom-cve-check.yaml`](../features/cve/sbom-cve-check.yaml) | `meta-sbom-cve-check` | SBOM generation and CVE scanning |
| [`yocto/features/tpm.yaml`](../yocto/features/tpm.yaml) | `meta-security` | TPM 2.0 support |
| [`yocto/features/pulseaudio.yml`](../yocto/features/pulseaudio.yml) | Poky | PulseAudio |

To promote one of these to a real feature, add a `registry.features` entry and reference it from
a preset — see [adding-a-board.md](adding-a-board.md).

---

## 3. Vendor-Bundled Fragments

Some fragments are not registry features at all: they are pulled in directly by vendor BSP
fragments, so they are enabled implicitly by choosing the corresponding `vendor_release`.

| Fragment(s) | Pulled in by | Purpose |
|-------------|--------------|---------|
| [`features/qt/`](../features/qt) (`qt6.3` … `qt6.11.0`) | NXP `imx-*` fragments, per release | Qt 6 via `meta-qt6`; the version is pinned per NXP BSP release |
| [`features/browser/browser.yml`](../features/browser/browser.yml) | NXP `imx-*` fragments | Chromium/WebKit browser stack |
| [`features/sbom/timesys.yml`](../features/sbom/timesys.yml) (+ [`timesys-whinlatter.yml`](../features/sbom/timesys-whinlatter.yml), [`timesys-wrynose.yml`](../features/sbom/timesys-wrynose.yml)) | NXP `imx-*` fragments | Timesys Vigiles SBOM/CVE reporting |
| [`features/ros2/`](../features/ros2) (`humble`, `jazzy`, `kilted`, `rolling`) | the `ros2-*` registry releases | ROS 2 distributions via `meta-ros` |
| [`features/deep-learning/tensorflow.yml`](../features/deep-learning/tensorflow.yml) | MediaTek and Qualcomm vendor fragments | TensorFlow Lite |
| [`compilers/clang/clang.yml`](../compilers/clang/clang.yml) | several device fragments | Build with Clang (`meta-clang`) instead of GCC |

---

## 4. Composing Features Manually

Anything in the tree can be used directly with KAS, even without a registry entry:

```bash
kas build yocto/yocto.yaml:yocto/releases/scarthgap.yml:yocto/distro/poky.yaml:\
vendors/qemu/machine/qemux86-64.yml:features/protocols/zenoh.yml
```

This is the escape hatch for preview fragments and for one-off experiments.
