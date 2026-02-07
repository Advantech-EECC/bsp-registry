# Qt Feature

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. Supported Qt Versions](#3-supported-qt-versions)
- [4. Repository](#4-repository)
- [5. Qt Modules Overview](#5-qt-modules-overview)
- [6. Features](#6-features)
- [7. Use Cases](#7-use-cases)
- [8. UI Development Workflow](#8-ui-development-workflow)
- [9. QML Example](#9-qml-example)
  - [9.1. Simple Qt Quick Application](#91-simple-qt-quick-application)
- [10. Platform Backends](#10-platform-backends)
- [11. Configuration Files](#11-configuration-files)
- [12. Usage Example](#12-usage-example)
- [13. Requirements](#13-requirements)
  - [13.1. Minimum Hardware Requirements](#131-minimum-hardware-requirements)
  - [13.2. Software Requirements](#132-software-requirements)
- [14. Performance Optimization](#14-performance-optimization)
  - [14.1. Rendering Pipeline](#141-rendering-pipeline)
  - [14.2. Tips](#142-tips)
- [15. Memory Footprint](#15-memory-footprint)
- [16. Application Types](#16-application-types)
  - [16.1. 1. Qt Widgets Application](#161-1-qt-widgets-application)
  - [16.2. 2. Qt Quick Application](#162-2-qt-quick-application)
  - [16.3. 3. Hybrid Application](#163-3-hybrid-application)
- [17. Integration Examples](#17-integration-examples)
  - [17.1. With Camera](#171-with-camera)
  - [17.2. With Networking](#172-with-networking)
  - [17.3. With Database](#173-with-database)
- [18. Development Tools](#18-development-tools)
- [19. Known Limitations](#19-known-limitations)
- [20. Migration from Qt 5](#20-migration-from-qt-5)
- [21. Related Features](#21-related-features)
- [22. Additional Resources](#22-additional-resources)


## 1. Overview

The Qt feature integrates the Qt application framework into the BSP, enabling development of modern, cross-platform graphical user interfaces and applications with hardware acceleration support.

## 2. Architecture

```
┌─────────────────────────────────────────┐
│      Qt Application                     │
│   (QML/C++ UI Logic)                    │
├─────────────────────────────────────────┤
│      Qt Framework                       │
│  ┌─────────────────────────────────┐   │
│  │ Qt Quick  │ Qt Widgets │ Qt Core │   │
│  ├─────────────────────────────────┤   │
│  │ Qt Multimedia │ Qt Network      │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│      Qt Platform Abstraction (QPA)      │
│   (Wayland/X11/EGLFS/LinuxFB)          │
├─────────────────────────────────────────┤
│      Graphics Stack                     │
│   (OpenGL ES/Vulkan + GPU drivers)      │
├─────────────────────────────────────────┤
│      Linux Kernel                       │
└─────────────────────────────────────────┘
```

## 3. Supported Qt Versions

The Qt feature supports multiple Qt 6 versions:

| Version | Status | Key Features |
|---------|--------|--------------|
| **Qt 6.3** | Stable | LTS baseline, mature APIs |
| **Qt 6.5** | LTS | Long-term support, enhanced performance |
| **Qt 6.7** | Stable | Latest features, improved QML |
| **Qt 6.8** | Latest | Cutting-edge, new Qt Quick controls |
| **Qt 6.8.1** | Latest | Bug fixes and stability |
| **Qt 6.8.3** | Latest | Most recent patch release |

## 4. Repository

- **Layer**: meta-qt6
- **Source**: https://code.qt.io/yocto/meta-qt6.git
- **Maintained by**: Qt Company

## 5. Qt Modules Overview

```
┌──────────────────────────────────────────┐
│         Qt Essentials                    │
│  ┌────────────────────────────────────┐ │
│  │ Qt Core  • Fundamental classes    │ │
│  │ Qt GUI   • Graphics & windows     │ │
│  │ Qt Quick • Declarative UI (QML)   │ │
│  │ Qt Widgets • Classical widgets    │ │
│  └────────────────────────────────────┘ │
├──────────────────────────────────────────┤
│         Qt Add-ons                       │
│  ┌────────────────────────────────────┐ │
│  │ Qt Multimedia  • Audio/Video      │ │
│  │ Qt Network     • Networking       │ │
│  │ Qt WebEngine   • Web content      │ │
│  │ Qt Charts      • Data visualization│ │
│  │ Qt 3D          • 3D rendering     │ │
│  │ Qt Sensors     • Sensor access    │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

## 6. Features

- **Declarative UI**: QML for rapid UI development
- **Hardware Acceleration**: OpenGL ES, Vulkan support
- **Touch Support**: Multi-touch gesture recognition
- **Multimedia**: Audio/video playback and capture
- **Networking**: HTTP, WebSockets, SSL/TLS
- **Cross-Platform**: Write once, run on multiple platforms
- **Performance**: Optimized for embedded systems
- **Internationalization**: Multi-language support

## 7. Use Cases

- **Industrial HMI**: Human-machine interfaces for factories
- **Medical Devices**: Touch-based medical equipment UIs
- **Automotive Dashboards**: In-vehicle infotainment (IVI)
- **Smart Home Panels**: Control panels for home automation
- **Kiosks**: Interactive information displays
- **POS Systems**: Point-of-sale terminals
- **Instrumentation**: Data visualization and control

## 8. UI Development Workflow

```
┌────────────────────────────────────┐
│ 1. Design UI                       │
│    (Qt Design Studio / Qt Creator) │
├────────────────────────────────────┤
│ 2. Implement QML                   │
│    (Declarative UI definition)     │
├────────────────────────────────────┤
│ 3. Add C++ Backend                 │
│    (Business logic, data models)   │
├────────────────────────────────────┤
│ 4. Build Application               │
│    (qmake / CMake)                 │
├────────────────────────────────────┤
│ 5. Deploy to Target                │
│    (Cross-compile & install)       │
└────────────────────────────────────┘
```

## 9. QML Example

### 9.1. Simple Qt Quick Application
```qml
import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 800
    height: 480
    title: "Embedded HMI"

    Rectangle {
        anchors.fill: parent
        color: "#2c3e50"

        Column {
            anchors.centerIn: parent
            spacing: 20

            Text {
                text: "Temperature: 25°C"
                color: "white"
                font.pixelSize: 32
            }

            Button {
                text: "Start Process"
                onClicked: console.log("Started")
            }
        }
    }
}
```

## 10. Platform Backends

```
┌────────────────────────────────────────┐
│  Qt Platform Plugin (QPA)              │
├────────────────────────────────────────┤
│  • EGLFS    → Direct framebuffer       │
│  • Wayland  → Compositor-based         │
│  • X11      → X Window System          │
│  • LinuxFB  → Linux framebuffer        │
│  • KMS      → Kernel Mode Setting      │
└────────────────────────────────────────┘
```

## 11. Configuration Files

- `qt6.3.yml` - Qt 6.3.x release
- `qt6.5.yml` - Qt 6.5.x LTS release
- `qt6.7.yml` - Qt 6.7.x release
- `qt6.8.yml` - Qt 6.8.x release
- `qt6.8.1.yml` - Qt 6.8.1 release
- `qt6.8.3.yml` - Qt 6.8.3 release

## 12. Usage Example

To include Qt support in your BSP build, you need to create a custom YAML configuration file that includes the Qt feature layer.

Example YAML configuration (`custom-bsp-with-qt.yaml`):
```yaml
header:
  version: 14
  includes:
    - adv-bsp-oenxp-scarthgap-rsb3720.yaml
    - features/qt/qt6.8.yml
```

Then build with KAS:
```bash
kas-container build custom-bsp-with-qt.yaml
```

See the main README's "HowTo build a BSP using KAS" section for more details on working with KAS configuration files.

## 13. Requirements

### 13.1. Minimum Hardware Requirements
- **Memory**: 256MB RAM (512MB+ recommended for Qt Quick)
- **Storage**: 150MB+ for Qt libraries
- **Display**: Framebuffer or GPU with OpenGL ES 2.0+
- **Input**: Touch screen or keyboard/mouse

### 13.2. Software Requirements
- **Compiler**: C++17 support (GCC 8+)
- **Graphics**: EGL, OpenGL ES, or Vulkan
- **Fonts**: TrueType font support

## 14. Performance Optimization

### 14.1. Rendering Pipeline
```
Application (QML)
      │
      ▼
Qt Quick Scenegraph
      │
      ▼
OpenGL ES Renderer
      │
      ▼
GPU Hardware
```

### 14.2. Tips
- Use `Image` for static content, `Canvas` for dynamic
- Enable QML caching for faster startup
- Use hardware layers for complex animations
- Profile with Qt Creator's performance analyzer

## 15. Memory Footprint

| Component | Size (Approx) |
|-----------|--------------|
| Qt Core | 5 MB |
| Qt GUI | 8 MB |
| Qt Quick | 12 MB |
| Qt Multimedia | 6 MB |
| Qt WebEngine | 40+ MB |
| **Total (minimal)** | **25-30 MB** |
| **Full featured** | **100+ MB** |

## 16. Application Types

### 16.1. 1. Qt Widgets Application
Traditional desktop-style UI with buttons, menus, dialogs.

### 16.2. 2. Qt Quick Application
Modern, touch-optimized UI with animations and effects.

### 16.3. 3. Hybrid Application
Combines Qt Widgets for tools and Qt Quick for main interface.

## 17. Integration Examples

### 17.1. With Camera
```qml
import QtMultimedia

Camera {
    id: camera
    
    VideoOutput {
        source: camera
        anchors.fill: parent
    }
}
```

### 17.2. With Networking
```cpp
QNetworkAccessManager manager;
QNetworkRequest request(QUrl("http://api.example.com/data"));
manager.get(request);
```

### 17.3. With Database
```cpp
QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
db.setDatabaseName("app.db");
db.open();
```

## 18. Development Tools

- **Qt Creator**: Cross-platform IDE
- **Qt Design Studio**: Visual design tool
- **qmake**: Qt build system
- **CMake**: Alternative build system
- **Qt Linguist**: Translation tool

## 19. Known Limitations

- Qt 6 requires newer compilers (C++17)
- WebEngine requires significant resources
- Some modules may not be available on all architectures
- Startup time can be slower on low-end hardware
- Build time is extensive (several hours for full Qt)

## 20. Migration from Qt 5

Qt 6 changes:
- QML engine improvements (better performance)
- Removed Qt Quick Controls 1 (use Controls 2)
- CMake is preferred over qmake
- Some modules reorganized or deprecated

## 21. Related Features

- **Browser**: Qt WebEngine for embedded web content
- **Cameras**: Display camera feeds with Qt Multimedia
- **Protocols**: Network communication with Qt Network
- **Python AI**: PyQt bindings for Python-based UIs

## 22. Additional Resources

- [Qt Documentation](https://doc.qt.io/)
- [Qt for Embedded](https://doc.qt.io/qt-6/embedded-linux.html)
- [Qt Examples](https://doc.qt.io/qt-6/qtexamples.html)
- [meta-qt6 Layer](https://code.qt.io/yocto/meta-qt6)
- [Qt Design Studio](https://www.qt.io/product/ui-design-tools)
