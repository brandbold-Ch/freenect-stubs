# Freenect Type Stubs

Comprehensive type hints (`.pyi` stubs) for the **freenect** Python bindings. This package provides full static type checking support for libfreenect, the cross-platform library for interacting with Microsoft Kinect sensors.

## Overview

[**libfreenect**](https://github.com/OpenKinect/libfreenect) is a cross-platform C library that provides access to Kinect sensor hardware. The **freenect** Python module wraps this C library but lacks type hints, making it difficult to use with modern Python tooling like Pylance, mypy, and IDEs.

This package provides complete PEP 484-compliant type stubs (`.pyi` files) for the freenect module, enabling:

- ✅ Full IDE autocomplete and IntelliSense
- ✅ Static type checking with mypy, Pylance, pyright
- ✅ Better code documentation and discoverability
- ✅ Proper numpy array type hints

## Installation

```bash
pip install freenect-stubs
```

The stubs are compatible with the standard `freenect` package. Install both:

```bash
pip install freenect freenect-stubs
```

## Features

### Complete Type Coverage

The stubs include type hints for:

- **Device Management**: Context and device initialization, enumeration, and cleanup
- **Depth Sensor**: Depth frame acquisition (synchronous and asynchronous)
- **RGB/Video Camera**: Video frame capture with multiple formats
- **Motor Control**: Tilt motor position and LED control  
- **Accelerometer**: 3-axis accelerometer readings
- **Event Processing**: Callback-based frame processing with proper typing

### Numpy Integration

Proper numpy array type hints for frame data:

```python
import freenect
from numpy.typing import NDArray
import numpy as np

# Type hints work correctly
depth: NDArray[np.uint16]
rgb: NDArray[np.uint8]

depth, ts = freenect.sync_get_depth()  # Properly typed
rgb, ts = freenect.sync_get_video()    # Properly typed
```

### Well-Documented API

Extensive docstrings with:

- Parameter descriptions
- Return type documentation
- Usage examples
- Format and resolution constants explained

## Quick Start

### Synchronous Frame Capture

```python
import freenect

# Get a depth frame (blocking)
depth, timestamp = freenect.sync_get_depth()
print(f"Depth shape: {depth.shape}")  # (480, 640)

# Get an RGB frame (blocking)
rgb, timestamp = freenect.sync_get_video()
print(f"RGB shape: {rgb.shape}")  # (480, 640, 3)
```

### Asynchronous Frame Processing

```python
import freenect
import numpy as np

def process_depth(dev: freenect.DevPtr, depth: np.ndarray, ts: int):
    print(f"Processing depth frame at {ts}ms")
    # Process frame...
    
ctx = freenect.init()
dev = freenect.open_device(ctx, 0)

freenect.set_depth_mode(dev, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_11BIT)
freenect.set_depth_callback(dev, process_depth)
freenect.start_depth(dev)
# ... frames processed via callback ...
freenect.stop_depth(dev)

freenect.close_device(dev)
freenect.shutdown(ctx)
```

## Module Structure

### Constants

**Video Formats** (for RGB/IR camera):
- `VIDEO_RGB`, `VIDEO_BAYER`, `VIDEO_IR_8BIT`, `VIDEO_IR_10BIT`, `VIDEO_IR_10BIT_PACKED`, `VIDEO_YUV_RGB`, `VIDEO_YUV_RAW`

**Depth Formats** (for depth sensor):
- `DEPTH_11BIT` (default), `DEPTH_10BIT`, `DEPTH_11BIT_PACKED`, `DEPTH_10BIT_PACKED`, `DEPTH_REGISTERED`, `DEPTH_MM`

**Resolution Modes**:
- `RESOLUTION_LOW` (320×240), `RESOLUTION_MEDIUM` (640×480), `RESOLUTION_HIGH` (1280×960)

**LED Modes**:
- `LED_OFF`, `LED_GREEN`, `LED_RED`, `LED_YELLOW`, `LED_BLINK_GREEN`, `LED_BLINK_RED_YELLOW`

**Device Types**:
- `DEVICE_MOTOR`, `DEVICE_CAMERA`, `DEVICE_AUDIO`

### Classes

- **`CtxPtr`**: Opaque libfreenect context (created by `init()`)
- **`DevPtr`**: Opaque Kinect device pointer (created by `open_device()`)
- **`StatePtr`**: Device state information
- **`Kill`**: Exception to terminate event loops from callbacks

### Main Functions

#### Initialization
- `init() -> CtxPtr`
- `shutdown(ctx: CtxPtr) -> int`

#### Device Management
- `num_devices(ctx: CtxPtr) -> int`
- `open_device(ctx: CtxPtr, index: int) -> DevPtr`
- `close_device(dev: DevPtr) -> int`

#### Depth Sensor
- `set_depth_mode(dev: DevPtr, res: int, mode: int) -> None`
- `start_depth(dev: DevPtr) -> int`
- `stop_depth(dev: DevPtr) -> int`
- `sync_get_depth(index: int = 0, format: int = DEPTH_11BIT) -> tuple[NDArray[np.uint16], int]`
- `set_depth_callback(dev: DevPtr, cb: Callable[[DevPtr, NDArray[np.uint16], int], Any]) -> None`
- `get_depth_format(dev: DevPtr) -> int`

#### Video/RGB Camera
- `set_video_mode(dev: DevPtr, res: int, mode: int) -> None`
- `start_video(dev: DevPtr) -> int`
- `stop_video(dev: DevPtr) -> int`
- `sync_get_video(index: int = 0, format: int = VIDEO_RGB) -> tuple[NDArray[np.uint8], int]`
- `set_video_callback(dev: DevPtr, cb: Callable[[DevPtr, NDArray[np.uint8], int], Any]) -> None`
- `get_video_format(dev: DevPtr) -> int`

#### Motor & Sensors
- `update_tilt_state(dev: DevPtr) -> int`
- `get_tilt_state(dev: DevPtr) -> int`
- `get_accel(dev: DevPtr) -> tuple[int, int, int]`

#### Event Processing
- `process_events(ctx: CtxPtr) -> int`
- `sync_stop() -> None`

## Usage Examples

For complete usage examples, see [**USAGE_EXAMPLES.md**](./USAGE_EXAMPLES.md).

Examples include:
- Basic device initialization
- Synchronous depth/video capture
- Asynchronous callbacks
- Motor control
- Error handling
- Full working examples

## Compatibility

- **Python**: 3.12+
- **freenect**: 0.1.0+
- **Type Checkers**: mypy, Pylance, pyright, pyre
- **IDEs**: VS Code (with Pylance), PyCharm, Vim (with LSP)

## Type Checking

Use these type checkers with the stubs:

### mypy

```bash
mypy --strict your_script.py
```

### Pylance (VS Code)

Enable in `settings.json`:
```json
{
  "pylance.typeCheckingMode": "basic"
}
```

### pyright

```bash
pyright your_script.py
```

## Development

The stubs are defined in:
```
freenect/__init__.pyi
```

Each function, class, and constant has:
- Complete type annotations
- Comprehensive docstrings
- Usage examples where applicable
- Clear parameter and return documentation

## Contributing

To improve these stubs:

1. Check the official [libfreenect documentation](https://github.com/OpenKinect/libfreenect/blob/master/wrappers/python/README.md)
2. Test type hints with mypy or Pylance
3. Update docstrings for clarity
4. Add examples for complex functions
5. Submit improvements

## License

These type stubs are provided under the same license as the freenect package. See the [freenect repository](https://github.com/OpenKinect/libfreenect) for more information.

## See Also

- [libfreenect GitHub](https://github.com/OpenKinect/libfreenect)
- [freenect Python wrapper](https://github.com/OpenKinect/libfreenect/tree/master/wrappers/python)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [PEP 561 - Distributing Type Information](https://www.python.org/dev/peps/pep-0561/)
