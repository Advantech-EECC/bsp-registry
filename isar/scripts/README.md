# isar-runqemu.sh

Helper script to boot an **Isar-built** image under **QEMU**.

It is intentionally simple:
- looks for build artifacts in a deploy directory
- selects a QEMU binary based on the `MACHINE`
- boots either:
  - **kernel+initrd** (and attaches a disk image as rootfs), or
  - **direct disk boot** (boots from the disk image alone)

## Quick start

From your Isar build directory (or any directory as long as you point `--deploy` to the right place):

```sh
./isar-runqemu.sh
```

Typical overrides:

```sh
./isar-runqemu.sh --machine qemuarm64 --deploy tmp/deploy/images/qemuarm64
```

## Prerequisites

- A completed Isar build that produced deploy artifacts (see **What it searches for**).
- The corresponding QEMU system emulator installed and available in `PATH`.

The script maps `MACHINE` to QEMU binaries:

| MACHINE | QEMU binary |
|---|---|
| `qemuarm` | `qemu-system-arm` |
| `qemuarm64` | `qemu-system-aarch64` |
| `qemux86` | `qemu-system-i386` |
| `qemux86-64` | `qemu-system-x86_64` |
| `qemuppc` | `qemu-system-ppc` |
| `qemumips` | `qemu-system-mips` |
| `qemumips64` | `qemu-system-mips64` |
| `qemuriscv32` | `qemu-system-riscv32` |
| `qemuriscv64` | `qemu-system-riscv64` |

On Debian/Ubuntu you typically want packages like:
- `qemu-system-arm` (covers `qemu-system-arm` and `qemu-system-aarch64`)
- `qemu-system-x86`
- `qemu-system-mips`
- `qemu-system-ppc`
- `qemu-system-riscv`

(Exact package names vary by distro.)

## Usage

```text
./isar-runqemu.sh [OPTIONS]
```

Run `./isar-runqemu.sh --help` to see the built-in help.

### Common options

- `-m, --machine MACHINE`
  - Select target machine (default: `qemuarm64`).
- `-d, --deploy DIR`
  - Path to the deploy directory (default: `tmp/deploy/images/${MACHINE}`).
- `--mem SIZE`
  - QEMU RAM size, e.g. `1G`, `512M`.
- `--serial MODE`
  - `stdio` (default), `telnet:host:port,server,nowait`, or `null`.
- `--network MODE`
  - `user` (default), `tap`, or `none`.
- `--display MODE`
  - `none` (default, implies `-nographic`), `gtk`, `sdl`, `curses`, ...
- `-k, --kernel FILE`
  - Use a specific kernel image instead of auto-detection.
- `-r, --initrd FILE`
  - Use a specific initrd instead of auto-detection.
- `-a, --append PARAMS`
  - Extra kernel command line arguments (only used for kernel+initrd boot).
- `-e, --extra ARGS`
  - Extra arguments passed verbatim to QEMU.

### Environment variables

The following can be set instead of passing flags:

- `MACHINE`, `DEPLOY_DIR`, `QEMU_MEM`, `QEMU_SERIAL`, `QEMU_NETWORK`, `QEMU_DISPLAY`

Notes:
- `IMAGE` is accepted by the script, but **currently not used** (it does not select artifacts by image name).

## What it searches for

The script expects `DEPLOY_DIR` to contain at least a bootable **disk/rootfs** image.

### Rootfs / disk image (required)

First match wins from these patterns:

- `*.wic`
- `*.ext4`
- `*.img`
- `rootfs.img`

If none are found, the script exits with an error.

### Kernel (optional)

If you don’t pass `--kernel`, it searches common names, e.g.:

- `vmlinuz`, `bzImage`, `vmlinux`, `Image`, `zImage`
- `*-vmlinuz`, `*-vmlinux`, `*-bzImage`, `*-Image`

### Initrd (optional)

If you don’t pass `--initrd`, it searches common names, e.g.:

- `initrd.img`, `initramfs.img`
- `*.initrd`, `*-initrd.img`, `*.cpio.gz`

## Boot modes

### 1) Kernel + initrd boot (preferred when available)

If both a kernel and initrd are found (or provided via overrides), the script:

- attaches the disk image via virtio (`virtio-blk-device`)
- supplies `-kernel` and `-initrd`
- builds a kernel command line like:
  - `root=/dev/vda2 rw console=<console> rootwait` plus your `--append`

Root device selection:
- For `*.ext4` images it uses `root=/dev/vda` (non-partitioned filesystem image).
- Otherwise it assumes partitioned images and uses `root=/dev/vda2`.

### 2) Direct disk boot

If it does **not** have both kernel and initrd, the script boots from the disk image directly.

In this mode it cannot inject kernel args (no `-append`), so your image must contain a bootloader configured to:
- boot successfully in QEMU
- output to the expected serial console

## Networking

- `--network user` (default)
  - Uses QEMU user-mode networking.
- `--network tap`
  - Uses `tap0` and assumes it is already configured.
  - The script prints a hint:
    - `sudo ip tuntap add tap0 mode tap`
- `--network none`
  - No network device is added.

## Exiting QEMU

The script prints:

- “Press Ctrl-A then X to exit QEMU.”

That’s the QEMU monitor escape sequence when running with `-nographic` / serial on stdio.

## Examples

Boot an `aarch64` image from a custom deploy directory:

```sh
./isar-runqemu.sh --machine qemuarm64 --deploy /path/to/build/tmp/deploy/images/qemuarm64
```

Increase memory and enable a GUI window:

```sh
./isar-runqemu.sh --mem 2G --display gtk
```

Expose serial over telnet (connect with `telnet localhost 1234`):

```sh
./isar-runqemu.sh --serial telnet:localhost:1234,server,nowait
```

Force a specific kernel/initrd and add kernel args:

```sh
./isar-runqemu.sh \
  --kernel Image \
  --initrd initrd.img \
  --append "loglevel=7 systemd.log_level=debug"
```

Pass extra QEMU args (example: enable KVM where supported):

```sh
./isar-runqemu.sh --extra "-enable-kvm"
```

## Troubleshooting

- **“Deployment directory not found”**
  - Your `--deploy` path is wrong. Point it at the directory that contains your `*.wic`/`*.img`/`*.ext4` artifact.

- **“QEMU binary … not found in PATH”**
  - Install the relevant QEMU system emulator package(s) for your `MACHINE`.

- **Kernel boots but cannot mount rootfs**
  - The default root device assumption may not match your image layout.
  - Use `--append` to override `root=...` (e.g. `root=/dev/vda3`) when using kernel+initrd boot.

- **No output on console**
  - Try `--serial stdio` and `--display none` (defaults).
  - If direct disk boot is used, ensure the bootloader inside the image uses the expected serial device.
