# Python AI Feature

## Overview

The Python AI feature integrates advanced Python-based artificial intelligence and machine learning libraries into the BSP, enabling development of AI applications with NumPy, SciPy, and scientific computing tools including Fortran support.

## Architecture

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

## Repository

- **Layer**: meta-python-ai
- **Source**: https://github.com/zboszor/meta-python-ai
- **Maintained by**: Zoltán Böszörményi

## Features

- **NumPy**: Fundamental package for numerical computing
- **SciPy**: Scientific computing library (optimization, integration, etc.)
- **Fortran Support**: GFortran compiler for scientific libraries
- **BLAS/LAPACK**: Optimized linear algebra routines
- **libquadmath**: Quad-precision floating-point support
- **Performance Libraries**: Optimized mathematical operations

## Scientific Computing Stack

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

## Use Cases

- **Machine Learning**: Train and deploy ML models
- **Data Analysis**: Process and analyze sensor data
- **Signal Processing**: FFT, filtering, spectral analysis
- **Computer Vision**: Image processing and analysis
- **Scientific Computing**: Numerical simulations
- **Statistics**: Statistical analysis and modeling
- **Optimization**: Linear/nonlinear optimization problems
- **Predictive Maintenance**: Anomaly detection

## Numerical Computing Pipeline

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

## Supported Libraries

### Core Scientific Libraries
- **NumPy**: Multi-dimensional arrays, linear algebra, FFT
- **SciPy**: Optimization, integration, interpolation, signal processing
- **Pandas**: Data structures and analysis tools

### Mathematical Libraries
- **BLAS**: Level 1, 2, 3 operations (vector, matrix operations)
- **LAPACK**: Linear system solving, eigenvalue problems
- **libquadmath**: 128-bit floating-point arithmetic

### Machine Learning (Can be added)
- **Scikit-learn**: Classical ML algorithms
- **TensorFlow Lite**: Lightweight ML inference
- **ONNX Runtime**: Cross-platform inference

## Configuration Files

- `python-ai.yml` - Python AI libraries configuration

## Special Configuration

The feature includes specific compiler settings:
- **Fortran Support**: Enables Fortran compiler in toolchain
- **libquadmath**: Adds quad-precision math library to runtime
- **GFortran**: Available as host tool for build-time compilation

## Usage Example

To include Python AI support in your BSP build:

```bash
# Using BSP Registry Manager
just bsp <board-name> <yocto-release> python-ai

# Example for RSB3720 with Scarthgap
just bsp rsb3720 scarthgap python-ai
```

## Requirements

- **Memory**: 512MB+ RAM (1GB+ recommended for ML workloads)
- **Storage**: 200MB+ for libraries and dependencies
- **CPU**: ARM or x86 with floating-point unit
- **Python 3**: Python 3.8+ runtime

## Performance Considerations

| Operation | Library | Performance |
|-----------|---------|-------------|
| Matrix Multiplication | NumPy/BLAS | Optimized for ARM NEON |
| FFT | NumPy/FFTW | Hardware acceleration |
| Linear Solve | LAPACK | Multi-threaded |
| Element-wise ops | NumPy | Vectorized |

## Code Examples

### NumPy Array Operations
```python
import numpy as np

# Create array
data = np.array([[1, 2], [3, 4]])

# Matrix operations
result = np.dot(data, data.T)
eigenvalues = np.linalg.eigvals(result)
```

### SciPy Signal Processing
```python
from scipy import signal
import numpy as np

# Create a signal
t = np.linspace(0, 1, 500)
sig = np.sin(2*np.pi*5*t) + np.sin(2*np.pi*10*t)

# Apply FFT
fft_result = np.fft.fft(sig)
```

### SciPy Optimization
```python
from scipy.optimize import minimize

def objective(x):
    return x[0]**2 + x[1]**2

result = minimize(objective, [1, 1])
```

## ML Workflow Example

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

## Integration with Other Tools

### Jupyter Notebooks
Can be combined with Jupyter for interactive development:
```bash
pip install jupyter
jupyter notebook
```

### Data Visualization
Add matplotlib for plotting:
```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.ylabel('values')
plt.show()
```

## Memory and CPU Optimization

### Use Smaller Data Types
```python
# Instead of float64, use float32 for less memory
data = np.array([1.0, 2.0], dtype=np.float32)
```

### Vectorize Operations
```python
# Vectorized (fast)
result = np.sqrt(data)

# Loop-based (slow)
result = [np.sqrt(x) for x in data]
```

## Known Limitations

- Fortran compilation increases build time
- Full SciPy stack requires significant storage
- Some advanced features may need additional dependencies
- BLAS/LAPACK performance depends on hardware optimizations

## Related Features

- **Deep Learning**: Complement with Hailo for hardware-accelerated inference
- **Cameras**: Process RealSense depth data with NumPy
- **Protocols**: Stream data via Zenoh for distributed ML
- **ROS2**: Integrate with robot sensor processing

## Additional Resources

- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Documentation](https://docs.scipy.org/)
- [meta-python-ai Layer](https://github.com/zboszor/meta-python-ai)
- [Python Scientific Lecture Notes](https://scipy-lectures.org/)
- [NumPy for Embedded Systems](https://numpy.org/doc/stable/user/c-info.html)
