"""Type stubs for freenect - Python bindings for libfreenect.

libfreenect is a cross-platform library for interacting with the Microsoft
Kinect sensor hardware. This module provides Python bindings for depth and
video frame acquisition, as well as motor and LED control.
"""

from typing import Any, Callable

import numpy as np
from numpy.typing import NDArray

# =======================
# Format Constants
# =======================

# Video format modes for the RGB/IR camera
VIDEO_RGB: int
"""RGB video format (640x480, 3 channels)"""

VIDEO_BAYER: int
"""Bayer video format (raw Bayer pattern)"""

VIDEO_IR_8BIT: int
"""8-bit infrared video format"""

VIDEO_IR_10BIT: int
"""10-bit infrared video format"""

VIDEO_IR_10BIT_PACKED: int
"""10-bit packed infrared video format"""

VIDEO_YUV_RGB: int
"""YUV to RGB converted video format"""

VIDEO_YUV_RAW: int
"""Raw YUV video format"""

# Depth format modes for the depth sensor
DEPTH_11BIT: int
"""11-bit depth format (default, most common)"""

DEPTH_10BIT: int
"""10-bit depth format"""

DEPTH_11BIT_PACKED: int
"""11-bit packed depth format"""

DEPTH_10BIT_PACKED: int
"""10-bit packed depth format"""

DEPTH_REGISTERED: int
"""Depth registered to RGB camera coordinates"""

DEPTH_MM: int
"""Depth in millimeters"""

# LED color modes
LED_OFF: int
"""Turn LED off"""

LED_GREEN: int
"""Set LED to green"""

LED_RED: int
"""Set LED to red"""

LED_YELLOW: int
"""Set LED to yellow"""

LED_BLINK_GREEN: int
"""Blink LED green"""

LED_BLINK_RED_YELLOW: int
"""Blink LED red and yellow"""

# Resolution modes
RESOLUTION_LOW: int
"""Low resolution (320x240)"""

RESOLUTION_MEDIUM: int
"""Medium resolution (640x480)"""

RESOLUTION_HIGH: int
"""High resolution (1280x960)"""

# Device types (for multi-device support)
DEVICE_MOTOR: int
"""Motor control device (tilt)"""

DEVICE_CAMERA: int
"""Camera/RGB device"""

DEVICE_AUDIO: int
"""Audio device"""

# =======================
# Opaque Pointer Types
# =======================

class CtxPtr:
    """Opaque pointer to a libfreenect context.
    
    Created by init() and used for device enumeration and management.
    Must be passed to open_device() and shutdown().
    """
    ...

class DevPtr:
    """Opaque pointer to a Kinect device.
    
    Created by open_device() and used for all device operations
    including frame acquisition and motor control.
    Must be passed to depth/video functions and closed with close_device().
    """
    ...

class StatePtr:
    """Opaque pointer to device state information.
    
    Contains tilt motor state and accelerometer data.
    Retrieved by get_tilt_state().
    """
    ...

# =======================
# Exception Classes
# =======================

class Kill(Exception):
    """Exception to terminate the event processing loop.
    
    Raise this exception from within a callback function to stop
    the runloop started by runloop(). This is the proper way to exit
    an asynchronous frame acquisition loop.
    
    Example:
        >>> def depth_callback(dev, depth, timestamp):
        ...     if should_stop():
        ...         raise freenect.Kill()
        ...     process_frame(depth)
    """
    ...

# =======================
# Initialization Functions
# =======================

def init() -> CtxPtr:
    """Initialize libfreenect and create a device context.
    
    This must be called before any other freenect operations.
    Returns a context pointer to be used with open_device() and shutdown().
    
    Returns:
        CtxPtr: A new libfreenect context.
        
    Raises:
        RuntimeError: If initialization fails.
        
    Example:
        >>> ctx = freenect.init()
        >>> # ... use ctx to open devices ...
        >>> freenect.shutdown(ctx)
    """
    ...

def shutdown(ctx: CtxPtr) -> int:
    """Clean up and close a libfreenect context.
    
    Closes all devices associated with this context and releases resources.
    Call this once you're done with the context.
    
    Args:
        ctx: The context to shutdown (from init()).
        
    Returns:
        int: 0 on success, negative on error.
    """
    ...

# =======================
# Device Management
# =======================

def num_devices(ctx: CtxPtr) -> int:
    """Get the number of Kinect devices available.
    
    Args:
        ctx: The libfreenect context.
        
    Returns:
        int: Number of connected Kinect devices (>= 0).
    """
    ...

def open_device(ctx: CtxPtr, index: int) -> DevPtr:
    """Open a Kinect device by index.
    
    Opens the device at the specified index (0-based). Call num_devices()
    first to determine how many devices are available.
    
    Args:
        ctx: The libfreenect context.
        index: Device index (0 for first device, etc.).
        
    Returns:
        DevPtr: A device pointer for the opened device.
        
    Raises:
        RuntimeError: If the device cannot be opened.
        
    Example:
        >>> ctx = freenect.init()
        >>> dev = freenect.open_device(ctx, 0)
    """
    ...

