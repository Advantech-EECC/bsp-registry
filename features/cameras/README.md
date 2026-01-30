# Cameras Feature

## Overview

The Cameras feature provides support for Intel RealSense depth cameras, enabling advanced computer vision, 3D scanning, and depth sensing capabilities on embedded systems.

## Architecture

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

## Supported Cameras

Intel RealSense camera family:
- RealSense D400 Series (depth cameras)
- RealSense D415, D435, D455
- Other RealSense SDK compatible devices

## Repository

- **Layer**: meta-intel-realsense
- **Source**: https://github.com/robwoolley/meta-intel-realsense.git
- **Maintained by**: Rob Woolley

## Features

- **Depth Sensing**: High-resolution depth maps (up to 1280x720)
- **RGB Imaging**: Color camera with synchronized depth
- **Point Cloud Generation**: 3D point cloud data for spatial mapping
- **IMU Data**: Accelerometer and gyroscope for motion tracking
- **Multiple Streams**: Simultaneous RGB, depth, and IR streams
- **SDK Integration**: Full librealsense2 SDK support

## Use Cases

- **Robotics**: Obstacle detection and navigation
- **3D Scanning**: Object and environment reconstruction
- **Gesture Recognition**: Touchless user interfaces
- **AR/VR**: Spatial tracking and mapping
- **Industrial Automation**: Bin picking and quality inspection
- **People Counting**: Retail analytics and security
- **Volume Measurement**: Logistics and warehouse management

## Data Flow

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

## Configuration Files

- `realsense.yml` - RealSense camera support configuration

## Usage Example

To include RealSense camera support in your BSP build:

```bash
# Using BSP Registry Manager
just bsp <board-name> <yocto-release> cameras/realsense

# Example for RSB3720 with Scarthgap
just bsp rsb3720 scarthgap cameras/realsense
```

## Requirements

- **USB 3.0/3.1**: Required for high-bandwidth data transfer
- **Minimum 2GB RAM**: For processing depth and RGB streams
- **CPU**: Multi-core recommended for real-time processing
- **Kernel**: USB drivers and V4L2 support

## Performance Considerations

- USB 3.0 bandwidth: ~5 Gbps required for full resolution streams
- CPU usage: 20-40% for basic depth processing on quad-core ARM
- Memory footprint: 100-500MB depending on configuration
- Latency: Typically 30-60ms for depth processing

## Integration Examples

### With OpenCV
```python
import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
pipeline.start()
```

### With ROS2
Compatible with `realsense-ros` packages for robotic applications.

### With Python AI
Can be combined with Python AI feature for depth-based machine learning.

## Known Limitations

- Requires USB 3.0 host controller with adequate bandwidth
- Camera performance may be limited on low-power embedded systems
- Some advanced features require specific firmware versions
- Outdoor use may be affected by sunlight interference with IR sensors

## Related Features

- **Deep Learning**: Combine with Hailo for AI-powered vision
- **Python AI**: Use with computer vision libraries
- **ROS2**: Integration with robotic systems
- **Protocols**: Stream data over Zenoh

## Additional Resources

- [Intel RealSense SDK](https://github.com/IntelRealSense/librealsense)
- [RealSense Documentation](https://dev.intelrealsense.com/)
- [meta-intel-realsense Layer](https://github.com/robwoolley/meta-intel-realsense)
