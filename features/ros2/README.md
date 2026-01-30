# ROS2 (Robot Operating System 2) Feature

## Overview

The ROS2 feature integrates the Robot Operating System 2 framework into the BSP, providing a flexible framework for writing robot software with support for distributed systems, real-time capabilities, and a rich ecosystem of tools and libraries.

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Robot Application Layer                 │
│  (Navigation, Perception, Manipulation)         │
├─────────────────────────────────────────────────┤
│         ROS2 Client Libraries                   │
│  ┌───────────────────────────────────────────┐ │
│  │ rclcpp (C++)  │  rclpy (Python)          │ │
│  └───────────────────────────────────────────┘ │
├─────────────────────────────────────────────────┤
│         ROS2 Middleware (DDS)                   │
│  (FastDDS, CycloneDDS, RTI Connext)            │
├─────────────────────────────────────────────────┤
│         Communication Infrastructure            │
│  ┌───────────────────────────────────────────┐ │
│  │ Topics  │ Services  │ Actions  │ Params  │ │
│  └───────────────────────────────────────────┘ │
├─────────────────────────────────────────────────┤
│         Operating System (Linux/Real-time)      │
└─────────────────────────────────────────────────┘
```

## Supported ROS2 Distributions

| Distribution | Release Date | EOL | Ubuntu Base | Key Features |
|--------------|--------------|-----|-------------|--------------|
| **Humble Hawksbill** | May 2022 | May 2027 | 22.04 | LTS, Production-ready |
| **Jazzy Jalisco** | May 2024 | May 2029 | 24.04 | Latest LTS, Modern features |
| **Kilted Kaiju** | Nov 2024 | Nov 2025 | - | Rolling release features |
| **Rolling** | Continuous | - | Latest | Cutting-edge, experimental |

## Repository

- **Layer**: meta-ros
- **Source**: https://github.com/ros/meta-ros.git
- **Includes**: meta-ros-common, meta-ros2, meta-ros2-{distribution}

## ROS2 Communication Patterns

### 1. Topics (Publish/Subscribe)
```
┌──────────┐                    ┌──────────┐
│Publisher │──► /sensor/data ──►│Subscriber│
│ (Sensor) │                    │(Logger)  │
└──────────┘                    └──────────┘
                                     │
                                     ▼
                                ┌──────────┐
                                │Subscriber│
                                │(Display) │
                                └──────────┘
```

### 2. Services (Request/Reply)
```
┌────────┐                      ┌────────┐
│ Client │─────► Request ─────► │Service │
│        │                      │ Server │
│        │◄───── Response ◄─────│        │
└────────┘                      └────────┘
```

### 3. Actions (Long-running Tasks)
```
┌────────┐                      ┌────────┐
│ Action │─────► Goal ─────────►│ Action │
│ Client │                      │ Server │
│        │◄───── Feedback ◄─────│        │
│        │◄───── Result ◄───────│        │
└────────┘                      └────────┘
```

## Features

- **Distributed Architecture**: Multiple nodes across processes/machines
- **Real-time Capable**: RTOS support for time-critical applications
- **QoS Policies**: Quality of Service for reliable communication
- **Component Model**: Composable nodes for efficiency
- **Type Safety**: Strong typing with IDL (Interface Definition Language)
- **Lifecycle Management**: Controlled node startup/shutdown
- **Security**: DDS-Security for encrypted communication
- **Multi-language**: C++, Python, and other language bindings

## Use Cases

- **Mobile Robots**: Autonomous navigation and mapping
- **Industrial Automation**: Robotic arms and manipulators
- **Drones**: Aerial robotics and fleet management
- **Autonomous Vehicles**: Self-driving car systems
- **Agricultural Robots**: Automated farming equipment
- **Service Robots**: Healthcare, hospitality, delivery
- **Research Platforms**: Academic robotics research
- **Multi-robot Systems**: Swarm and collaborative robots

## ROS2 Node Graph Example

```
┌─────────────┐
│ /camera_node│
└──────┬──────┘
       │ publishes
       ▼
  /camera/image ──────┐
                      │
                      ▼
              ┌──────────────┐
              │ /detector_node│
              └───────┬───────┘
                      │ publishes
                      ▼
              /detections ─────┐
                                │
                                ▼
                        ┌──────────────┐
                        │ /control_node │
                        └───────────────┘
```

## Key ROS2 Concepts

### Nodes
Independent processes that perform computation.

### Topics
Named buses for asynchronous data streaming.

### Messages
Data structures for topic communication (sensor_msgs, geometry_msgs, etc.).

### Quality of Service (QoS)
Configure reliability, durability, deadline, liveliness.

### Launch Files
Declarative configuration for starting multiple nodes.

## Configuration Files

- `humble.yml` - ROS2 Humble Hawksbill (LTS)
- `jazzy.yml` - ROS2 Jazzy Jalisco (Latest LTS)
- `kilted.yml` - ROS2 Kilted Kaiju
- `rolling.yml` - ROS2 Rolling (Development)

## Usage Example

To include ROS2 support in your BSP build:

```bash
# Using BSP Registry Manager
just bsp <board-name> <yocto-release> ros2/humble