def close_device(dev: DevPtr) -> int:
    """Close a Kinect device.
    
    Closes the device and stops any active streams. Terminates the
    synchronous runloop if running, otherwise this is a no-op.
    
    Args:
        dev: The device to close.
        
    Returns:
        int: 0 on success, negative on error.
    """
    ...

def error_open_device() -> None:
    """Get the last device open error.
    
    Call this after a failed open_device() to get more details about
    the error. The error message is typically printed to stderr.
    """
    ...

# =======================
# Depth Sensor Functions
# =======================

def set_depth_mode(dev: DevPtr, res: int, mode: int) -> None:
    """Set the depth sensor resolution and format.
    
    Configures the depth sensor before starting. Use RESOLUTION_* and
    DEPTH_* constants.
    
    Args:
        dev: The device.
        res: Resolution mode (RESOLUTION_LOW, RESOLUTION_MEDIUM, RESOLUTION_HIGH).
        mode: Depth format (DEPTH_11BIT, DEPTH_10BIT, DEPTH_REGISTERED, etc.).
        
    Example:
        >>> freenect.set_depth_mode(dev, freenect.RESOLUTION_MEDIUM, 
        ...                         freenect.DEPTH_11BIT)
    """
    ...

def get_depth_format(dev: DevPtr) -> int:
    """Get the current depth format of a device.
    
    Args:
        dev: The device.
        
    Returns:
        int: The current depth format constant.
    """
    ...

def start_depth(dev: DevPtr) -> int:
    """Start capturing depth frames.
    
    Begins streaming depth data from the device. Set up a callback with
    set_depth_callback() first if you want to process frames asynchronously,
    or use sync_get_depth() for synchronous access.
    
    Args:
        dev: The device.
        
    Returns:
        int: 0 on success, negative on error.
        
    Example:
        >>> freenect.set_depth_callback(dev, my_callback)
        >>> freenect.start_depth(dev)
    """
    ...

def stop_depth(dev: DevPtr) -> int:
    """Stop capturing depth frames.
    
    Args:
        dev: The device.
        
    Returns:
        int: 0 on success, negative on error.
    """
    ...

def sync_get_depth(
    index: int = 0, format: int = DEPTH_11BIT
) -> tuple[NDArray[np.uint16], int]:
    """Get the next available depth frame synchronously.
    
    Blocks until a new depth frame is available, then returns it.
    This is a convenience function for simple synchronous use cases.
    For more control, use start_depth() with set_depth_callback().
    
    Args:
        index: Kinect device index (default: 0 for first device).
        format: Depth format (default: DEPTH_11BIT).
        
    Returns:
        tuple: (depth_array, timestamp) where:
            - depth_array: numpy array with shape (480, 640), dtype uint16.
              Values represent millimeter depth or raw depth counts
              depending on the format.
            - timestamp: int representing the kernel timestamp in milliseconds.
            
    Raises:
        RuntimeError: If frame acquisition fails.
        
    Example:
        >>> depth, ts = freenect.sync_get_depth()
        >>> print(f"Depth frame at {ts}ms")
        >>> print(depth.shape, depth.min(), depth.max())
    """
    ...

def set_depth_callback(
    dev: DevPtr, cb: Callable[[DevPtr, NDArray[np.uint16], int], Any]
) -> None:
    """Set an asynchronous callback for depth frames.
    
    When depth streaming is active, the callback is invoked for each
    new depth frame. Raise Kill() from the callback to stop streaming.
    
    Args:
        dev: The device.
        cb: Callback function with signature (device, depth_array, timestamp).
            - device: DevPtr of the device that produced the frame.
            - depth_array: numpy array, shape (480, 640), dtype uint16.
            - timestamp: int millisecond timestamp.
            
    Example:
        >>> def on_depth(dev, depth, ts):
        ...     print(f"Depth frame: {depth.shape}")
        >>> freenect.set_depth_callback(dev, on_depth)
    """
    ...

# =======================
# Video/RGB Camera Functions
# =======================

def set_video_mode(dev: DevPtr, res: int, mode: int) -> None:
    """Set the video camera resolution and format.
    
    Configures the RGB/IR camera before starting. Use RESOLUTION_* and
    VIDEO_* constants.
    
    Args:
        dev: The device.
        res: Resolution mode (RESOLUTION_LOW, RESOLUTION_MEDIUM, RESOLUTION_HIGH).
        mode: Video format (VIDEO_RGB, VIDEO_IR_8BIT, VIDEO_YUV_RGB, etc.).
        
    Example:
        >>> freenect.set_video_mode(dev, freenect.RESOLUTION_MEDIUM,
        ...                         freenect.VIDEO_RGB)
    """
    ...

