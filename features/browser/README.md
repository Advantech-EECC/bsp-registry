# Browser Feature

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. Supported Yocto Releases](#3-supported-yocto-releases)
- [4. Repository](#4-repository)
- [5. Features](#5-features)
- [6. Use Cases](#6-use-cases)
- [7. Configuration Files](#7-configuration-files)
- [8. Usage Example](#8-usage-example)
- [9. Requirements](#9-requirements)
- [10. Known Limitations](#10-known-limitations)
- [11. Related Features](#11-related-features)
- [12. Additional Resources](#12-additional-resources)


## 1. Overview

The Browser feature adds Chromium web browser support to your BSP image, enabling web-based applications and user interfaces on embedded systems.

## 2. Architecture

```
┌─────────────────────────────────────────┐
│         User Application                │
│    (HTML/CSS/JavaScript/WebUI)          │
├─────────────────────────────────────────┤
│         Chromium Browser                │
│    (Rendering Engine + V8 JS)           │
├─────────────────────────────────────────┤
│         Graphics Stack                  │
│    (Wayland/X11 + GPU drivers)          │
├─────────────────────────────────────────┤
│         Linux Kernel                    │
└─────────────────────────────────────────┘
```

## 3. Supported Yocto Releases

The browser feature is available for the following Yocto releases:

- **Kirkstone** (LTS)
- **Mickledore**
- **Scarthgap** (LTS)
- **Styhead**
- **Walnascar**

## 4. Repository

- **Layer**: meta-browser (meta-chromium)
- **Source**: https://github.com/OSSystems/meta-browser.git
- **Maintained by**: OSSystems

## 5. Features

- Full Chromium browser with hardware acceleration support
- WebGL and Canvas rendering capabilities
- Modern web standards compliance (HTML5, CSS3, ES6+)
- Hardware video decoding support (where available)
- Touch screen support for HMI applications
- Kiosk mode support for embedded displays

## 6. Use Cases

- **Industrial HMI**: Web-based human-machine interfaces
- **Digital Signage**: Content display and management
- **IoT Dashboards**: Real-time monitoring and control
- **Embedded Web Applications**: Modern web app deployment on embedded devices
- **Testing and Development**: Web-based development tools

## 7. Configuration Files

Each Yocto release has its own configuration file:
- `kirkstone.yml` - For Kirkstone release
- `mickledore.yml` - For Mickledore release
- `scarthgap.yml` - For Scarthgap release
- `styhead.yml` - For Styhead release
- `walnascar.yml` - For Walnascar release

## 8. Usage Example

To include the browser feature in your BSP build, you need to create a custom YAML configuration file that includes the browser feature layer. The browser feature is not directly supported via command-line arguments.

Example YAML configuration (`custom-bsp-with-browser.yaml`):
```yaml
header:
  version: 14
  includes:
    - adv-bsp-oenxp-scarthgap-rsb3720.yaml
    - features/browser/scarthgap.yml
```

Then build with KAS:
```bash
kas-container build custom-bsp-with-browser.yaml
```

See the main README's "HowTo build a BSP using KAS" section for more details on working with KAS configuration files.

## 9. Requirements

- Sufficient system memory (minimum 512MB RAM recommended, 1GB+ preferred)
- GPU with graphics acceleration (recommended)
- Display output (HDMI, LVDS, etc.)
- Wayland or X11 compositor

## 10. Known Limitations

- Chromium requires significant disk space (200MB+ for binaries)
- Initial build time can be extensive (several hours)
- Performance varies based on hardware capabilities
- Some advanced features may require additional configuration

## 11. Related Features

- **Qt**: Can be combined with Qt WebEngine for Qt-based web applications
- **Protocols**: Works with Zenoh for networked web applications

## 12. Additional Resources

- [Chromium Project](https://www.chromium.org/)
- [meta-browser Documentation](https://github.com/OSSystems/meta-browser)
- [Yocto Project Graphics Stack](https://www.yoctoproject.org/)
