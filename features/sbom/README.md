# SBOM (Software Bill of Materials) Feature

## Overview

The SBOM feature integrates Timesys Vigiles vulnerability management and SBOM generation capabilities into the BSP build process, enabling comprehensive tracking of software components, licenses, and security vulnerabilities.

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Yocto Build System                      │
│  (BitBake building packages)                    │
└────────────────┬────────────────────────────────┘
                 │ Collects metadata
                 ▼
┌─────────────────────────────────────────────────┐
│      Timesys Vigiles Integration               │
│  (SBOM generation & vulnerability scanning)     │
└────────────────┬────────────────────────────────┘
                 │ Generates SBOM & CVE report
                 ▼
┌─────────────────────────────────────────────────┐
│              Output Artifacts                   │
│  ┌───────────────────────────────────────────┐ │
│  │ • SBOM (Software Bill of Materials)       │ │
│  │ • CVE Report (Known vulnerabilities)      │ │
│  │ • License Report                          │ │
│  │ • Component Inventory                     │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## What is SBOM?

A Software Bill of Materials (SBOM) is a comprehensive inventory of all software components, libraries, and dependencies used in a product, including:

- **Component names** and versions
- **Licenses** for each component
- **Dependencies** between components
- **Security vulnerabilities** (CVEs)
- **Suppliers** and origins
- **Hashes** for integrity verification

## SBOM Information Flow

```
Build Process
      │
      ├─► Package A (v1.2.3)
      ├─► Package B (v2.0.1)
      ├─► Package C (v3.1.0)
      │
      ▼
  SBOM Generator
      │
      ├─► Component List
      ├─► License Info
      ├─► CVE Database Lookup
      │
      ▼
  SBOM Document
  ┌─────────────────────────────┐
  │ Components: 347             │
  │ Licenses: Apache, GPL, MIT  │
  │ CVEs: 12 (3 critical)       │
  │ Last Updated: 2024-01-30    │
  └─────────────────────────────┘
```

## Repository

- **Layer**: meta-timesys
- **Source**: https://github.com/TimesysGit/meta-timesys.git
- **Maintained by**: Timesys Corporation
- **Service**: Vigiles vulnerability monitoring

## Features

- **Automated SBOM Generation**: Automatically create SBOM during build
- **Vulnerability Scanning**: Check against NVD and other CVE databases
- **License Compliance**: Track and report all software licenses
- **Continuous Monitoring**: Ongoing vulnerability alerts
- **Historical Tracking**: Version-to-version comparison
- **Export Formats**: SPDX, CycloneDX, JSON formats
- **Supply Chain Security**: Track component provenance

## Use Cases

- **Regulatory Compliance**: Meet FDA, automotive safety standards (ISO 26262)
- **Security Auditing**: Identify and remediate vulnerabilities
- **License Management**: Ensure open-source license compliance
- **Supply Chain Risk**: Track third-party component risks
- **Customer Requirements**: Provide SBOM to customers/partners
- **Incident Response**: Quick identification of affected products
- **Procurement**: Vendor software assessment

## SBOM Standards

### SPDX (Software Package Data Exchange)
```
SPDX Document
├── Package: busybox
│   ├── Version: 1.36.1
│   ├── License: GPL-2.0
│   ├── Checksum: sha256:abc123...
│   └── Supplier: busybox.net
├── Package: openssl
│   ├── Version: 3.0.8
│   ├── License: Apache-2.0
│   └── CVEs: CVE-2023-XXXXX
```

### CycloneDX
```xml
<components>
  <component type="library">
    <name>libssl</name>
    <version>3.0.8</version>
    <licenses>
      <license><id>Apache-2.0</id></license>
    </licenses>
  </component>
</components>
```

## Vulnerability Severity Levels

```
┌──────────────────────────────────┐
│  CRITICAL  (CVSS 9.0-10.0)       │  ← Immediate action required
├──────────────────────────────────┤
│  HIGH      (CVSS 7.0-8.9)        │  ← Urgent patching needed
├──────────────────────────────────┤
│  MEDIUM    (CVSS 4.0-6.9)        │  ← Schedule remediation
├──────────────────────────────────┤
│  LOW       (CVSS 0.1-3.9)        │  ← Monitor for updates
└──────────────────────────────────┘
```

## Timesys Vigiles Workflow

```
┌────────────────────────────────────────┐
│ 1. Build BSP with Timesys Integration │
│    (Collect package metadata)          │
├────────────────────────────────────────┤
│ 2. Upload SBOM to Vigiles Service     │
│    (Automated via build)               │
├────────────────────────────────────────┤
│ 3. Vigiles Analyzes Components        │
│    (CVE matching, license checking)    │
├────────────────────────────────────────┤
│ 4. Generate Report                     │
│    (Vulnerabilities, recommendations)  │
├────────────────────────────────────────┤
│ 5. Continuous Monitoring               │
│    (New CVEs trigger alerts)           │
└────────────────────────────────────────┘
```

## Configuration Files