def get_video_format(dev: DevPtr) -> int:
    """Get the current video format of a device.
    
    Args:
        dev: The device.
        
    Returns:
        int: The current video format constant.
    """
    ...

def start_video(dev: DevPtr) -> int:
    """Start capturing video frames from the RGB camera.
    
    Begins streaming RGB/IR data from the device. Set up a callback with
    set_video_callback() first if you want to process frames asynchronously,
    or use sync_get_video() for synchronous access.
    
    Args:
        dev: The device.
        
    Returns:
        int: 0 on success, negative on error.
        
    Example:
        >>> freenect.set_video_callback(dev, my_callback)
        >>> freenect.start_video(dev)
    """
    ...

def stop_video(dev: DevPtr) -> int:
    """Stop capturing video frames.
    
    Args:
        dev: The device.
        
    Returns:
        int: 0 on success, negative on error.
    """
    ...

def sync_get_video(
    index: int = 0, format: int = VIDEO_RGB
) -> tuple[NDArray[np.uint8], int]:
    """Get the next available video frame from the RGB camera synchronously.
    
    Blocks until a new frame is available, then returns it.
    This is a convenience function for simple synchronous use cases.
    For more control, use start_video() with set_video_callback().
    
    Args:
        index: Kinect device index (default: 0 for first device).
        format: Video format (default: VIDEO_RGB).
        
    Returns:
        tuple: (video_array, timestamp) where:
            - video_array: numpy array with shape (480, 640, 3), dtype uint8.
              For RGB format, channels are [R, G, B] with values 0-255.
              For IR formats, the shape and channel count may differ.
            - timestamp: int representing the kernel timestamp in milliseconds.
            
    Raises:
        RuntimeError: If frame acquisition fails.
        
    Example:
        >>> rgb, ts = freenect.sync_get_video()
        >>> print(f"RGB frame at {ts}ms, shape: {rgb.shape}")
    """
    ...

def set_video_callback(
    dev: DevPtr, cb: Callable[[DevPtr, NDArray[np.uint8], int], Any]
) -> None:
    """Set an asynchronous callback for video frames.
    
    When video streaming is active, the callback is invoked for each
    new video frame. Raise Kill() from the callback to stop streaming.
    
    Args:
        dev: The device.
        cb: Callback function with signature (device, video_array, timestamp).
            - device: DevPtr of the device that produced the frame.
            - video_array: numpy array, shape (480, 640, 3), dtype uint8 (for RGB).
            - timestamp: int millisecond timestamp.
            
    Example:
        >>> def on_video(dev, rgb, ts):
        ...     print(f"Video frame: {rgb.shape}")
        >>> freenect.set_video_callback(dev, on_video)
    """
    ...

# =======================
# Motor/Tilt Functions
# =======================

def update_tilt_state(dev: DevPtr) -> int:
    """Update the cached tilt motor state from the device.
    
    Queries the device for the current tilt motor angle and accelerometer
    readings. Must be called before get_tilt_state() to get fresh data.
    
    Args:
        dev: The device.
        
    Returns:
        int: 0 on success, negative on error.
    """
    ...

def get_tilt_state(dev: DevPtr) -> int:
    """Get the current tilt motor angle.
    
    Returns the angle from the most recent update_tilt_state() call.
    Call update_tilt_state() first to fetch fresh data from the device.
    
    Args:
        dev: The device.
        
    Returns:
        int: Tilt angle in degrees (-27 to 27 approximately).
        
    Example:
        >>> freenect.update_tilt_state(dev)
        >>> angle = freenect.get_tilt_state(dev)
        >>> print(f"Tilt angle: {angle}°")
    """
    ...

def get_accel(dev: DevPtr) -> tuple[int, int, int]:
    """Get accelerometer readings in SI units (m/s²).
    
    Returns the X, Y, Z accelerometer values from the Kinect's built-in
    motion sensor. These values are in SI units (meters per second squared).
    
    Args:
        dev: The device.
        
    Returns:
        tuple: (x, y, z) accelerometer values in m/s².
        
    Example:
        >>> x, y, z = freenect.get_accel(dev)
        >>> print(f"Acceleration: x={x} y={y} z={z} m/s²")
    """
    ...

# =======================
# Event Processing
# =======================

def process_events(ctx: CtxPtr) -> int:
    """Process pending events from the libfreenect event loop.
    
    This function is used in custom event loops when you don't want to use
    the runloop() convenience function. Call this repeatedly to let
    libfreenect process USB events and invoke callbacks.
    
    Args:
        ctx: The libfreenect context.
        
    Returns:
        int: 0 on success, negative on error.
        
    Note:
        For simple applications, use runloop() instead of calling this
        and managing the event loop yourself.
    """
    ...

def sync_stop() -> None:
    """Stop the synchronous frame acquisition loop.
    
    Terminates any active sync_get_depth() or sync_get_video() calls.
    Use this to exit from blocking synchronous calls.
    """
    ...
