# Protocols Feature

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. Key Concepts](#3-key-concepts)
  - [3.1. Pub/Sub Model](#31-pubsub-model)
  - [3.2. Query/Reply Model](#32-queryreply-model)
  - [3.3. Shared Memory Optimization](#33-shared-memory-optimization)
- [4. Repository](#4-repository)
- [5. Features](#5-features)
- [6. Use Cases](#6-use-cases)
- [7. Communication Patterns](#7-communication-patterns)
  - [7.1. 1. Publish/Subscribe](#71-1-publishsubscribe)
  - [7.2. 2. Query/Reply](#72-2-queryreply)
  - [7.3. 3. Storage](#73-3-storage)
- [8. Performance Characteristics](#8-performance-characteristics)
- [9. Network Topology](#9-network-topology)
- [10. Configuration Files](#10-configuration-files)
- [11. Configuration Options](#11-configuration-options)
- [12. Usage Example](#12-usage-example)
- [13. Requirements](#13-requirements)
- [14. Integration Examples](#14-integration-examples)
  - [14.1. With ROS2](#141-with-ros2)
  - [14.2. With Python](#142-with-python)
  - [14.3. With C](#143-with-c)
- [15. Comparison with Other Protocols](#15-comparison-with-other-protocols)
- [16. Advanced Features](#16-advanced-features)
  - [16.1. Time-Series Data](#161-time-series-data)
  - [16.2. Geo-Distribution](#162-geo-distribution)
  - [16.3. Liveliness Tokens](#163-liveliness-tokens)
  - [16.4. Access Control](#164-access-control)
- [17. Known Limitations](#17-known-limitations)
- [18. Related Features](#18-related-features)
- [19. Additional Resources](#19-additional-resources)


## 1. Overview

The Protocols feature integrates Zenoh, a high-performance, zero-overhead pub/sub and query-reply protocol designed for IoT, robotics, and distributed systems.

## 2. Architecture

```
┌──────────────────────────────────────────────────────┐
│              Distributed Applications                │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐    ┌─────────────┐  ┌───────────┐ │
│  │ Publisher   │    │ Subscriber  │  │ Queryable │ │
│  └──────┬──────┘    └──────┬──────┘  └─────┬─────┘ │
│         │                   │                │       │
│         └───────────────────┼────────────────┘       │
│                             ▼                        │
├──────────────────────────────────────────────────────┤
│              Zenoh Protocol Layer                    │
│  ┌────────────────────────────────────────────────┐ │
│  │  Routing • Discovery • QoS • Fragmentation     │ │
│  └────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────┤
│           Transport Layer (TCP/UDP/Shared Mem)       │
└──────────────────────────────────────────────────────┘
```

## 3. Key Concepts

### 3.1. Pub/Sub Model
```
Publisher ─────► [Key/Value] ─────► Subscriber(s)
  (Sensor)      (topic: /temp)      (Dashboard, Logger)
```

### 3.2. Query/Reply Model
```
Querier ─────► [Query: /device/*] ─────► Queryable
(Client)                                  (Service)
         ◄──── [Reply: Data] ──────
```

### 3.3. Shared Memory Optimization
```
┌───────────────────────────────────┐
│  Process A    Shared Memory       │
│  ┌─────┐      ┌─────────────┐    │
│  │ Pub │─────►│ Zero-copy   │    │
│  └─────┘      │ Buffer      │    │
│               └──────┬──────┘    │
│  ┌─────┐            │            │
│  │ Sub │◄───────────┘            │
│  └─────┘                         │
│  Process B                       │
└───────────────────────────────────┘
```

## 4. Repository

- **Layer**: meta-zenoh
- **Source**: https://github.com/Jarsop/meta-zenoh.git
- **Language**: Rust (with C, Python, Java bindings)

## 5. Features

- **Zero-Copy**: Shared memory transport for local communication
- **Protocol Agnostic**: Works over TCP, UDP, WebSocket, Serial
- **Auto-Discovery**: Peer discovery without configuration
- **QoS Support**: Reliable and best-effort delivery
- **Routing**: Multi-hop message routing
- **Low Latency**: Sub-millisecond latency for local communication
- **Scalability**: Thousands of endpoints per network
- **Extensible**: Plugin architecture for custom protocols

## 6. Use Cases

- **Robotics**: ROS2 bridge for robot communication
- **IoT Gateways**: Edge-to-cloud data pipelines
- **Distributed Sensing**: Multi-sensor data aggregation
- **Industrial Automation**: Real-time control systems
- **Vehicle-to-Everything (V2X)**: Automotive communication
- **Edge Computing**: Distributed data processing
- **Telemetry**: High-frequency sensor data collection

## 7. Communication Patterns

### 7.1. 1. Publish/Subscribe
```rust
// Publisher
let session = zenoh::open(config).await.unwrap();
session.put("/demo/example", "Hello Zenoh!").await.unwrap();

// Subscriber
let subscriber = session.subscribe("/demo/**").await.unwrap();
```

### 7.2. 2. Query/Reply
```rust
// Queryable (Server)
let queryable = session
    .queryable("/demo/service")
    .await.unwrap();

// Querier (Client)
let replies = session.get("/demo/service").await.unwrap();
```

### 7.3. 3. Storage
Zenoh can store last values for topics, enabling late-joining subscribers.

## 8. Performance Characteristics

| Metric | Value |
|--------|-------|
| **Latency** (local) | < 10 μs |
| **Throughput** (shared mem) | > 10 GB/s |
| **CPU Overhead** | Minimal (zero-copy) |
| **Memory Footprint** | ~2-5 MB |
| **Discovery Time** | < 100 ms |

## 9. Network Topology

```
                    Internet/WAN
                         │
                    ┌────┴────┐
                    │ Router  │
                    │  Zenoh  │
                    └────┬────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────┴────┐      ┌────┴────┐     ┌────┴────┐
   │ Client  │      │ Client  │     │ Peer    │
   │  Edge   │      │  Edge   │     │  Cloud  │
   └─────────┘      └─────────┘     └─────────┘
```

## 10. Configuration Files

- `zenoh.yml` - Zenoh protocol support with shared memory enabled

## 11. Configuration Options

The configuration enables:
- **Shared Memory**: `ZENOH_SHARED_MEMORY = "true"` for zero-copy
- **Unstable API**: `ZENOH_UNSTABLE_API = "true"` for experimental features
- **Build Fixes**: Compatibility patches for specific Yocto releases

## 12. Usage Example

To include Zenoh protocol support in your BSP build, you need to create a custom YAML configuration file that includes the Zenoh feature layer.

Example YAML configuration (`custom-bsp-with-zenoh.yaml`):
```yaml
header:
  version: 14
  includes:
    - adv-bsp-oenxp-scarthgap-rsb3720.yaml
    - features/protocols/zenoh.yml
```

Then build with KAS:
```bash
kas-container build custom-bsp-with-zenoh.yaml
```

See the main README's "HowTo build a BSP using KAS" section for more details on working with KAS configuration files.

## 13. Requirements

- **Memory**: 4MB+ for runtime
- **Network**: Ethernet/WiFi for distributed deployment
- **Rust Support**: Yocto Rust toolchain

## 14. Integration Examples

### 14.1. With ROS2
Zenoh provides a DDS bridge for ROS2 integration:
```
ROS2 Node ◄──► Zenoh-DDS Bridge ◄──► Zenoh Network
```

### 14.2. With Python
```python
import zenoh

session = zenoh.open()
session.put("/demo/hello", "Hello from Python!")
```

### 14.3. With C
```c
z_owned_session_t session;
z_open(&session, z_config_default());
z_put(session, "/demo/hello", "Hello from C");
```

## 15. Comparison with Other Protocols

| Feature | Zenoh | MQTT | DDS | gRPC |
|---------|-------|------|-----|------|
| **Latency** | Very Low | Medium | Low | Medium |
| **Overhead** | Minimal | Low | High | Medium |
| **Discovery** | Auto | Manual | Auto | Manual |
| **QoS** | ✅ | ✅ | ✅ | ❌ |
| **Zero-Copy** | ✅ | ❌ | ⚠️ | ❌ |
| **Routing** | ✅ | ✅ | ❌ | ❌ |

## 16. Advanced Features

### 16.1. Time-Series Data
Zenoh supports time-stamped data for synchronized multi-sensor systems.

### 16.2. Geo-Distribution
Built-in routing allows spanning multiple sites and networks.

### 16.3. Liveliness Tokens
Detect presence/absence of nodes in the network.

### 16.4. Access Control
Fine-grained permissions for topics and queries.

## 17. Known Limitations

- Rust dependency increases build time
- Unstable API may change between versions
- Limited GUI tools compared to mature protocols like MQTT
- Documentation primarily in English

## 18. Related Features

- **ROS2**: Can bridge ROS2 DDS to Zenoh
- **Cameras**: Stream sensor data from RealSense
- **Deep Learning**: Distribute inference results
- **OTA**: Signal update availability across fleet
- **Python AI**: Python bindings for ML pipelines

## 19. Additional Resources

- [Zenoh Website](https://zenoh.io/)
- [Zenoh GitHub](https://github.com/eclipse-zenoh/zenoh)
- [Zenoh Documentation](https://zenoh.io/docs/)
- [meta-zenoh Layer](https://github.com/Jarsop/meta-zenoh)
- [Zenoh Examples](https://github.com/eclipse-zenoh/zenoh/tree/master/examples)
