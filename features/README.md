# BSP Features Documentation

## Table of Contents

- [1. Overview](#1-overview)
- [2. Features Architecture](#2-features-architecture)
- [3. Available Features](#3-available-features)
  - [3.1. 🌐 [Browser](browser/README.md)](#31-browserbrowserreadmemd)
  - [3.2. 📷 [Cameras](cameras/README.md)](#32-camerascamerasreadmemd)
  - [3.3. 🤖 [Deep Learning](deep-learning/README.md)](#33-deep-learningdeep-learningreadmemd)
  - [3.4. 🔄 [OTA (Over-The-Air Updates)](ota/README.md)](#34-ota-over-the-air-updatesotareadmemd)
  - [3.5. 🌐 [Protocols](protocols/README.md)](#35-protocolsprotocolsreadmemd)
  - [3.6. 🐍 [Python AI](python-ai/README.md)](#36-python-aipython-aireadmemd)
  - [3.7. 🖼️ [Qt](qt/README.md)](#37-qtqtreadmemd)
  - [3.8. 🤖 [ROS2](ros2/README.md)](#38-ros2ros2readmemd)
  - [3.9. 📋 [SBOM](sbom/README.md)](#39-sbomsbomreadmemd)
- [4. Quick Start Guide](#4-quick-start-guide)
  - [4.1. 1. Choose Your Features](#41-1-choose-your-features)
  - [4.2. 2. Feature Combinations](#42-2-feature-combinations)
  - [4.3. 3. Build Your BSP](#43-3-build-your-bsp)
- [5. Feature Compatibility Matrix](#5-feature-compatibility-matrix)
- [6. Feature Selection Guide](#6-feature-selection-guide)
  - [6.1. By Industry](#61-by-industry)
  - [6.2. By Application Type](#62-by-application-type)
- [7. System Requirements](#7-system-requirements)
  - [7.1. Minimum Hardware Requirements](#71-minimum-hardware-requirements)
  - [7.2. Build System Requirements](#72-build-system-requirements)
- [8. Architecture Decision Guide](#8-architecture-decision-guide)
- [9. Development Workflow](#9-development-workflow)
- [10. Support and Resources](#10-support-and-resources)
  - [10.1. Documentation](#101-documentation)
  - [10.2. Community](#102-community)
  - [10.3. Commercial Support](#103-commercial-support)
- [11. Contributing](#11-contributing)
- [12. Version History](#12-version-history)
- [13. License](#13-license)


## 1. Overview

This directory contains comprehensive documentation for all available features that can be integrated into Advantech BSP builds. Each feature extends the base BSP with additional capabilities for specific use cases, from web browsers and AI acceleration to robotics and over-the-air updates.

## 2. Features Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    BSP Base System                         │
│         (Linux Kernel + Core System Libraries)             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Browser  │  │ Cameras  │  │Deep Learn│  │   OTA    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Protocols │  │Python AI │  │    Qt    │  │  ROS2    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                            │
│  ┌──────────┐                                             │
│  │   SBOM   │                                             │
│  └──────────┘                                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## 3. Available Features

### 3.1. 🌐 [Browser](browser/README.md)
Web browser support with Chromium for embedded web applications and HMI interfaces.

**Key Capabilities:**
- Full Chromium browser with hardware acceleration
- WebGL and HTML5 support
- Touch screen and kiosk mode
- Industrial HMI and digital signage

**Supported Releases:** Kirkstone, Mickledore, Scarthgap, Styhead, Walnascar

**Use Cases:** Web-based HMI, digital signage, IoT dashboards, embedded web apps

---

### 3.2. 📷 [Cameras](cameras/README.md)
Intel RealSense depth camera support for 3D vision and spatial computing.

**Key Capabilities:**
- RGB and depth sensing (D400 series)
- Point cloud generation
- IMU data integration
- librealsense2 SDK

**Supported Hardware:** RealSense D415, D435, D455

**Use Cases:** Robotics navigation, 3D scanning, gesture recognition, AR/VR, bin picking

---

### 3.3. 🤖 [Deep Learning](deep-learning/README.md)
Hailo AI accelerator integration for hardware-accelerated neural network inference.

**Key Capabilities:**
- 26 TOPS inference performance (Hailo-8)
- Low power (2.5W typical)
- GStreamer integration via TAPPAS
- ONNX, TensorFlow, PyTorch model support

**Supported Hardware:** Hailo-8, Hailo-8L (PCIe, M.2)

**Use Cases:** Object detection, image classification, pose estimation, facial recognition, quality control

---

### 3.4. 🔄 [OTA (Over-The-Air Updates)](ota/README.md)
Comprehensive OTA update solutions with multiple strategies for reliable firmware updates.

**Key Capabilities:**
- Three update technologies: OSTree, RAUC, SWUpdate
- Atomic updates with automatic rollback
- Signature verification and encryption
- A/B partition schemes

**Supported Releases:** Scarthgap, Styhead, Walnascar

**Use Cases:** Remote firmware updates, fleet management, security patching, production device maintenance

---

### 3.5. 🌐 [Protocols](protocols/README.md)
Zenoh protocol support for high-performance pub/sub communication in distributed systems.

**Key Capabilities:**
- Zero-copy shared memory transport
- Sub-millisecond latency
- Auto-discovery and routing
- Multi-transport (TCP, UDP, WebSocket)

**Supported Patterns:** Pub/Sub, Query/Reply, Storage

**Use Cases:** Robotics, IoT gateways, edge computing, distributed sensing, V2X communication

---

### 3.6. 🐍 [Python AI](python-ai/README.md)
Python-based AI and scientific computing libraries with NumPy, SciPy, and Fortran support.

**Key Capabilities:**
- NumPy for numerical computing
- SciPy for scientific algorithms
- Fortran compiler and BLAS/LAPACK
- libquadmath for quad-precision

**Supported Libraries:** NumPy, SciPy, Pandas, scikit-learn (add-on)

**Use Cases:** Machine learning, data analysis, signal processing, computer vision, statistics

---

### 3.7. 🖼️ [Qt](qt/README.md)
Qt framework for modern cross-platform GUI applications with hardware acceleration.

**Key Capabilities:**
- Qt 6.3 to 6.8.3 versions
- QML declarative UI
- Hardware-accelerated rendering
- Multi-touch support

**Supported Modules:** Qt Quick, Qt Widgets, Qt Multimedia, Qt Network

**Use Cases:** Industrial HMI, automotive dashboards, medical devices, kiosks, POS systems

---

### 3.8. 🤖 [ROS2](ros2/README.md)
Robot Operating System 2 for advanced robotics applications and autonomous systems.

**Key Capabilities:**
- DDS-based distributed communication
- Real-time capable
- Lifecycle management
- Rich ecosystem of packages

**Supported Distributions:** Humble (LTS), Jazzy (Latest LTS), Kilted, Rolling

**Use Cases:** Mobile robots, industrial automation, drones, autonomous vehicles, multi-robot systems

---

### 3.9. 📋 [SBOM](sbom/README.md)
Software Bill of Materials generation and vulnerability management with Timesys Vigiles.

**Key Capabilities:**
- Automated SBOM generation
- CVE vulnerability scanning
- License compliance tracking
- Continuous monitoring

**Supported Formats:** SPDX, CycloneDX

**Use Cases:** Regulatory compliance, security auditing, license management, supply chain risk

---

## 4. Quick Start Guide

### 4.1. 1. Choose Your Features

Select features based on your application requirements. Features are included by referencing their YAML configuration files in your BSP configuration, or by using dedicated just recipes for specific features:

```bash
# Example: Basic BSP build (no additional features)
just bsp rsb3720 scarthgap

# Example: Modular BSP build
just mbsp rsb3720 scarthgap

# Example: Robotics with ROS2
just ros-mbsp rsb3720 humble scarthgap

# Example: BSP with OTA updates
just ota-mbsp rsb3720 rauc scarthgap
```

To add other features (browser, cameras, Qt, deep learning, etc.), you need to create or modify YAML configuration files that include the desired feature YAML files. See the "HowTo build a BSP using KAS" section in the main README for details on working with KAS configuration files.

### 4.2. 2. Feature Combinations

Some features work particularly well together:

| Primary Feature | Complementary Features | Use Case |
|----------------|------------------------|----------|
| **ROS2** | Cameras, Deep Learning, Protocols | Autonomous robot |
| **Qt** | Browser, Cameras | Interactive HMI |
| **Deep Learning** | Cameras, Python AI | AI vision system |
| **OTA** | SBOM, any feature | Production deployment |
| **Protocols** | ROS2, Deep Learning | Distributed AI |

### 4.3. 3. Build Your BSP

```bash
# Standard BSP build
just bsp <board> <yocto-release> <feature1> <feature2> ...

# Modular BSP with OTA (recommended for production)
just mbsp <board> <yocto-release> <feature1> <feature2> ...
```

## 5. Feature Compatibility Matrix

| Feature | Kirkstone | Mickledore | Scarthgap | Styhead | Walnascar |
|---------|-----------|------------|-----------|---------|-----------|
| Browser | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cameras | ✅ | ✅ | ✅ | ✅ | ✅ |
| Deep Learning | ✅ | ✅ | ✅ | ✅ | ✅ |
| OTA | ❌ | ❌ | ✅ | ✅ | ✅ |
| Protocols | ✅ | ✅ | ✅ | ✅ | ✅ |
| Python AI | ✅ | ✅ | ✅ | ✅ | ✅ |
| Qt | ✅ | ✅ | ✅ | ✅ | ✅ |
| ROS2 | ✅ | ✅ | ✅ | ✅ | ✅ |
| SBOM | ✅ | ✅ | ✅ | ✅ | ✅ |

## 6. Feature Selection Guide

### 6.1. By Industry

**Industrial Automation**
- Qt (HMI)
- Protocols (Zenoh)
- OTA (Updates)
- SBOM (Compliance)

**Robotics**
- ROS2 (Framework)
- Cameras (Vision)
- Deep Learning (AI)
- Protocols (Communication)

**Medical Devices**
- Qt (User Interface)
- SBOM (Regulatory)
- OTA (Updates)
- Python AI (Analysis)

**Automotive**
- Qt (Dashboard)
- Cameras (ADAS)
- Deep Learning (Perception)
- OTA (Updates)

### 6.2. By Application Type

**Vision Systems**
- Cameras + Deep Learning + Python AI

**IoT Gateway**
- Protocols + OTA + SBOM

**HMI Panel**
- Qt + Browser

**Autonomous System**
- ROS2 + Cameras + Deep Learning

## 7. System Requirements

### 7.1. Minimum Hardware Requirements

| Feature | RAM | Storage | Special Hardware |
|---------|-----|---------|------------------|
| Browser | 512MB | 200MB | GPU recommended |
| Cameras | 2GB | 100MB | USB 3.0 required |
| Deep Learning | 2GB | 500MB | Hailo accelerator |
| OTA | 1GB | 2x rootfs | A/B partitions |
| Protocols | 256MB | 50MB | - |
| Python AI | 512MB | 200MB | - |
| Qt | 512MB | 150MB | GPU recommended |
| ROS2 | 512MB | 500MB | - |
| SBOM | 256MB | 50MB | Network access |

### 7.2. Build System Requirements

- **Disk Space**: 100GB+ free space
- **RAM**: 16GB+ recommended (32GB for large builds)
- **CPU**: Multi-core (8+ cores recommended)
- **Docker**: For containerized builds

## 8. Architecture Decision Guide

```
┌─────────────────────────────────────────────┐
│  What is your primary application?          │
└─────────────┬───────────────────────────────┘
              │
    ┌─────────┼─────────┬─────────────┐
    ▼         ▼         ▼             ▼
  Vision    HMI     Robotics      IoT/Edge
    │         │         │             │
    ▼         ▼         ▼             ▼
 Cameras    Qt      ROS2         Protocols
    +         +         +             +
Deep Learn Browser  Cameras         OTA
    +         +         +             +
Python AI   OTA    Deep Learn      SBOM
```

## 9. Development Workflow

1. **Prototype**: Start with minimal features, test quickly
2. **Integrate**: Add features incrementally, test each addition
3. **Optimize**: Tune performance, reduce footprint
4. **Secure**: Add SBOM, review vulnerabilities
5. **Deploy**: Add OTA for production updates

## 10. Support and Resources

### 10.1. Documentation
- Each feature has detailed README in its subdirectory
- See main [BSP Registry README](../README.md) for build instructions

### 10.2. Community
- GitHub Issues: Report bugs or request features
- GitHub Discussions: Ask questions, share knowledge

### 10.3. Commercial Support
- Advantech provides commercial BSP support
- Timesys Vigiles for security monitoring (SBOM feature)

## 11. Contributing

To add or improve feature documentation:
1. Follow the existing README structure
2. Include ASCII diagrams for clarity
3. Provide realistic use cases
4. Add code examples where appropriate
5. Update this central README with links

## 12. Version History

- **2024-01-30**: Initial comprehensive documentation
  - All 9 features documented
  - ASCII diagrams added
  - Central TOC created

## 13. License

This documentation is part of the Advantech BSP Registry project.
See [LICENSE](../LICENSE) for details.
