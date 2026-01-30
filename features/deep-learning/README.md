# Deep Learning Feature

## Overview

The Deep Learning feature integrates Hailo AI accelerators, providing hardware-accelerated neural network inference for edge AI applications with low power consumption and high performance.

## Architecture

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

## Supported Hardware

- **Hailo-8**: 26 TOPS AI accelerator
- **Hailo-8L**: Efficient variant for edge deployment
- **Form Factors**: PCIe, M.2, Mini PCIe

## Repository

- **Layer**: meta-hailo
- **Source**: https://github.com/hailo-ai/meta-hailo.git
- **Branch**: kirkstone (compatible with multiple releases)
- **Maintained by**: Hailo

## Components

The meta-hailo layer includes:
- **meta-hailo-libhailort**: Core runtime library
- **meta-hailo-tappas**: TAPPAS framework for video analytics pipelines

## Features

- **High Performance**: Up to 26 TOPS inference performance
- **Low Power**: 2.5W typical power consumption
- **Model Support**: ONNX, TensorFlow, PyTorch model compatibility
- **GStreamer Integration**: Video pipeline processing via TAPPAS
- **Multi-Stream**: Parallel inference on multiple video streams
- **Network Flexibility**: Support for various CNN architectures

## Use Cases

- **Object Detection**: Real-time detection (YOLO, SSD, etc.)
- **Image Classification**: Visual recognition and categorization
- **Semantic Segmentation**: Pixel-level scene understanding
- **Pose Estimation**: Human pose and skeleton tracking
- **Facial Recognition**: Identity verification and tracking
- **License Plate Recognition**: Vehicle monitoring
- **Defect Detection**: Industrial quality control
- **People Counting**: Retail and crowd analytics

## Inference Pipeline

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

## Performance Metrics

| Model | Resolution | FPS | Precision |
|-------|-----------|-----|-----------|
| YOLOv5s | 640x640 | 280+ | FP16 |
| YOLOv8n | 640x640 | 300+ | FP16 |
| ResNet-50 | 224x224 | 1100+ | FP16 |
| MobileNetV2 | 224x224 | 2500+ | FP16 |

*Performance on Hailo-8 accelerator

## Configuration Files

- `hailo.yml` - Hailo AI accelerator support configuration

## Usage Example

To include Hailo deep learning support in your BSP build:

```bash
# Using BSP Registry Manager
just bsp <board-name> <yocto-release> deep-learning/hailo

# Example for RSB3720 with Scarthgap
just bsp rsb3720 scarthgap deep-learning/hailo
```

## Requirements

- **PCIe/M.2 Slot**: For Hailo accelerator card
- **Minimum 2GB RAM**: For video processing and buffering
- **CPU**: ARM or x86 host processor
- **Kernel**: PCIe drivers and DMA support

## Model Deployment Workflow

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

## Integration Examples

### GStreamer Pipeline
```bash
gst-launch-1.0 filesrc location=video.mp4 ! \
  decodebin ! hailonet hef-path=model.hef ! \
  hailofilter ! videoconvert ! autovideosink
```

### Python API
```python
from hailo_platform import HEF, VDevice

hef = HEF("model.hef")
target = VDevice()
network_group = target.configure(hef)
```

## Known Limitations

- Requires Hailo Dataflow Compiler for model optimization
- Some model architectures may need modifications
- HEF model format is proprietary to Hailo
- PCIe bandwidth considerations for high-resolution multi-stream

## Related Features

- **Cameras**: Combine with RealSense for depth-aware AI
- **Python AI**: Use with Python ML frameworks
- **Protocols**: Stream inference results over Zenoh
- **Browser**: Display AI results in web UI

## Additional Resources

- [Hailo Developer Zone](https://hailo.ai/developer-zone/)
- [TAPPAS Documentation](https://github.com/hailo-ai/tappas)
- [Hailo Model Zoo](https://github.com/hailo-ai/hailo_model_zoo)
- [meta-hailo Layer](https://github.com/hailo-ai/meta-hailo)
