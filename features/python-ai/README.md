# Python AI Feature

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture](#2-architecture)
- [3. Repository](#3-repository)
- [4. Features](#4-features)
- [5. Scientific Computing Stack](#5-scientific-computing-stack)
- [6. Use Cases](#6-use-cases)
- [7. Numerical Computing Pipeline](#7-numerical-computing-pipeline)
- [8. Supported Libraries](#8-supported-libraries)
  - [8.1. Core Scientific Libraries](#81-core-scientific-libraries)
  - [8.2. Mathematical Libraries](#82-mathematical-libraries)
  - [8.3. Machine Learning (Can be added)](#83-machine-learning-can-be-added)
- [9. Configuration Files](#9-configuration-files)
- [10. Special Configuration](#10-special-configuration)
- [11. Usage Example](#11-usage-example)
- [12. Requirements](#12-requirements)
- [13. Performance Considerations](#13-performance-considerations)
- [14. Code Examples](#14-code-examples)
  - [14.1. NumPy Array Operations](#141-numpy-array-operations)
  - [14.2. SciPy Signal Processing](#142-scipy-signal-processing)
  - [14.3. SciPy Optimization](#143-scipy-optimization)
- [15. ML Workflow Example](#15-ml-workflow-example)
- [16. Integration with Other Tools](#16-integration-with-other-tools)
  - [16.1. Jupyter Notebooks](#161-jupyter-notebooks)
  - [16.2. Data Visualization](#162-data-visualization)
- [17. Memory and CPU Optimization](#17-memory-and-cpu-optimization)
  - [17.1. Use Smaller Data Types](#171-use-smaller-data-types)
  - [17.2. Vectorize Operations](#172-vectorize-operations)
- [18. Known Limitations](#18-known-limitations)
- [19. Related Features](#19-related-features)
- [20. Additional Resources](#20-additional-resources)


## 1. Overview

The Python AI feature integrates advanced Python-based artificial intelligence and machine learning libraries into the BSP, enabling development of AI applications with NumPy, SciPy, and scientific computing tools including Fortran support.

## 2. Architecture

```
┌─────────────────────────────────────────┐
│      AI/ML Application                  │
│  (TensorFlow, PyTorch, Scikit-learn)    │
├─────────────────────────────────────────┤
│      Python AI Libraries                │
│  ┌─────────────────────────────────┐   │
│  │ NumPy   │ SciPy  │ Pandas      │   │
│  ├─────────────────────────────────┤   │
│  │ Fortran Libraries (BLAS/LAPACK) │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│      Python Runtime (CPython)           │
├─────────────────────────────────────────┤
│      Operating System                   │
└─────────────────────────────────────────┘
```

## 3. Repository

- **Layer**: meta-python-ai
- **Source**: https://github.com/zboszor/meta-python-ai
- **Maintained by**: Zoltán Böszörményi

## 4. Features

- **NumPy**: Fundamental package for numerical computing
- **SciPy**: Scientific computing library (optimization, integration, etc.)
- **Fortran Support**: GFortran compiler for scientific libraries
- **BLAS/LAPACK**: Optimized linear algebra routines
- **libquadmath**: Quad-precision floating-point support
- **Performance Libraries**: Optimized mathematical operations

## 5. Scientific Computing Stack

```
┌──────────────────────────────────────────┐
│  High-Level Libraries                    │
│  • Scikit-learn (ML)                     │
│  • Pandas (Data Analysis)                │
│  • Matplotlib (Visualization)            │
├──────────────────────────────────────────┤
│  Core Scientific Libraries               │
│  • NumPy (Arrays, Linear Algebra)        │
│  • SciPy (Scientific Algorithms)         │
├──────────────────────────────────────────┤
│  Low-Level Optimized Libraries           │
│  • BLAS (Basic Linear Algebra)           │
│  • LAPACK (Linear Algebra Package)       │
│  • FFTW (Fast Fourier Transform)         │
├──────────────────────────────────────────┤
│  Compilers & Runtime                     │
│  • GFortran                              │
│  • GCC                                   │
│  • libquadmath                           │
└──────────────────────────────────────────┘
```

## 6. Use Cases

- **Machine Learning**: Train and deploy ML models
- **Data Analysis**: Process and analyze sensor data
- **Signal Processing**: FFT, filtering, spectral analysis
- **Computer Vision**: Image processing and analysis
- **Scientific Computing**: Numerical simulations
- **Statistics**: Statistical analysis and modeling
- **Optimization**: Linear/nonlinear optimization problems
- **Predictive Maintenance**: Anomaly detection

## 7. Numerical Computing Pipeline

```
Raw Data Input
      │
      ▼
┌──────────────┐
│ Data Loading │
│  (Pandas)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Preprocessing│
│  (NumPy)     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Analysis    │
│  (SciPy)     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Results    │
│ Visualization│
└──────────────┘
```

## 8. Supported Libraries

### 8.1. Core Scientific Libraries
- **NumPy**: Multi-dimensional arrays, linear algebra, FFT
- **SciPy**: Optimization, integration, interpolation, signal processing
- **Pandas**: Data structures and analysis tools

### 8.2. Mathematical Libraries
- **BLAS**: Level 1, 2, 3 operations (vector, matrix operations)
- **LAPACK**: Linear system solving, eigenvalue problems
- **libquadmath**: 128-bit floating-point arithmetic

### 8.3. Machine Learning (Can be added)
- **Scikit-learn**: Classical ML algorithms
- **TensorFlow Lite**: Lightweight ML inference
- **ONNX Runtime**: Cross-platform inference

## 9. Configuration Files

- `python-ai.yml` - Python AI libraries configuration

## 10. Special Configuration

The feature includes specific compiler settings:
- **Fortran Support**: Enables Fortran compiler in toolchain
- **libquadmath**: Adds quad-precision math library to runtime
- **GFortran**: Available as host tool for build-time compilation

## 11. Usage Example

To include Python AI support in your BSP build, you need to create a custom YAML configuration file that includes the Python AI feature layer.

Example YAML configuration (`custom-bsp-with-python-ai.yaml`):
```yaml
header:
  version: 14
  includes:
    - adv-bsp-oenxp-scarthgap-rsb3720.yaml
    - features/python-ai/python-ai.yml
```

Then build with KAS:
```bash
kas-container build custom-bsp-with-python-ai.yaml
```

See the main README's "HowTo build a BSP using KAS" section for more details on working with KAS configuration files.

## 12. Requirements

- **Memory**: 512MB+ RAM (1GB+ recommended for ML workloads)
- **Storage**: 200MB+ for libraries and dependencies
- **CPU**: ARM or x86 with floating-point unit
- **Python 3**: Python 3.8+ runtime

## 13. Performance Considerations

| Operation | Library | Performance |
|-----------|---------|-------------|
| Matrix Multiplication | NumPy/BLAS | Optimized for ARM NEON |
| FFT | NumPy/FFTW | Hardware acceleration |
| Linear Solve | LAPACK | Multi-threaded |
| Element-wise ops | NumPy | Vectorized |

## 14. Code Examples

### 14.1. NumPy Array Operations
```python
import numpy as np

# Create array
data = np.array([[1, 2], [3, 4]])

# Matrix operations
result = np.dot(data, data.T)
eigenvalues = np.linalg.eigvals(result)
```

### 14.2. SciPy Signal Processing
```python
from scipy import signal
import numpy as np

# Create a signal
t = np.linspace(0, 1, 500)
sig = np.sin(2*np.pi*5*t) + np.sin(2*np.pi*10*t)

# Apply FFT
fft_result = np.fft.fft(sig)
```

### 14.3. SciPy Optimization
```python
from scipy.optimize import minimize

def objective(x):
    return x[0]**2 + x[1]**2

result = minimize(objective, [1, 1])
```

## 15. ML Workflow Example

```
┌────────────────────────────────────┐
│ 1. Data Collection                 │
│    (Sensors, Files, Network)       │
├────────────────────────────────────┤
│ 2. Data Preprocessing              │
│    (NumPy: normalize, reshape)     │
├────────────────────────────────────┤
│ 3. Feature Engineering             │
│    (SciPy: filtering, transforms)  │
├────────────────────────────────────┤
│ 4. Model Training                  │
│    (Scikit-learn: fit model)       │
├────────────────────────────────────┤
│ 5. Prediction                      │
│    (Scikit-learn: predict)         │
├────────────────────────────────────┤
│ 6. Results Processing              │
│    (NumPy: post-processing)        │
└────────────────────────────────────┘
```

## 16. Integration with Other Tools

### 16.1. Jupyter Notebooks
Can be combined with Jupyter for interactive development:
```bash
pip install jupyter
jupyter notebook
```

### 16.2. Data Visualization
Add matplotlib for plotting:
```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.ylabel('values')
plt.show()
```

## 17. Memory and CPU Optimization

### 17.1. Use Smaller Data Types
```python
# Instead of float64, use float32 for less memory
data = np.array([1.0, 2.0], dtype=np.float32)
```

### 17.2. Vectorize Operations
```python
# Vectorized (fast)
result = np.sqrt(data)

# Loop-based (slow)
result = [np.sqrt(x) for x in data]
```

## 18. Known Limitations

- Fortran compilation increases build time
- Full SciPy stack requires significant storage
- Some advanced features may need additional dependencies
- BLAS/LAPACK performance depends on hardware optimizations

## 19. Related Features

- **Deep Learning**: Complement with Hailo for hardware-accelerated inference
- **Cameras**: Process RealSense depth data with NumPy
- **Protocols**: Stream data via Zenoh for distributed ML
- **ROS2**: Integrate with robot sensor processing

## 20. Additional Resources

- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Documentation](https://docs.scipy.org/)
- [meta-python-ai Layer](https://github.com/zboszor/meta-python-ai)
- [Python Scientific Lecture Notes](https://scipy-lectures.org/)
- [NumPy for Embedded Systems](https://numpy.org/doc/stable/user/c-info.html)
