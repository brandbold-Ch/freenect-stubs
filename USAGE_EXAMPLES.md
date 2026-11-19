# Freenect Type Stubs - Usage Examples

This document provides examples of how to use the freenect Python bindings with proper type hints.

## Basic Setup

```python
import freenect
import numpy as np

# Initialize the libfreenect context
ctx = freenect.init()

# Check how many Kinect devices are connected
num_devices = freenect.num_devices(ctx)
print(f"Found {num_devices} device(s)")

# Open the first device (index 0)
dev = freenect.open_device(ctx, 0)

# Clean up when done
freenect.close_device(dev)
freenect.shutdown(ctx)
```

## Synchronous Depth Acquisition

Get depth frames one at a time (blocking):

```python
import freenect

# Get a single depth frame
depth_array, timestamp = freenect.sync_get_depth(
    index=0, 
    format=freenect.DEPTH_11BIT
)

print(f"Depth frame shape: {depth_array.shape}")  # (480, 640)
print(f"Frame timestamp: {timestamp} ms")
print(f"Min/Max depth: {depth_array.min()}/{depth_array.max()}")

# Stop the sync loop when done
freenect.sync_stop()
```

## Synchronous Video/RGB Acquisition

Get RGB frames one at a time (blocking):

```python
import freenect

# Get a single RGB frame
rgb_array, timestamp = freenect.sync_get_video(
    index=0,
    format=freenect.VIDEO_RGB
)

print(f"RGB frame shape: {rgb_array.shape}")  # (480, 640, 3)
print(f"Frame timestamp: {timestamp} ms")
print(f"Frame dtype: {rgb_array.dtype}")  # uint8

# Stop the sync loop when done
freenect.sync_stop()
```

## Asynchronous Depth Acquisition with Callbacks

```python
import freenect
from typing import Any
import numpy as np
from numpy.typing import NDArray

def depth_callback(dev: freenect.DevPtr, depth: NDArray[np.uint16], ts: int) -> None:
    """Process each depth frame as it arrives."""
    print(f"Received depth frame at {ts}ms")
    print(f"Min depth: {depth.min()}, Max depth: {depth.max()}")
    
    # Process the frame...
    # To stop the loop from within the callback, raise Kill()

# Setup
ctx = freenect.init()
dev = freenect.open_device(ctx, 0)

# Configure and start streaming
freenect.set_depth_mode(dev, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_11BIT)
freenect.set_depth_callback(dev, depth_callback)
freenect.start_depth(dev)

# ... let callbacks process frames ...

# Stop and cleanup
freenect.stop_depth(dev)
freenect.close_device(dev)
freenect.shutdown(ctx)
```

## Asynchronous Video/RGB Acquisition with Callbacks

```python
import freenect
import numpy as np
from numpy.typing import NDArray

def video_callback(dev: freenect.DevPtr, rgb: NDArray[np.uint8], ts: int) -> None:
    """Process each RGB frame as it arrives."""
    print(f"Received RGB frame at {ts}ms, shape: {rgb.shape}")
    
    # Process the frame...
    # To stop the loop, raise Kill()

# Setup
ctx = freenect.init()
dev = freenect.open_device(ctx, 0)

# Configure and start streaming
freenect.set_video_mode(dev, freenect.RESOLUTION_MEDIUM, freenect.VIDEO_RGB)
freenect.set_video_callback(dev, video_callback)
freenect.start_video(dev)

# ... let callbacks process frames ...

# Stop and cleanup
freenect.stop_video(dev)
freenect.close_device(dev)
freenect.shutdown(ctx)
```

## Stopping the Event Loop

You can stop the event loop from within a callback by raising `Kill`:

