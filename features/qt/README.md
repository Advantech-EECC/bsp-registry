# Qt Feature

## Overview

The Qt feature integrates the Qt application framework into the BSP, enabling development of modern, cross-platform graphical user interfaces and applications with hardware acceleration support.

## Architecture

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

## Supported Qt Versions

The Qt feature supports multiple Qt 6 versions:

| Version | Status | Key Features |
|---------|--------|--------------|
| **Qt 6.3** | Stable | LTS baseline, mature APIs |
| **Qt 6.5** | LTS | Long-term support, enhanced performance |
| **Qt 6.7** | Stable | Latest features, improved QML |
| **Qt 6.8** | Latest | Cutting-edge, new Qt Quick controls |
| **Qt 6.8.1** | Latest | Bug fixes and stability |
| **Qt 6.8.3** | Latest | Most recent patch release |

## Repository

- **Layer**: meta-qt6
- **Source**: https://code.qt.io/yocto/meta-qt6.git
- **Maintained by**: Qt Company

## Qt Modules Overview

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

## Features

- **Declarative UI**: QML for rapid UI development
- **Hardware Acceleration**: OpenGL ES, Vulkan support
- **Touch Support**: Multi-touch gesture recognition
- **Multimedia**: Audio/video playback and capture
- **Networking**: HTTP, WebSockets, SSL/TLS
- **Cross-Platform**: Write once, run on multiple platforms
- **Performance**: Optimized for embedded systems
- **Internationalization**: Multi-language support

## Use Cases

- **Industrial HMI**: Human-machine interfaces for factories
- **Medical Devices**: Touch-based medical equipment UIs
- **Automotive Dashboards**: In-vehicle infotainment (IVI)
- **Smart Home Panels**: Control panels for home automation
- **Kiosks**: Interactive information displays
- **POS Systems**: Point-of-sale terminals
- **Instrumentation**: Data visualization and control

## UI Development Workflow

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

## QML Example

### Simple Qt Quick Application
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

## Platform Backends

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

## Configuration Files

- `qt6.3.yml` - Qt 6.3.x release
- `qt6.5.yml` - Qt 6.5.x LTS release
- `qt6.7.yml` - Qt 6.7.x release
- `qt6.8.yml` - Qt 6.8.x release
- `qt6.8.1.yml` - Qt 6.8.1 release
- `qt6.8.3.yml` - Qt 6.8.3 release

## Usage Example

To include Qt support in your BSP build:

```bash
# Using BSP Registry Manager
just bsp <board-name> <yocto-release> qt/qt6.8

# Example for RSB3720 with Scarthgap
just bsp rsb3720 scarthgap qt/qt6.8
```

## Requirements

### Minimum Hardware Requirements
- **Memory**: 256MB RAM (512MB+ recommended for Qt Quick)
- **Storage**: 150MB+ for Qt libraries
- **Display**: Framebuffer or GPU with OpenGL ES 2.0+
- **Input**: Touch screen or keyboard/mouse

### Software Requirements
- **Compiler**: C++17 support (GCC 8+)
- **Graphics**: EGL, OpenGL ES, or Vulkan
- **Fonts**: TrueType font support

## Performance Optimization

### Rendering Pipeline
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

### Tips
- Use `Image` for static content, `Canvas` for dynamic
- Enable QML caching for faster startup
- Use hardware layers for complex animations
- Profile with Qt Creator's performance analyzer

## Memory Footprint

| Component | Size (Approx) |
|-----------|--------------|
| Qt Core | 5 MB |
| Qt GUI | 8 MB |
| Qt Quick | 12 MB |
| Qt Multimedia | 6 MB |
| Qt WebEngine | 40+ MB |
| **Total (minimal)** | **25-30 MB** |
| **Full featured** | **100+ MB** |

## Application Types

### 1. Qt Widgets Application
Traditional desktop-style UI with buttons, menus, dialogs.

### 2. Qt Quick Application
Modern, touch-optimized UI with animations and effects.

### 3. Hybrid Application
Combines Qt Widgets for tools and Qt Quick for main interface.

## Integration Examples

### With Camera
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

### With Networking
```cpp
QNetworkAccessManager manager;
QNetworkRequest request(QUrl("http://api.example.com/data"));
manager.get(request);
```

### With Database
```cpp
QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
db.setDatabaseName("app.db");
db.open();
```

## Development Tools

- **Qt Creator**: Cross-platform IDE
- **Qt Design Studio**: Visual design tool
- **qmake**: Qt build system
- **CMake**: Alternative build system
- **Qt Linguist**: Translation tool

## Known Limitations

- Qt 6 requires newer compilers (C++17)
- WebEngine requires significant resources
- Some modules may not be available on all architectures
- Startup time can be slower on low-end hardware
- Build time is extensive (several hours for full Qt)

## Migration from Qt 5

Qt 6 changes:
- QML engine improvements (better performance)
- Removed Qt Quick Controls 1 (use Controls 2)
- CMake is preferred over qmake
- Some modules reorganized or deprecated

## Related Features

- **Browser**: Qt WebEngine for embedded web content
- **Cameras**: Display camera feeds with Qt Multimedia
- **Protocols**: Network communication with Qt Network
- **Python AI**: PyQt bindings for Python-based UIs

## Additional Resources

- [Qt Documentation](https://doc.qt.io/)
- [Qt for Embedded](https://doc.qt.io/qt-6/embedded-linux.html)
- [Qt Examples](https://doc.qt.io/qt-6/qtexamples.html)
- [meta-qt6 Layer](https://code.qt.io/yocto/meta-qt6)
- [Qt Design Studio](https://www.qt.io/product/ui-design-tools)
