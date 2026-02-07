# SBOM (Software Bill of Materials) Feature

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. What is SBOM?](#3-what-is-sbom)
- [4. SBOM Information Flow](#4-sbom-information-flow)
- [5. Repository](#5-repository)
- [6. Features](#6-features)
- [7. Use Cases](#7-use-cases)
- [8. SBOM Standards](#8-sbom-standards)
  - [8.1. SPDX (Software Package Data Exchange)](#81-spdx-software-package-data-exchange)
  - [8.2. CycloneDX](#82-cyclonedx)
- [9. Vulnerability Severity Levels](#9-vulnerability-severity-levels)
- [10. Timesys Vigiles Workflow](#10-timesys-vigiles-workflow)
- [11. Configuration Files](#11-configuration-files)
- [12. Usage Example](#12-usage-example)
- [13. Requirements](#13-requirements)
- [14. SBOM Report Example](#14-sbom-report-example)
- [15. Integration in CI/CD](#15-integration-in-cicd)
- [16. Benefits](#16-benefits)
  - [16.1. Security](#161-security)
  - [16.2. Compliance](#162-compliance)
  - [16.3. Risk Management](#163-risk-management)
- [17. SBOM Lifecycle Management](#17-sbom-lifecycle-management)
- [18. Best Practices](#18-best-practices)
- [19. Common Vulnerabilities](#19-common-vulnerabilities)
- [20. Troubleshooting](#20-troubleshooting)
  - [20.1. Issue: SBOM Generation Fails](#201-issue-sbom-generation-fails)
  - [20.2. Issue: False Positives in CVE Report](#202-issue-false-positives-in-cve-report)
  - [20.3. Issue: Too Many Vulnerabilities](#203-issue-too-many-vulnerabilities)
- [21. Related Features](#21-related-features)
- [22. Regulatory Compliance](#22-regulatory-compliance)
- [23. Additional Resources](#23-additional-resources)


## 1. Overview

The SBOM feature integrates Timesys Vigiles vulnerability management and SBOM generation capabilities into the BSP build process, enabling comprehensive tracking of software components, licenses, and security vulnerabilities.

## 2. Architecture

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

## 3. What is SBOM?

A Software Bill of Materials (SBOM) is a comprehensive inventory of all software components, libraries, and dependencies used in a product, including:

- **Component names** and versions
- **Licenses** for each component
- **Dependencies** between components
- **Security vulnerabilities** (CVEs)
- **Suppliers** and origins
- **Hashes** for integrity verification

## 4. SBOM Information Flow

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

## 5. Repository

- **Layer**: meta-timesys
- **Source**: https://github.com/TimesysGit/meta-timesys.git
- **Maintained by**: Timesys Corporation
- **Service**: Vigiles vulnerability monitoring

## 6. Features

- **Automated SBOM Generation**: Automatically create SBOM during build
- **Vulnerability Scanning**: Check against NVD and other CVE databases
- **License Compliance**: Track and report all software licenses
- **Continuous Monitoring**: Ongoing vulnerability alerts
- **Historical Tracking**: Version-to-version comparison
- **Export Formats**: SPDX, CycloneDX, JSON formats
- **Supply Chain Security**: Track component provenance

## 7. Use Cases

- **Regulatory Compliance**: Meet FDA, automotive safety standards (ISO 26262)
- **Security Auditing**: Identify and remediate vulnerabilities
- **License Management**: Ensure open-source license compliance
- **Supply Chain Risk**: Track third-party component risks
- **Customer Requirements**: Provide SBOM to customers/partners
- **Incident Response**: Quick identification of affected products
- **Procurement**: Vendor software assessment

## 8. SBOM Standards

### 8.1. SPDX (Software Package Data Exchange)
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

### 8.2. CycloneDX
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

## 9. Vulnerability Severity Levels

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

## 10. Timesys Vigiles Workflow

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

## 11. Configuration Files

- `timesys-kirkstone.yml` - Kirkstone release
- `timesys-mickledore.yml` - Mickledore release
- `timesys-scarthgap.yml` - Scarthgap release
- `timesys-styhead.yml` - Styhead release
- `timesys-walnascar.yml` - Walnascar release

Each configuration is tailored for the specific Yocto release.

## 12. Usage Example

To include SBOM generation in your BSP build, you need to create a custom YAML configuration file that includes the Timesys feature layer.

Example YAML configuration (`custom-bsp-with-sbom.yaml`):
```yaml
header:
  version: 14
  includes:
    - adv-bsp-oenxp-scarthgap-rsb3720.yaml
    - features/sbom/timesys-scarthgap.yml
```

Then build with KAS:
```bash
kas-container build custom-bsp-with-sbom.yaml
```

See the main README's "HowTo build a BSP using KAS" section for more details on working with KAS configuration files.

## 13. Requirements

- **Vigiles Account**: Timesys Vigiles subscription (or free tier)
- **API Key**: Configure Vigiles API credentials
- **Network Access**: Build system needs internet for CVE database
- **Build Time**: Additional 5-10 minutes for SBOM generation

## 14. SBOM Report Example

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

## 15. Integration in CI/CD

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

## 16. Benefits

### 16.1. Security
- Early vulnerability detection
- Continuous monitoring for new CVEs
- Reduced time to remediation
- Supply chain attack prevention

### 16.2. Compliance
- Meet regulatory requirements
- License compliance tracking
- Audit trail for software components
- Export reports for customers

### 16.3. Risk Management
- Understand component risks
- Track outdated/EOL components
- Prioritize security updates
- Vendor risk assessment

## 17. SBOM Lifecycle Management

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

## 18. Best Practices

1. **Regular Scans**: Check for new vulnerabilities weekly
2. **Prioritize Fixes**: Address critical/high severity first
3. **Track Updates**: Document all security patches
4. **Version Control**: Store SBOMs in version control
5. **Customer Sharing**: Provide SBOM to customers/partners
6. **Automation**: Integrate into CI/CD pipeline
7. **License Review**: Regularly audit license compliance

## 19. Common Vulnerabilities

| Type | Example | Risk |
|------|---------|------|
| **Memory Corruption** | Buffer overflow | Remote code execution |
| **Injection** | SQL/Command injection | Data breach |
| **Cryptographic** | Weak encryption | Information disclosure |
| **Authentication** | Broken auth | Unauthorized access |
| **Denial of Service** | Resource exhaustion | Service disruption |

## 20. Troubleshooting

### 20.1. Issue: SBOM Generation Fails
- Check internet connectivity
- Verify Vigiles API credentials
- Check build log for errors

### 20.2. Issue: False Positives in CVE Report
- Review CVE applicability to your use case
- Mark as false positive in Vigiles
- Document reasoning for audit trail

### 20.3. Issue: Too Many Vulnerabilities
- Prioritize by severity (critical/high first)
- Check if CVE affects your configuration
- Plan phased remediation approach

## 21. Related Features

- **OTA**: Deploy security updates remotely
- All features benefit from vulnerability tracking

## 22. Regulatory Compliance

SBOMs help meet requirements from:
- **FDA**: Medical device cybersecurity
- **NHTSA**: Automotive cybersecurity
- **EU Cyber Resilience Act**: Product security
- **Executive Order 14028**: Federal supply chain security

## 23. Additional Resources

- [Timesys Vigiles](https://www.timesys.com/security/vigiles/)
- [SPDX Specification](https://spdx.dev/)
- [CycloneDX Specification](https://cyclonedx.org/)
- [NIST SBOM Resources](https://www.nist.gov/sbom)
- [meta-timesys Layer](https://github.com/TimesysGit/meta-timesys)
- [NTIA SBOM Guide](https://www.ntia.gov/sbom)