# Example for RSB3720 with Scarthgap
just bsp rsb3720 scarthgap ros2/humble
```

## Requirements

- **Memory**: 512MB+ RAM (1GB+ recommended)
- **Storage**: 500MB+ for ROS2 core packages
- **Network**: Ethernet for multi-machine communication
- **Python 3**: Python 3.8+ for rclpy
- **C++14/17**: Modern C++ compiler

## ROS2 Workspace Structure

```
ros2_workspace/
├── src/                    # Source code
│   ├── package_1/
│   ├── package_2/
│   └── package_3/
├── build/                  # Build artifacts
├── install/                # Installed packages
└── log/                    # Build logs
```

## Common ROS2 Packages

| Package | Purpose |
|---------|---------|
| **nav2** | Navigation stack (SLAM, path planning) |
| **moveit2** | Motion planning for manipulators |
| **image_pipeline** | Camera image processing |
| **tf2** | Transform library for coordinate frames |
| **robot_state_publisher** | Publish robot joint states |
| **rviz2** | 3D visualization tool |
| **rqt** | Qt-based GUI tools |

## Example Code

### Publisher (C++)
```cpp
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

class MinimalPublisher : public rclcpp::Node {
public:
  MinimalPublisher() : Node("minimal_publisher") {
    publisher_ = create_publisher<std_msgs::msg::String>("topic", 10);
    timer_ = create_wall_timer(
      500ms, std::bind(&MinimalPublisher::timer_callback, this));
  }

private:
  void timer_callback() {
    auto message = std_msgs::msg::String();
    message.data = "Hello, ROS2!";
    publisher_->publish(message);
  }
  
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};
```

### Subscriber (Python)
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String, 'topic', self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

rclpy.init()
node = MinimalSubscriber()
rclpy.spin(node)
```

## Data Flow Example

```
Sensor (Camera)
      │
      ├─► /camera/image_raw (sensor_msgs/Image)
      │
      ▼
  Image Processing Node
      │
      ├─► /camera/image_processed
      │
      ▼
  Object Detection Node
      │
      ├─► /detections (vision_msgs/Detection2DArray)
      │
      ▼
  Robot Controller
      │
      ├─► /cmd_vel (geometry_msgs/Twist)
      │
      ▼
  Motor Driver
```

## Quality of Service Profiles

```
Profile: Sensor Data
├── Reliability: Best Effort
├── Durability: Volatile
├── History: Keep Last 10
└── Liveliness: Automatic

Profile: Services
├── Reliability: Reliable
├── Durability: Volatile
├── History: Keep Last 1
└── Liveliness: Automatic
```

## Performance Considerations

- **Inter-process**: Use composable nodes for efficiency
- **Serialization**: Choose appropriate message sizes
- **QoS tuning**: Match QoS to use case
- **Network**: Use DDS discovery for multi-machine setups
- **Real-time**: Consider PREEMPT_RT kernel for determinism

## ROS2 vs ROS1

| Feature | ROS1 | ROS2 |
|---------|------|------|
| **Architecture** | Master-based | Distributed (DDS) |
| **Real-time** | Limited | Yes |
| **Security** | No | DDS-Security |
| **Multi-robot** | Difficult | Native |
| **Platforms** | Linux | Linux, Windows, macOS |
| **Python** | 2.7 | 3.x |

## Debugging Tools

- **ros2 topic**: List, echo, info about topics
- **ros2 node**: Inspect running nodes
- **ros2 service**: Interact with services
- **ros2 bag**: Record and replay data
- **rqt_graph**: Visualize node graph

## Known Limitations

- Large installation size (500MB+ for core)
- DDS middleware can be complex to configure
- Higher resource usage than ROS1
- Some ROS1 packages not yet ported to ROS2
- Real-time performance requires kernel tuning

## Related Features

- **Cameras**: RealSense with realsense-ros package
- **Deep Learning**: Integrate AI inference in perception
- **Protocols**: Zenoh-DDS bridge for WAN communication
- **Python AI**: Use NumPy/SciPy in ROS2 nodes
- **Qt**: Build robot GUIs with rqt

## Additional Resources

- [ROS2 Documentation](https://docs.ros.org/)
- [ROS2 Tutorials](https://docs.ros.org/en/rolling/Tutorials.html)
- [meta-ros Layer](https://github.com/ros/meta-ros)
- [ROS Discourse](https://discourse.ros.org/)
- [ROS Answers](https://answers.ros.org/)
- [ROS Index](https://index.ros.org/)
