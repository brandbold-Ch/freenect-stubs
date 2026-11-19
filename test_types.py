"""
Type checking test file to verify that type hints are working correctly.

Run with: mypy test_types.py
Or: pylance with typeCheckingMode set to basic/strict
"""

import freenect
from typing import Any
import numpy as np
from numpy.typing import NDArray


def test_initialization() -> None:
    """Test initialization functions."""
    ctx: freenect.CtxPtr = freenect.init()
    num: int = freenect.num_devices(ctx)
    result: int = freenect.shutdown(ctx)


def test_device_management() -> None:
    """Test device management functions."""
    ctx = freenect.init()
    
    # Test opening device
    dev: freenect.DevPtr = freenect.open_device(ctx, 0)
    
    # Test closing device
    close_result: int = freenect.close_device(dev)
    
    freenect.shutdown(ctx)


def test_depth_functions() -> None:
    """Test depth sensor functions."""
    ctx = freenect.init()
    dev = freenect.open_device(ctx, 0)
    
    # Set depth mode
    freenect.set_depth_mode(dev, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_11BIT)
    
    # Get depth format
    fmt: int = freenect.get_depth_format(dev)
    
    # Start/stop depth
    start_result: int = freenect.start_depth(dev)
    stop_result: int = freenect.stop_depth(dev)
    
    freenect.close_device(dev)
    freenect.shutdown(ctx)


def test_video_functions() -> None:
    """Test video/RGB camera functions."""
    ctx = freenect.init()
    dev = freenect.open_device(ctx, 0)
    
    # Set video mode
    freenect.set_video_mode(dev, freenect.RESOLUTION_MEDIUM, freenect.VIDEO_RGB)
    
    # Get video format
    fmt: int = freenect.get_video_format(dev)
    
    # Start/stop video
    start_result: int = freenect.start_video(dev)
    stop_result: int = freenect.stop_video(dev)
    
    freenect.close_device(dev)
    freenect.shutdown(ctx)


def test_sync_operations() -> None:
    """Test synchronous frame acquisition."""
    # Get depth frame
    depth: NDArray[np.uint16]
    timestamp: int
    depth, timestamp = freenect.sync_get_depth(
        index=0,
        format=freenect.DEPTH_11BIT
    )
    
    assert depth.shape == (480, 640)
    assert depth.dtype == np.uint16
    assert isinstance(timestamp, int)
    
    # Get video frame
    rgb: NDArray[np.uint8]
    rgb, timestamp = freenect.sync_get_video(
        index=0,
        format=freenect.VIDEO_RGB
    )
    
    assert rgb.shape == (480, 640, 3)
    assert rgb.dtype == np.uint8
    
    # Stop sync
    freenect.sync_stop()


def test_callbacks() -> None:
    """Test callback setup."""
    ctx = freenect.init()
    dev = freenect.open_device(ctx, 0)
    
    # Depth callback with proper type signature
    def depth_callback(
        device: freenect.DevPtr,
        depth: NDArray[np.uint16],
        ts: int
    ) -> None:
        print(f"Depth frame at {ts}ms, shape: {depth.shape}")
    
    # Video callback with proper type signature
    def video_callback(
        device: freenect.DevPtr,
        rgb: NDArray[np.uint8],
        ts: int
    ) -> None:
        print(f"Video frame at {ts}ms, shape: {rgb.shape}")
    
    # Set callbacks
    freenect.set_depth_callback(dev, depth_callback)
    freenect.set_video_callback(dev, video_callback)
    
    freenect.close_device(dev)
    freenect.shutdown(ctx)


def test_motor_control() -> None:
    """Test motor and sensor functions."""
    ctx = freenect.init()
    dev = freenect.open_device(ctx, 0)
    
    # Update and get tilt state
    update_result: int = freenect.update_tilt_state(dev)
    angle: int = freenect.get_tilt_state(dev)
    
    # Get accelerometer readings
    x: int
    y: int
    z: int
    x, y, z = freenect.get_accel(dev)
    
    freenect.close_device(dev)
    freenect.shutdown(ctx)


def test_event_processing() -> None:
    """Test event processing functions."""
    ctx = freenect.init()
    
    # Process events
    result: int = freenect.process_events(ctx)
    
    freenect.shutdown(ctx)


def test_kill_exception() -> None:
    """Test Kill exception."""
    try:
        raise freenect.Kill()
    except freenect.Kill:
        print("Kill exception caught successfully")


def test_constants() -> None:
    """Test that all constants are properly typed."""
    # Video formats
    assert isinstance(freenect.VIDEO_RGB, int)
    assert isinstance(freenect.VIDEO_BAYER, int)
    assert isinstance(freenect.VIDEO_IR_8BIT, int)
    assert isinstance(freenect.VIDEO_IR_10BIT, int)
    
    # Depth formats
    assert isinstance(freenect.DEPTH_11BIT, int)
    assert isinstance(freenect.DEPTH_10BIT, int)
    
    # Resolutions
    assert isinstance(freenect.RESOLUTION_LOW, int)
    assert isinstance(freenect.RESOLUTION_MEDIUM, int)
    assert isinstance(freenect.RESOLUTION_HIGH, int)
    
    # LED modes
    assert isinstance(freenect.LED_OFF, int)
    assert isinstance(freenect.LED_GREEN, int)
    
    # Device types
    assert isinstance(freenect.DEVICE_MOTOR, int)
    assert isinstance(freenect.DEVICE_CAMERA, int)
    
    print("✅ All constants are properly typed")


if __name__ == "__main__":
    test_constants()
    print("✅ All type hints are properly defined")
