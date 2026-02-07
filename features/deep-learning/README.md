# Deep Learning Feature

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. Supported Hardware](#3-supported-hardware)
- [4. Repository](#4-repository)
- [5. Components](#5-components)
- [6. Features](#6-features)
- [7. Use Cases](#7-use-cases)
- [8. Inference Pipeline](#8-inference-pipeline)
- [9. Performance Metrics](#9-performance-metrics)
- [10. Configuration Files](#10-configuration-files)
- [11. Usage Example](#11-usage-example)
- [12. Requirements](#12-requirements)
- [13. Model Deployment Workflow](#13-model-deployment-workflow)
- [14. Integration Examples](#14-integration-examples)
  - [14.1. GStreamer Pipeline](#141-gstreamer-pipeline)
  - [14.2. Python API](#142-python-api)
- [15. Known Limitations](#15-known-limitations)
- [16. Related Features](#16-related-features)
- [17. Additional Resources](#17-additional-resources)


## 1. Overview

The Deep Learning feature integrates Hailo AI accelerators, providing hardware-accelerated neural network inference for edge AI applications with low power consumption and high performance.

## 2. Architecture

```
┌─────────────────────────────────────────┐
│      AI Application                     │
│   (Object Detection, Classification)    │
├─────────────────────────────────────────┤
│      Hailo TAPPAS Framework             │
│   (Pipelines + Pre/Post Processing)     │
├─────────────────────────────────────────┤
│      Hailo Runtime (HailoRT)            │
│   (Model Loading + Scheduling)          │
├─────────────────────────────────────────┤
│      Hailo AI Accelerator               │
│   (Neural Network Inference Engine)     │
│   ┌─────────────────────────────────┐   │
│   │  Hailo-8/8L PCIe/M.2 Card       │   │
│   │  26 TOPS @ 2.5W                 │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 3. Supported Hardware

- **Hailo-8**: 26 TOPS AI accelerator
- **Hailo-8L**: Efficient variant for edge deployment
- **Form Factors**: PCIe, M.2, Mini PCIe

## 4. Repository

- **Layer**: meta-hailo
- **Source**: https://github.com/hailo-ai/meta-hailo.git
- **Branch**: kirkstone (compatible with multiple releases)
- **Maintained by**: Hailo

## 5. Components

The meta-hailo layer includes:
- **meta-hailo-libhailort**: Core runtime library
- **meta-hailo-tappas**: TAPPAS framework for video analytics pipelines

## 6. Features

- **High Performance**: Up to 26 TOPS inference performance
- **Low Power**: 2.5W typical power consumption
- **Model Support**: ONNX, TensorFlow, PyTorch model compatibility
- **GStreamer Integration**: Video pipeline processing via TAPPAS
- **Multi-Stream**: Parallel inference on multiple video streams
- **Network Flexibility**: Support for various CNN architectures

## 7. Use Cases

- **Object Detection**: Real-time detection (YOLO, SSD, etc.)
- **Image Classification**: Visual recognition and categorization
- **Semantic Segmentation**: Pixel-level scene understanding
- **Pose Estimation**: Human pose and skeleton tracking
- **Facial Recognition**: Identity verification and tracking
- **License Plate Recognition**: Vehicle monitoring
- **Defect Detection**: Industrial quality control
- **People Counting**: Retail and crowd analytics

## 8. Inference Pipeline

```
Video Input (Camera/File)
      │
      ▼
  Pre-processing
  (Resize, Normalize)
      │
      ▼
  Hailo Inference
  (Neural Network)
      │
      ▼
  Post-processing
  (NMS, Filtering)
      │
      ▼
  Application Logic
  (Alerts, Display, Storage)
```

## 9. Performance Metrics

| Model | Resolution | FPS | Precision |
|-------|-----------|-----|-----------|
| YOLOv5s | 640x640 | 280+ | FP16 |
| YOLOv8n | 640x640 | 300+ | FP16 |
| ResNet-50 | 224x224 | 1100+ | FP16 |
| MobileNetV2 | 224x224 | 2500+ | FP16 |

*Performance on Hailo-8 accelerator

## 10. Configuration Files

- `hailo.yml` - Hailo AI accelerator support configuration

## 11. Usage Example

To include Hailo deep learning support in your BSP build, you need to create a custom YAML configuration file that includes the Hailo feature layer.

Example YAML configuration (`custom-bsp-with-hailo.yaml`):
```yaml
header:
  version: 14
  includes:
    - adv-bsp-oenxp-scarthgap-rsb3720.yaml
    - features/deep-learning/hailo.yml
```

Then build with KAS:
```bash
kas-container build custom-bsp-with-hailo.yaml
```

See the main README's "HowTo build a BSP using KAS" section for more details on working with KAS configuration files.

## 12. Requirements

- **PCIe/M.2 Slot**: For Hailo accelerator card
- **Minimum 2GB RAM**: For video processing and buffering
- **CPU**: ARM or x86 host processor
- **Kernel**: PCIe drivers and DMA support

## 13. Model Deployment Workflow

```
┌─────────────────────────────────────┐
│  1. Train Model                     │
│     (TensorFlow/PyTorch/ONNX)       │
├─────────────────────────────────────┤
│  2. Optimize for Hailo              │
│     (Hailo Dataflow Compiler)       │
├─────────────────────────────────────┤
│  3. Generate HEF File               │
│     (Hailo Executable Format)       │
├─────────────────────────────────────┤
│  4. Deploy to Target                │
│     (Load via HailoRT)              │
├─────────────────────────────────────┤
│  5. Run Inference                   │
│     (Real-time Processing)          │
└─────────────────────────────────────┘
```

## 14. Integration Examples

### 14.1. GStreamer Pipeline
```bash
gst-launch-1.0 filesrc location=video.mp4 ! \
  decodebin ! hailonet hef-path=model.hef ! \
  hailofilter ! videoconvert ! autovideosink
```

### 14.2. Python API
```python
from hailo_platform import HEF, VDevice

hef = HEF("model.hef")
target = VDevice()
network_group = target.configure(hef)
```

## 15. Known Limitations

- Requires Hailo Dataflow Compiler for model optimization
- Some model architectures may need modifications
- HEF model format is proprietary to Hailo
- PCIe bandwidth considerations for high-resolution multi-stream

## 16. Related Features

- **Cameras**: Combine with RealSense for depth-aware AI
- **Python AI**: Use with Python ML frameworks
- **Protocols**: Stream inference results over Zenoh
- **Browser**: Display AI results in web UI

## 17. Additional Resources

- [Hailo Developer Zone](https://hailo.ai/developer-zone/)
- [TAPPAS Documentation](https://github.com/hailo-ai/tappas)
- [Hailo Model Zoo](https://github.com/hailo-ai/hailo_model_zoo)
- [meta-hailo Layer](https://github.com/hailo-ai/meta-hailo)
