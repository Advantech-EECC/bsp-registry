# Protocols Feature

## Overview

The Protocols feature integrates Zenoh, a high-performance, zero-overhead pub/sub and query-reply protocol designed for IoT, robotics, and distributed systems.

## Architecture

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

## Key Concepts

### Pub/Sub Model
```
Publisher ─────► [Key/Value] ─────► Subscriber(s)
  (Sensor)      (topic: /temp)      (Dashboard, Logger)
```

### Query/Reply Model
```
Querier ─────► [Query: /device/*] ─────► Queryable
(Client)                                  (Service)
         ◄──── [Reply: Data] ──────
```

### Shared Memory Optimization
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

## Repository

- **Layer**: meta-zenoh
- **Source**: https://github.com/Jarsop/meta-zenoh.git
- **Language**: Rust (with C, Python, Java bindings)

## Features

- **Zero-Copy**: Shared memory transport for local communication
- **Protocol Agnostic**: Works over TCP, UDP, WebSocket, Serial
- **Auto-Discovery**: Peer discovery without configuration
- **QoS Support**: Reliable and best-effort delivery
- **Routing**: Multi-hop message routing
- **Low Latency**: Sub-millisecond latency for local communication
- **Scalability**: Thousands of endpoints per network
- **Extensible**: Plugin architecture for custom protocols

## Use Cases

- **Robotics**: ROS2 bridge for robot communication
- **IoT Gateways**: Edge-to-cloud data pipelines
- **Distributed Sensing**: Multi-sensor data aggregation
- **Industrial Automation**: Real-time control systems
- **Vehicle-to-Everything (V2X)**: Automotive communication
- **Edge Computing**: Distributed data processing
- **Telemetry**: High-frequency sensor data collection

## Communication Patterns

### 1. Publish/Subscribe
```rust
// Publisher
let session = zenoh::open(config).await.unwrap();
session.put("/demo/example", "Hello Zenoh!").await.unwrap();

// Subscriber
let subscriber = session.subscribe("/demo/**").await.unwrap();
```

### 2. Query/Reply
```rust
// Queryable (Server)
let queryable = session
    .queryable("/demo/service")
    .await.unwrap();

// Querier (Client)
let replies = session.get("/demo/service").await.unwrap();
```

### 3. Storage
Zenoh can store last values for topics, enabling late-joining subscribers.

## Performance Characteristics

| Metric | Value |
|--------|-------|
| **Latency** (local) | < 10 μs |
| **Throughput** (shared mem) | > 10 GB/s |
| **CPU Overhead** | Minimal (zero-copy) |
| **Memory Footprint** | ~2-5 MB |
| **Discovery Time** | < 100 ms |

## Network Topology

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

## Configuration Files

- `zenoh.yml` - Zenoh protocol support with shared memory enabled

## Configuration Options

The configuration enables:
- **Shared Memory**: `ZENOH_SHARED_MEMORY = "true"` for zero-copy
- **Unstable API**: `ZENOH_UNSTABLE_API = "true"` for experimental features
- **Build Fixes**: Compatibility patches for specific Yocto releases

## Usage Example

To include Zenoh protocol support in your BSP build:

```bash
# Using BSP Registry Manager
just bsp <board-name> <yocto-release> protocols/zenoh

# Example for RSB3720 with Scarthgap
just bsp rsb3720 scarthgap protocols/zenoh
```

## Requirements

- **Memory**: 4MB+ for runtime
- **Network**: Ethernet/WiFi for distributed deployment
- **Rust Support**: Yocto Rust toolchain

## Integration Examples

### With ROS2
Zenoh provides a DDS bridge for ROS2 integration:
```
ROS2 Node ◄──► Zenoh-DDS Bridge ◄──► Zenoh Network
```

### With Python
```python
import zenoh

session = zenoh.open()
session.put("/demo/hello", "Hello from Python!")
```

### With C
```c
z_owned_session_t session;
z_open(&session, z_config_default());
z_put(session, "/demo/hello", "Hello from C");
```

## Comparison with Other Protocols

| Feature | Zenoh | MQTT | DDS | gRPC |
|---------|-------|------|-----|------|
| **Latency** | Very Low | Medium | Low | Medium |
| **Overhead** | Minimal | Low | High | Medium |
| **Discovery** | Auto | Manual | Auto | Manual |
| **QoS** | ✅ | ✅ | ✅ | ❌ |
| **Zero-Copy** | ✅ | ❌ | ⚠️ | ❌ |
| **Routing** | ✅ | ✅ | ❌ | ❌ |

## Advanced Features

### Time-Series Data
Zenoh supports time-stamped data for synchronized multi-sensor systems.

### Geo-Distribution
Built-in routing allows spanning multiple sites and networks.

### Liveliness Tokens
Detect presence/absence of nodes in the network.

### Access Control
Fine-grained permissions for topics and queries.

## Known Limitations

- Rust dependency increases build time
- Unstable API may change between versions
- Limited GUI tools compared to mature protocols like MQTT
- Documentation primarily in English

## Related Features

- **ROS2**: Can bridge ROS2 DDS to Zenoh
- **Cameras**: Stream sensor data from RealSense
- **Deep Learning**: Distribute inference results
- **OTA**: Signal update availability across fleet
- **Python AI**: Python bindings for ML pipelines

## Additional Resources

- [Zenoh Website](https://zenoh.io/)
- [Zenoh GitHub](https://github.com/eclipse-zenoh/zenoh)
- [Zenoh Documentation](https://zenoh.io/docs/)
- [meta-zenoh Layer](https://github.com/Jarsop/meta-zenoh)
- [Zenoh Examples](https://github.com/eclipse-zenoh/zenoh/tree/master/examples)
