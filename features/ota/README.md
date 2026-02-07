# OTA (Over-The-Air Updates) Feature

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. Supported OTA Technologies](#3-supported-ota-technologies)
  - [3.1. 1. OSTree (libostree)](#31-1-ostree-libostree)
  - [3.2. 2. RAUC (Robust Auto-Update Controller)](#32-2-rauc-robust-auto-update-controller)
  - [3.3. 3. SWUpdate](#33-3-swupdate)
- [4. Comparison Matrix](#4-comparison-matrix)
- [5. Update Process Flow](#5-update-process-flow)
- [6. Configuration Files](#6-configuration-files)
  - [6.1. OSTree](#61-ostree)
  - [6.2. RAUC](#62-rauc)
  - [6.3. SWUpdate](#63-swupdate)
- [7. Usage Examples](#7-usage-examples)
  - [7.1. OSTree-based OTA](#71-ostree-based-ota)
  - [7.2. RAUC-based OTA](#72-rauc-based-ota)
  - [7.3. SWUpdate-based OTA](#73-swupdate-based-ota)
- [8. Requirements](#8-requirements)
  - [8.1. Common Requirements](#81-common-requirements)
  - [8.2. Storage Sizing](#82-storage-sizing)
- [9. Security Considerations](#9-security-considerations)
- [10. Best Practices](#10-best-practices)
- [11. Troubleshooting](#11-troubleshooting)
  - [11.1. Common Issues](#111-common-issues)
- [12. Related Features](#12-related-features)
- [13. Additional Resources](#13-additional-resources)


## 1. Overview

The OTA feature provides comprehensive over-the-air update capabilities for embedded systems, supporting multiple update strategies and technologies to ensure reliable and secure firmware updates in production environments.

## 2. Architecture

```
┌─────────────────────────────────────────────────────┐
│              Update Server                          │
│  (Hosts update artifacts and metadata)              │
└────────────────┬────────────────────────────────────┘
                 │ HTTPS/HTTP
                 │ Update Package
                 ▼
┌─────────────────────────────────────────────────────┐
│              Target Device                          │
│  ┌─────────────────────────────────────────────┐   │
│  │  Update Client (OSTree/RAUC/SWUpdate)       │   │
│  ├─────────────────────────────────────────────┤   │
│  │  Bootloader (U-Boot with A/B support)       │   │
│  ├─────────────────────────────────────────────┤   │
│  │  Partition A (Active)  │ Partition B (Backup)│  │
│  │  ┌──────────────────┐  │ ┌──────────────────┐│  │
│  │  │  Root FS         │  │ │  Root FS         ││  │
│  │  │  (Current)       │  │ │  (Update Target) ││  │
│  │  └──────────────────┘  │ └──────────────────┘│  │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## 3. Supported OTA Technologies

### 3.1. 1. OSTree (libostree)

**Image-based atomic updates with Git-like version control**

```
OSTree Repository Structure:
┌─────────────────────────────────┐
│  ostree repo                    │
│  ├── objects/                   │
│  │   └── (content-addressed)    │
│  ├── refs/                      │
│  │   └── heads/                 │
│  │       └── os/version         │
│  └── config                     │
└─────────────────────────────────┘
```

**Advantages:**
- Atomic updates with rollback capability
- Efficient delta updates (only changed files)
- Git-like deployment model
- Strong integrity verification

**Use Cases:**
- Linux distributions (similar to Fedora Silverblue)
- Container host systems
- Systems requiring complex update orchestration

### 3.2. 2. RAUC (Robust Auto-Update Controller)

**Partition-based atomic updates with flexible strategies**

```
RAUC Update Flow:
┌────────────┐
│ Update     │
│ Bundle     │──┐
│ (.raucb)   │  │
└────────────┘  │
                ▼
         ┌──────────────┐
         │ RAUC Service │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
  Slot A     Slot B      Data
 (Active)   (Inactive)  (Persist)
```

**Advantages:**
- Flexible partition schemes (A/B, recovery, etc.)
- Atomic bootloader integration
- Cryptographic signature verification
- Hardware watchdog integration

**Use Cases:**
- Industrial embedded systems
- Automotive applications
- Critical infrastructure devices

### 3.3. 3. SWUpdate

**Flexible software update framework with multiple strategies**

```
SWUpdate Architecture:
┌─────────────────────────────────┐
│  Update Package (.swu)          │
│  ├── sw-description (metadata)  │
│  ├── firmware.img               │
│  ├── rootfs.tar.gz              │
│  └── scripts/                   │
└──────────────┬──────────────────┘
               ▼
        ┌──────────────┐
        │  SWUpdate    │
        │  Daemon      │
        └──────┬───────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
  Images   Packages   Scripts
```

**Advantages:**
- Multiple update strategies
- Web interface included
- Symmetric/asymmetric A/B updates
- Extensible via Lua scripts

**Use Cases:**
- Devices with web UI requirements
- Complex update scenarios
- Multi-component systems

## 4. Comparison Matrix

| Feature | OSTree | RAUC | SWUpdate |
|---------|--------|------|----------|
| **Update Type** | File-based | Image/partition | Flexible |
| **Rollback** | ✅ Automatic | ✅ Automatic | ✅ Configurable |
| **Delta Updates** | ✅ Efficient | ❌ Full image | ⚠️ Partial support |
| **Signature Verification** | ✅ GPG | ✅ CMS/OpenSSL | ✅ RSA/CMS |
| **Bootloader Integration** | GRUB/U-Boot | U-Boot | U-Boot |
| **Complexity** | Medium | Low | Medium |
| **Disk Overhead** | Low | High (2x space) | High (2x space) |
| **Network Efficiency** | High | Low | Medium |

## 5. Update Process Flow

```
┌──────────────────────────────────────────────────┐
│ 1. Check for Updates                             │
│    - Query update server                         │
│    - Compare versions                            │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 2. Download Update                               │
│    - Transfer update package                     │
│    - Verify checksums/signatures                 │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 3. Install Update                                │
│    - Write to inactive partition                 │
│    - Update bootloader configuration             │
└────────────────┬─────────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────────┐
│ 4. Reboot to New System                          │
│    - Switch to updated partition                 │
│    - Run integrity checks                        │
└────────────────┬─────────────────────────────────┘
                 ▼
         ┌───────┴────────┐
         ▼                ▼
    ┌─────────┐      ┌─────────┐
    │ Success │      │ Failure │
    │ Commit  │      │ Rollback│
    └─────────┘      └─────────┘
```

## 6. Configuration Files

### 6.1. OSTree
- `ostree/scarthgap.yml` - Scarthgap release
- `ostree/styhead.yml` - Styhead release
- `ostree/walnascar.yml` - Walnascar release
- `ostree/adv-ota-*.yml` - Advantech-specific configurations

### 6.2. RAUC
- `rauc/scarthgap.yml` - Scarthgap release
- `rauc/styhead.yml` - Styhead release
- `rauc/walnascar.yml` - Walnascar release
- `rauc/adv-ota-*.yml` - Advantech-specific configurations

### 6.3. SWUpdate
- `swupdate/common.yml` - Common configuration
- `swupdate/scarthgap.yml` - Scarthgap release
- `swupdate/styhead.yml` - Styhead release
- `swupdate/walnascar.yml` - Walnascar release
- `swupdate/adv-ota-*.yml` - Advantech-specific configurations

## 7. Usage Examples

### 7.1. OSTree-based OTA

```bash
# Using the dedicated OTA recipe
just ota-mbsp <machine> ostree <yocto-release>

# Example for RSB3720 with Scarthgap
just ota-mbsp rsb3720 ostree scarthgap
```

### 7.2. RAUC-based OTA

```bash
# Using the dedicated OTA recipe
just ota-mbsp <machine> rauc <yocto-release>

# Example for RSB3720 with Scarthgap
just ota-mbsp rsb3720 rauc scarthgap
```

### 7.3. SWUpdate-based OTA

```bash
# Using the dedicated OTA recipe
just ota-mbsp <machine> swupdate <yocto-release>

# Example for RSB3720 with Scarthgap
just ota-mbsp rsb3720 swupdate scarthgap
```

## 8. Requirements

### 8.1. Common Requirements
- **Bootloader**: U-Boot with A/B boot support
- **Storage**: Sufficient space for dual partitions (or OSTree repo)
- **Network**: Reliable connectivity to update server
- **Security**: TPM/secure boot (recommended)

### 8.2. Storage Sizing

| Technology | Storage Overhead | Example (2GB rootfs) |
|-----------|------------------|---------------------|
| OSTree | ~120% | 2.4 GB |
| RAUC | ~200% | 4.0 GB |
| SWUpdate | ~200% | 4.0 GB |

## 9. Security Considerations

```
┌─────────────────────────────────────────┐
│  Security Layers                        │
├─────────────────────────────────────────┤
│  1. Transport Security (TLS/HTTPS)      │
├─────────────────────────────────────────┤
│  2. Package Signature Verification      │
│     (GPG/RSA/CMS)                       │
├─────────────────────────────────────────┤
│  3. Checksum Validation                 │
│     (SHA256/SHA512)                     │
├─────────────────────────────────────────┤
│  4. Secure Boot (Optional)              │
│     (Verified boot chain)               │
├─────────────────────────────────────────┤
│  5. Rollback Protection                 │
│     (Anti-downgrade mechanism)          │
└─────────────────────────────────────────┘
```

## 10. Best Practices

1. **Test Updates**: Always test in staging before production
2. **Staged Rollout**: Deploy to subsets of devices first
3. **Monitoring**: Implement update success/failure tracking
4. **Bandwidth**: Schedule updates during off-peak hours
5. **Fallback**: Ensure rollback mechanism is tested
6. **Validation**: Implement post-update health checks

## 11. Troubleshooting

### 11.1. Common Issues

| Issue | Solution |
|-------|----------|
| Update fails to download | Check network connectivity, server availability |
| Boot fails after update | Rollback should occur automatically; check bootloader |
| Signature verification fails | Verify signing keys are correctly provisioned |
| Insufficient space | Check partition sizes, cleanup old artifacts |

## 12. Related Features

- **Protocols**: Use Zenoh for update notifications
- **SBOM**: Track component versions and vulnerabilities

## 13. Additional Resources

- [OSTree Documentation](https://ostreedev.github.io/ostree/)
- [RAUC Documentation](https://rauc.readthedocs.io/)
- [SWUpdate Documentation](https://sbabic.github.io/swupdate/)
- [Yocto OTA Guide](https://docs.yoctoproject.org/)
