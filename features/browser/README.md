# Browser Feature

## Overview

The Browser feature adds Chromium web browser support to your BSP image, enabling web-based applications and user interfaces on embedded systems.

## Architecture

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

## Supported Yocto Releases

The browser feature is available for the following Yocto releases:

- **Kirkstone** (LTS)
- **Mickledore**
- **Scarthgap** (LTS)
- **Styhead**
- **Walnascar**

## Repository

- **Layer**: meta-browser (meta-chromium)
- **Source**: https://github.com/OSSystems/meta-browser.git
- **Maintained by**: OSSystems

## Features

- Full Chromium browser with hardware acceleration support
- WebGL and Canvas rendering capabilities
- Modern web standards compliance (HTML5, CSS3, ES6+)
- Hardware video decoding support (where available)
- Touch screen support for HMI applications
- Kiosk mode support for embedded displays

## Use Cases

- **Industrial HMI**: Web-based human-machine interfaces
- **Digital Signage**: Content display and management
- **IoT Dashboards**: Real-time monitoring and control
- **Embedded Web Applications**: Modern web app deployment on embedded devices
- **Testing and Development**: Web-based development tools

## Configuration Files

Each Yocto release has its own configuration file:
- `kirkstone.yml` - For Kirkstone release
- `mickledore.yml` - For Mickledore release
- `scarthgap.yml` - For Scarthgap release
- `styhead.yml` - For Styhead release
- `walnascar.yml` - For Walnascar release

## Usage Example

To include the browser feature in your BSP build:

```bash
# Using BSP Registry Manager
just bsp <board-name> <yocto-release> browser

# Example for RSB3720 with Scarthgap
just bsp rsb3720 scarthgap browser
```

## Requirements

- Sufficient system memory (minimum 512MB RAM recommended, 1GB+ preferred)
- GPU with graphics acceleration (recommended)
- Display output (HDMI, LVDS, etc.)
- Wayland or X11 compositor

## Known Limitations

- Chromium requires significant disk space (200MB+ for binaries)
- Initial build time can be extensive (several hours)
- Performance varies based on hardware capabilities
- Some advanced features may require additional configuration

## Related Features

- **Qt**: Can be combined with Qt WebEngine for Qt-based web applications
- **Protocols**: Works with Zenoh for networked web applications

## Additional Resources

- [Chromium Project](https://www.chromium.org/)
- [meta-browser Documentation](https://github.com/OSSystems/meta-browser)
- [Yocto Project Graphics Stack](https://www.yoctoproject.org/)