```python
import freenect
import numpy as np

frame_count = 0

def depth_callback(dev: freenect.DevPtr, depth: np.ndarray, ts: int) -> None:
    global frame_count
    frame_count += 1
    print(f"Frame {frame_count} received")
    
    # Stop after 100 frames
    if frame_count >= 100:
        raise freenect.Kill()

ctx = freenect.init()
dev = freenect.open_device(ctx, 0)
freenect.set_depth_callback(dev, depth_callback)
freenect.start_depth(dev)

# ... frames will be processed until Kill() is raised ...

freenect.close_device(dev)
freenect.shutdown(ctx)
```

## Working with the Motor/Tilt

```python
import freenect

ctx = freenect.init()
dev = freenect.open_device(ctx, 0)

# Get current tilt angle
freenect.update_tilt_state(dev)
angle = freenect.get_tilt_state(dev)
print(f"Current tilt angle: {angle}°")

# Get accelerometer readings
x, y, z = freenect.get_accel(dev)
print(f"Acceleration: x={x}, y={y}, z={z} m/s²")

freenect.close_device(dev)
freenect.shutdown(ctx)
```

## Depth Formats

Available depth formats (use with `set_depth_mode` and `sync_get_depth`):

- `DEPTH_11BIT` (default): 11-bit depth values, most common
- `DEPTH_10BIT`: 10-bit depth values
- `DEPTH_11BIT_PACKED`: 11-bit packed format
- `DEPTH_10BIT_PACKED`: 10-bit packed format
- `DEPTH_REGISTERED`: Depth registered to RGB coordinates
- `DEPTH_MM`: Depth in millimeters (Kinect v2 feature)

## Video/RGB Formats

Available video formats (use with `set_video_mode` and `sync_get_video`):

- `VIDEO_RGB` (default): RGB format, 3 channels (480x640x3)
- `VIDEO_BAYER`: Raw Bayer pattern
- `VIDEO_IR_8BIT`: 8-bit infrared
- `VIDEO_IR_10BIT`: 10-bit infrared
- `VIDEO_IR_10BIT_PACKED`: 10-bit packed infrared
- `VIDEO_YUV_RGB`: YUV converted to RGB
- `VIDEO_YUV_RAW`: Raw YUV format

## Resolution Modes

Available resolutions for both depth and video:

- `RESOLUTION_LOW`: 320x240
- `RESOLUTION_MEDIUM`: 640x480 (most common)
- `RESOLUTION_HIGH`: 1280x960

## Error Handling

```python
import freenect

ctx = freenect.init()
num_devs = freenect.num_devices(ctx)

if num_devs == 0:
    print("No Kinect devices found!")
else:
    dev = freenect.open_device(ctx, 0)
    if dev is None:
        print("Failed to open device")
        freenect.error_open_device()  # Print error details
    else:
        # Use device...
        freenect.close_device(dev)

freenect.shutdown(ctx)
```

## Full Example: Capture and Save Depth Map

```python
import freenect
import numpy as np
from pathlib import Path

def capture_depth_snapshot(output_path: Path) -> None:
    """Capture a single depth frame and save it."""
    ctx = freenect.init()
    
    try:
        depth, timestamp = freenect.sync_get_depth(
            index=0,
            format=freenect.DEPTH_11BIT
        )
        
        # Normalize to 0-255 for visualization
        depth_normalized = ((depth / depth.max()) * 255).astype(np.uint8)
        
        # Save using numpy or image library
        np.save(output_path, depth_normalized)
        print(f"Saved depth frame to {output_path}")
        print(f"Timestamp: {timestamp}ms")
        
    finally:
        freenect.sync_stop()

if __name__ == "__main__":
    capture_depth_snapshot(Path("depth_frame.npy"))
```

## Notes

- Always call `shutdown()` when done to properly release resources
- The `CtxPtr`, `DevPtr`, and `StatePtr` types are opaque C pointers; don't create them directly
- Callback functions should complete quickly to avoid frame drops
- Raise `Kill()` from a callback to exit the event loop
- Use `sync_get_depth()` / `sync_get_video()` for simple, blocking operations
- Use callbacks with `start_depth()` / `start_video()` for high-performance streaming
