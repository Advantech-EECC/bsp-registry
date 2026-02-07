# Cameras Feature

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. Supported Cameras](#3-supported-cameras)
- [4. Repository](#4-repository)
- [5. Features](#5-features)
- [6. Use Cases](#6-use-cases)
- [7. Data Flow](#7-data-flow)
- [8. Configuration Files](#8-configuration-files)
- [9. Usage Example](#9-usage-example)
- [10. Requirements](#10-requirements)
- [11. Performance Considerations](#11-performance-considerations)
- [12. Integration Examples](#12-integration-examples)
  - [12.1. With OpenCV](#121-with-opencv)
  - [12.2. With ROS2](#122-with-ros2)
  - [12.3. With Python AI](#123-with-python-ai)
- [13. Known Limitations](#13-known-limitations)
- [14. Related Features](#14-related-features)
- [15. Additional Resources](#15-additional-resources)


## 1. Overview

The Cameras feature provides support for Intel RealSense depth cameras, enabling advanced computer vision, 3D scanning, and depth sensing capabilities on embedded systems.

## 2. Architecture

```
┌─────────────────────────────────────────┐
│      Vision Application                 │
│   (OpenCV, PCL, Custom Code)            │
├─────────────────────────────────────────┤
│      RealSense SDK (librealsense)       │
│   (Camera Control + Data Processing)    │
├─────────────────────────────────────────┤
│      USB 3.0/3.1 Stack                  │
│   (High-bandwidth camera interface)     │
├─────────────────────────────────────────┤
│      RealSense Camera Hardware          │
│   (RGB + Depth Sensors + IMU)           │
└─────────────────────────────────────────┘
```

## 3. Supported Cameras

Intel RealSense camera family:
- RealSense D400 Series (depth cameras)
- RealSense D415, D435, D455
- Other RealSense SDK compatible devices

## 4. Repository

- **Layer**: meta-intel-realsense
- **Source**: https://github.com/robwoolley/meta-intel-realsense.git
- **Maintained by**: Rob Woolley

## 5. Features

- **Depth Sensing**: High-resolution depth maps (up to 1280x720)
- **RGB Imaging**: Color camera with synchronized depth
- **Point Cloud Generation**: 3D point cloud data for spatial mapping
- **IMU Data**: Accelerometer and gyroscope for motion tracking
- **Multiple Streams**: Simultaneous RGB, depth, and IR streams
- **SDK Integration**: Full librealsense2 SDK support

## 6. Use Cases

- **Robotics**: Obstacle detection and navigation
- **3D Scanning**: Object and environment reconstruction
- **Gesture Recognition**: Touchless user interfaces
- **AR/VR**: Spatial tracking and mapping
- **Industrial Automation**: Bin picking and quality inspection
- **People Counting**: Retail analytics and security
- **Volume Measurement**: Logistics and warehouse management

## 7. Data Flow

```
RealSense Camera
      │
      ├─► RGB Stream (1920x1080 @ 30fps)
      │
      ├─► Depth Stream (1280x720 @ 30fps)
      │
      ├─► Infrared Streams (stereo)
      │
      └─► IMU Data (200Hz)
            │
            ▼
      librealsense SDK
            │
            ▼
      Application
```

## 8. Configuration Files

- `realsense.yml` - RealSense camera support configuration

## 9. Usage Example

To include RealSense camera support in your BSP build, you need to create a custom YAML configuration file that includes the camera feature layer.

Example YAML configuration (`custom-bsp-with-realsense.yaml`):
```yaml
header:
  version: 14
  includes:
    - adv-bsp-oenxp-scarthgap-rsb3720.yaml
    - features/cameras/realsense.yml
```

Then build with KAS:
```bash
kas-container build custom-bsp-with-realsense.yaml
```

See the main README's "HowTo build a BSP using KAS" section for more details on working with KAS configuration files.

## 10. Requirements

- **USB 3.0/3.1**: Required for high-bandwidth data transfer
- **Minimum 2GB RAM**: For processing depth and RGB streams
- **CPU**: Multi-core recommended for real-time processing
- **Kernel**: USB drivers and V4L2 support

## 11. Performance Considerations

- USB 3.0 bandwidth: ~5 Gbps required for full resolution streams
- CPU usage: 20-40% for basic depth processing on quad-core ARM
- Memory footprint: 100-500MB depending on configuration
- Latency: Typically 30-60ms for depth processing

## 12. Integration Examples

### 12.1. With OpenCV
```python
import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
pipeline.start()
```

### 12.2. With ROS2
Compatible with `realsense-ros` packages for robotic applications.

### 12.3. With Python AI
Can be combined with Python AI feature for depth-based machine learning.

## 13. Known Limitations

- Requires USB 3.0 host controller with adequate bandwidth
- Camera performance may be limited on low-power embedded systems
- Some advanced features require specific firmware versions
- Outdoor use may be affected by sunlight interference with IR sensors

## 14. Related Features

- **Deep Learning**: Combine with Hailo for AI-powered vision
- **Python AI**: Use with computer vision libraries
- **ROS2**: Integration with robotic systems
- **Protocols**: Stream data over Zenoh

## 15. Additional Resources

- [Intel RealSense SDK](https://github.com/IntelRealSense/librealsense)
- [RealSense Documentation](https://dev.intelrealsense.com/)
- [meta-intel-realsense Layer](https://github.com/robwoolley/meta-intel-realsense)