- `timesys-kirkstone.yml` - Kirkstone release
- `timesys-mickledore.yml` - Mickledore release
- `timesys-scarthgap.yml` - Scarthgap release
- `timesys-styhead.yml` - Styhead release
- `timesys-walnascar.yml` - Walnascar release

Each configuration is tailored for the specific Yocto release.

## Usage Example

To include SBOM generation in your BSP build:

```bash
# Using BSP Registry Manager
just bsp <board-name> <yocto-release> sbom/timesys-<release>

# Example for RSB3720 with Scarthgap
just bsp rsb3720 scarthgap sbom/timesys-scarthgap
```

## Requirements

- **Vigiles Account**: Timesys Vigiles subscription (or free tier)
- **API Key**: Configure Vigiles API credentials
- **Network Access**: Build system needs internet for CVE database
- **Build Time**: Additional 5-10 minutes for SBOM generation

## SBOM Report Example

```
═══════════════════════════════════════════
  Product: RSB3720 BSP Scarthgap
  Build Date: 2024-01-30
  Total Packages: 347
═══════════════════════════════════════════

Vulnerability Summary:
  Critical:  3
  High:     12
  Medium:   28
  Low:      45

Top Vulnerabilities:
  1. CVE-2024-XXXXX (openssl 3.0.8)
     CVSS: 9.8 (Critical)
     Fix: Upgrade to 3.0.9+

  2. CVE-2024-YYYYY (libcurl 8.1.0)
     CVSS: 8.2 (High)
     Fix: Upgrade to 8.1.2+

License Distribution:
  GPL-2.0:      78 packages
  Apache-2.0:   45 packages
  MIT:          123 packages
  BSD-3-Clause: 34 packages
  Other:        67 packages
```

## Integration in CI/CD

```
┌────────────────────┐
│  Code Commit       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  BSP Build         │
│  (with SBOM)       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Vigiles Scan      │
│  (CVE Check)       │
└─────────┬──────────┘
          │
     Pass │ Fail
          │
    ┌─────┴──────┐
    ▼            ▼
┌────────┐  ┌─────────┐
│ Deploy │  │ Block   │
│        │  │ & Alert │
└────────┘  └─────────┘
```

## Benefits

### Security
- Early vulnerability detection
- Continuous monitoring for new CVEs
- Reduced time to remediation
- Supply chain attack prevention

### Compliance
- Meet regulatory requirements
- License compliance tracking
- Audit trail for software components
- Export reports for customers

### Risk Management
- Understand component risks
- Track outdated/EOL components
- Prioritize security updates
- Vendor risk assessment

## SBOM Lifecycle Management

```
Development Phase
      │
      ├─► Generate SBOM
      │
Production Phase
      │
      ├─► Monitor for New CVEs
      │   (Daily/Weekly scans)
      │
Maintenance Phase
      │
      ├─► Update Components
      ├─► Regenerate SBOM
      ├─► Validate Changes
      │
End-of-Life
      │
      └─► Archive SBOM for Records
```

## Best Practices

1. **Regular Scans**: Check for new vulnerabilities weekly
2. **Prioritize Fixes**: Address critical/high severity first
3. **Track Updates**: Document all security patches
4. **Version Control**: Store SBOMs in version control
5. **Customer Sharing**: Provide SBOM to customers/partners
6. **Automation**: Integrate into CI/CD pipeline
7. **License Review**: Regularly audit license compliance

## Common Vulnerabilities

| Type | Example | Risk |
|------|---------|------|
| **Memory Corruption** | Buffer overflow | Remote code execution |
| **Injection** | SQL/Command injection | Data breach |
| **Cryptographic** | Weak encryption | Information disclosure |
| **Authentication** | Broken auth | Unauthorized access |
| **Denial of Service** | Resource exhaustion | Service disruption |

## Troubleshooting

### Issue: SBOM Generation Fails
- Check internet connectivity
- Verify Vigiles API credentials
- Check build log for errors

### Issue: False Positives in CVE Report
- Review CVE applicability to your use case
- Mark as false positive in Vigiles
- Document reasoning for audit trail

### Issue: Too Many Vulnerabilities
- Prioritize by severity (critical/high first)
- Check if CVE affects your configuration
- Plan phased remediation approach

## Related Features

- **OTA**: Deploy security updates remotely
- All features benefit from vulnerability tracking

## Regulatory Compliance

SBOMs help meet requirements from:
- **FDA**: Medical device cybersecurity
- **NHTSA**: Automotive cybersecurity
- **EU Cyber Resilience Act**: Product security
- **Executive Order 14028**: Federal supply chain security

## Additional Resources

- [Timesys Vigiles](https://www.timesys.com/security/vigiles/)
- [SPDX Specification](https://spdx.dev/)
- [CycloneDX Specification](https://cyclonedx.org/)
- [NIST SBOM Resources](https://www.nist.gov/sbom)
- [meta-timesys Layer](https://github.com/TimesysGit/meta-timesys)
- [NTIA SBOM Guide](https://www.ntia.gov/sbom)
