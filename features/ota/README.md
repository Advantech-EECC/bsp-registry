# OTA (Over-The-Air Updates) Feature

## Overview

The OTA feature provides comprehensive over-the-air update capabilities for embedded systems, supporting multiple update strategies and technologies to ensure reliable and secure firmware updates in production environments.

## Architecture

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

## Supported OTA Technologies

### 1. OSTree (libostree)

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

### 2. RAUC (Robust Auto-Update Controller)

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

### 3. SWUpdate

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

## Comparison Matrix

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

## Update Process Flow

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

## Configuration Files

### OSTree
- `ostree/scarthgap.yml` - Scarthgap release
- `ostree/styhead.yml` - Styhead release
- `ostree/walnascar.yml` - Walnascar release
- `ostree/adv-ota-*.yml` - Advantech-specific configurations

### RAUC
- `rauc/scarthgap.yml` - Scarthgap release
- `rauc/styhead.yml` - Styhead release
- `rauc/walnascar.yml` - Walnascar release
- `rauc/adv-ota-*.yml` - Advantech-specific configurations

### SWUpdate
- `swupdate/common.yml` - Common configuration
- `swupdate/scarthgap.yml` - Scarthgap release
- `swupdate/styhead.yml` - Styhead release
- `swupdate/walnascar.yml` - Walnascar release
- `swupdate/adv-ota-*.yml` - Advantech-specific configurations

## Usage Examples

### OSTree-based OTA

```bash
# Using BSP Registry Manager
just mbsp <board-name> <yocto-release> ota/ostree

# Example for RSB3720 with Scarthgap
just mbsp rsb3720 scarthgap ota/ostree
```

### RAUC-based OTA

```bash
# Using BSP Registry Manager
just mbsp <board-name> <yocto-release> ota/rauc

# Example for RSB3720 with Scarthgap
just mbsp rsb3720 scarthgap ota/rauc
```

### SWUpdate-based OTA

```bash
# Using BSP Registry Manager
just mbsp <board-name> <yocto-release> ota/swupdate

# Example for RSB3720 with Scarthgap
just mbsp rsb3720 scarthgap ota/swupdate
```

## Requirements

### Common Requirements
- **Bootloader**: U-Boot with A/B boot support
- **Storage**: Sufficient space for dual partitions (or OSTree repo)
- **Network**: Reliable connectivity to update server
- **Security**: TPM/secure boot (recommended)

### Storage Sizing

| Technology | Storage Overhead | Example (2GB rootfs) |
|-----------|------------------|---------------------|
| OSTree | ~120% | 2.4 GB |
| RAUC | ~200% | 4.0 GB |
| SWUpdate | ~200% | 4.0 GB |

## Security Considerations

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

## Best Practices

1. **Test Updates**: Always test in staging before production
2. **Staged Rollout**: Deploy to subsets of devices first
3. **Monitoring**: Implement update success/failure tracking
4. **Bandwidth**: Schedule updates during off-peak hours
5. **Fallback**: Ensure rollback mechanism is tested
6. **Validation**: Implement post-update health checks

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Update fails to download | Check network connectivity, server availability |
| Boot fails after update | Rollback should occur automatically; check bootloader |
| Signature verification fails | Verify signing keys are correctly provisioned |
| Insufficient space | Check partition sizes, cleanup old artifacts |

## Related Features

- **Protocols**: Use Zenoh for update notifications
- **SBOM**: Track component versions and vulnerabilities

## Additional Resources

- [OSTree Documentation](https://ostreedev.github.io/ostree/)
- [RAUC Documentation](https://rauc.readthedocs.io/)
- [SWUpdate Documentation](https://sbabic.github.io/swupdate/)
- [Yocto OTA Guide](https://docs.yoctoproject.org/)
