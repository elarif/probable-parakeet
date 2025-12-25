"""
Screen Capture API Contract

This contract defines the interface for capturing window content.
Implements FR-004, FR-005, FR-013.
"""

from typing import Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class WindowCapture:
    """Represents a captured screenshot of a window."""
    image: np.ndarray  # Shape: (height, width, 3), dtype: uint8, BGR format
    width: int
    height: int
    timestamp: datetime
    window_handle: int
    format: str  # "BGR", "RGB", or "GRAY"


class CaptureTimeoutError(Exception):
    """Raised when screen capture exceeds timeout threshold."""
    pass


class CaptureFailedError(Exception):
    """Raised when screen capture fails (invalid handle, insufficient permissions)."""
    pass


class ScreenCapture:
    """Interface for capturing window content."""
    
    def capture_window(
        self, 
        window_handle: int,
        timeout_seconds: float = 5.0,
        color_format: str = "BGR"
    ) -> WindowCapture:
        """
        Capture the visible content of a game window.
        
        Args:
            window_handle: Windows window handle (HWND)
            timeout_seconds: Maximum time to wait for capture completion
            color_format: Output color format ("BGR", "RGB", or "GRAY")
        
        Returns:
            WindowCapture object with image data as NumPy array
        
        Raises:
            CaptureTimeoutError: If capture exceeds timeout
            CaptureFailedError: If capture fails (invalid handle, permissions)
            ValueError: If color_format is invalid
        
        Example:
            capturer = ScreenCapture()
            capture = capturer.capture_window(handle)
            # capture.image is np.ndarray, shape (1080, 1920, 3) for 1920x1080 window
            
            # Display with OpenCV
            import cv2
            cv2.imshow("Game", capture.image)
        
        Performance: ≥10 FPS (≤100ms per capture) for typical game windows
        
        Notes:
            - Captures window content regardless of position/monitor
            - If window is minimized, may capture last visible state or blank
            - Overlapping windows may be included in capture (depends on method)
        """
        raise NotImplementedError
    
    def capture_region(
        self,
        window_handle: int,
        x: int,
        y: int,
        width: int,
        height: int,
        timeout_seconds: float = 5.0,
        color_format: str = "BGR"
    ) -> WindowCapture:
        """
        Capture a specific region within a window.
        
        Args:
            window_handle: Windows window handle
            x: Region top-left X coordinate (window-relative)
            y: Region top-left Y coordinate (window-relative)
            width: Region width in pixels
            height: Region height in pixels
            timeout_seconds: Maximum time to wait for capture
            color_format: Output color format
        
        Returns:
            WindowCapture object with cropped image
        
        Raises:
            CaptureTimeoutError: If capture exceeds timeout
            CaptureFailedError: If capture fails
            ValueError: If region coordinates invalid (negative, out of bounds)
        
        Example:
            # Capture only the top-right corner (for minimap detection)
            capture = capturer.capture_region(
                handle, 
                x=1500, y=0, 
                width=420, height=420
            )
        
        Use Case: OCR on specific UI regions (faster than full window capture)
        
        Performance: Faster than full capture for small regions
        """
        raise NotImplementedError
    
    def capture_window_to_file(
        self,
        window_handle: int,
        filepath: str,
        timeout_seconds: float = 5.0
    ) -> None:
        """
        Capture window and save directly to file (for debugging).
        
        Args:
            window_handle: Windows window handle
            filepath: Output file path (PNG format recommended)
            timeout_seconds: Maximum time to wait
        
        Raises:
            CaptureTimeoutError: If capture exceeds timeout
            CaptureFailedError: If capture or file write fails
            IOError: If file cannot be written
        
        Example:
            capturer.capture_window_to_file(handle, "debug_capture.png")
        
        Use Case: Debugging - save failed detection screenshots
        """
        raise NotImplementedError
    
    def get_capture_fps(self, sample_duration_seconds: float = 5.0) -> float:
        """
        Measure capture frame rate for performance testing.
        
        Args:
            sample_duration_seconds: How long to sample captures
        
        Returns:
            Average frames per second achieved
        
        Example:
            fps = capturer.get_capture_fps()
            print(f"Capture rate: {fps:.1f} FPS")
            # Expected: 10-30 FPS depending on window size and system
        
        Use Case: Validate performance requirements (SC-002: ≥10 FPS)
        """
        raise NotImplementedError
