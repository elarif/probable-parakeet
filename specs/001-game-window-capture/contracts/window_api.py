"""
Window Detection and Management API Contract

This contract defines the interface for detecting and managing game windows.
Implements FR-001, FR-002, FR-003, FR-012, FR-014.
"""

from typing import List, Optional
from dataclasses import dataclass
from enum import IntEnum


class WindowState(IntEnum):
    """Window state enumeration."""
    NORMAL = 0
    MINIMIZED = 1
    MAXIMIZED = 2
    CLOSED = 3


@dataclass
class GameWindow:
    """Represents a detected game window."""
    handle: int
    title: str
    width: int
    height: int
    x: int
    y: int
    state: WindowState
    is_visible: bool
    process_id: int


class WindowNotFoundError(Exception):
    """Raised when expected window is not found or becomes invalid."""
    pass


class WindowDetectionTimeoutError(Exception):
    """Raised when window detection exceeds timeout threshold."""
    pass


class WindowDetector:
    """Interface for game window detection and management."""
    
    def find_windows_by_title(
        self, 
        title_pattern: str, 
        timeout_seconds: float = 5.0
    ) -> List[GameWindow]:
        """
        Find all windows matching the given title pattern.
        
        Args:
            title_pattern: String to match in window title (case-insensitive substring match)
            timeout_seconds: Maximum time to wait for window detection
        
        Returns:
            List of GameWindow objects (empty list if no matches found)
        
        Raises:
            WindowDetectionTimeoutError: If detection exceeds timeout
            ValueError: If title_pattern is empty string
        
        Example:
            detector = WindowDetector()
            windows = detector.find_windows_by_title("Raid")
            # Returns all windows with "Raid" in title
        
        Performance: <500ms for typical system (10-50 windows)
        """
        raise NotImplementedError
    
    def get_window_by_handle(self, handle: int) -> Optional[GameWindow]:
        """
        Get window information by window handle.
        
        Args:
            handle: Windows window handle (HWND)
        
        Returns:
            GameWindow if handle is valid, None if window no longer exists
        
        Example:
            window = detector.get_window_by_handle(263458)
            if window is None:
                print("Window closed")
        """
        raise NotImplementedError
    
    def get_window_state(self, handle: int) -> WindowState:
        """
        Get current state of window by handle.
        
        Args:
            handle: Windows window handle
        
        Returns:
            Current WindowState
        
        Raises:
            WindowNotFoundError: If handle is invalid or window closed
        
        Example:
            state = detector.get_window_state(263458)
            if state == WindowState.MINIMIZED:
                print("Window is minimized")
        """
        raise NotImplementedError
    
    def is_window_valid(self, handle: int) -> bool:
        """
        Check if window handle is still valid (window exists).
        
        Args:
            handle: Windows window handle
        
        Returns:
            True if window exists, False otherwise
        
        Example:
            if not detector.is_window_valid(old_handle):
                # Re-detect window
                windows = detector.find_windows_by_title("Raid")
        
        Performance: <10ms (fast validity check)
        """
        raise NotImplementedError
    
    def refresh_window_info(self, handle: int) -> GameWindow:
        """
        Refresh window dimensions and position (for resized/moved windows).
        
        Args:
            handle: Windows window handle
        
        Returns:
            Updated GameWindow object
        
        Raises:
            WindowNotFoundError: If handle is invalid
        
        Use Case: When window may have been resized between capture and click,
                  call this to get current dimensions for coordinate scaling.
        
        Example:
            # After 10 seconds, window might have been resized
            updated_window = detector.refresh_window_info(handle)
            # Use updated_window.width, updated_window.height for scaling
        """
        raise NotImplementedError


class WindowMonitor:
    """Interface for monitoring window state changes."""
    
    def start_monitoring(
        self, 
        handle: int, 
        poll_interval_seconds: float = 1.0,
        on_state_change=None
    ) -> None:
        """
        Start monitoring window for state changes.
        
        Args:
            handle: Window handle to monitor
            poll_interval_seconds: How often to check window state
            on_state_change: Optional callback(old_state, new_state, window)
        
        Example:
            def handle_change(old, new, window):
                if new == WindowState.CLOSED:
                    print("Game closed!")
            
            monitor = WindowMonitor()
            monitor.start_monitoring(handle, on_state_change=handle_change)
        
        Implementation: Runs in background thread, polls window state
        """
        raise NotImplementedError
    
    def stop_monitoring(self, handle: int) -> None:
        """
        Stop monitoring a window.
        
        Args:
            handle: Window handle to stop monitoring
        """
        raise NotImplementedError
