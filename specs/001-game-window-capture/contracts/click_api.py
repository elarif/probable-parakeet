"""
Click Automation API Contract

This contract defines the interface for executing mouse clicks.
Implements FR-006, FR-007, FR-008.
"""

from typing import Optional, Tuple
from dataclasses import dataclass
from enum import IntEnum


class CoordinateType(IntEnum):
    """Coordinate interpretation modes."""
    ABSOLUTE = 0  # x/y are absolute pixels within window
    RELATIVE = 1  # x/y are percentages (0.0-1.0) of window dimensions
    SCALED = 2    # x/y are reference resolution pixels, scaled to actual size


class ClickType(IntEnum):
    """Mouse click types."""
    LEFT = 0
    RIGHT = 1
    MIDDLE = 2
    DOUBLE = 3  # Double left-click


@dataclass
class ClickTarget:
    """Specifies where and how to execute a click."""
    x: int | float  # Coordinate (type depends on coordinate_type)
    y: int | float
    window_handle: int
    coordinate_type: CoordinateType
    click_type: ClickType
    delay_ms: int = 50  # Delay between mouse down and up


class ClickFailedError(Exception):
    """Raised when click execution fails."""
    pass


class ClickHandler:
    """Interface for executing mouse clicks in game windows."""
    
    def __init__(
        self, 
        reference_width: int = 1920, 
        reference_height: int = 1080
    ):
        """
        Initialize click handler with reference resolution for scaling.
        
        Args:
            reference_width: Reference resolution width (for SCALED coordinates)
            reference_height: Reference resolution height (for SCALED coordinates)
        
        Example:
            # Use 1920x1080 as reference for all scaled clicks
            handler = ClickHandler(reference_width=1920, reference_height=1080)
        """
        raise NotImplementedError
    
    def click(
        self, 
        target: ClickTarget,
        bring_to_foreground: bool = True
    ) -> None:
        """
        Execute a mouse click at the specified target.
        
        Args:
            target: ClickTarget specifying location and click type
            bring_to_foreground: Whether to bring window to foreground before clicking
        
        Raises:
            ClickFailedError: If click execution fails
            ValueError: If coordinates are invalid for the coordinate_type
        
        Example:
            # Click at absolute coordinates (960, 540)
            target = ClickTarget(
                x=960, y=540,
                window_handle=handle,
                coordinate_type=CoordinateType.ABSOLUTE,
                click_type=ClickType.LEFT
            )
            handler.click(target)
        
        Performance: <200ms total (includes bringing window to foreground)
        
        Notes:
            - If bring_to_foreground=False, attempts background click (may not work for all games)
            - Some games require foreground focus to accept input
            - Coordinates automatically scaled if coordinate_type=SCALED
        """
        raise NotImplementedError
    
    def click_at(
        self,
        x: int | float,
        y: int | float,
        window_handle: int,
        coordinate_type: CoordinateType = CoordinateType.ABSOLUTE,
        click_type: ClickType = ClickType.LEFT
    ) -> None:
        """
        Convenience method to click at coordinates without creating ClickTarget.
        
        Args:
            x: X coordinate
            y: Y coordinate
            window_handle: Target window handle
            coordinate_type: How to interpret coordinates
            click_type: Type of click
        
        Example:
            # Quick click at center (relative coordinates)
            handler.click_at(
                0.5, 0.5, 
                handle, 
                coordinate_type=CoordinateType.RELATIVE
            )
        """
        raise NotImplementedError
    
    def double_click_at(
        self,
        x: int | float,
        y: int | float,
        window_handle: int,
        coordinate_type: CoordinateType = CoordinateType.ABSOLUTE
    ) -> None:
        """
        Convenience method for double-click.
        
        Example:
            handler.double_click_at(850, 920, handle)
        """
        raise NotImplementedError
    
    def scale_coordinates(
        self,
        ref_x: int,
        ref_y: int,
        window_width: int,
        window_height: int
    ) -> Tuple[int, int]:
        """
        Scale reference resolution coordinates to actual window size.
        
        Args:
            ref_x: X coordinate in reference resolution
            ref_y: Y coordinate in reference resolution
            window_width: Actual window width
            window_height: Actual window height
        
        Returns:
            Tuple of (scaled_x, scaled_y) in actual window coordinates
        
        Example:
            # Reference click at (960, 540) for 1920x1080
            # Scale to 1280x720 window
            actual_x, actual_y = handler.scale_coordinates(
                960, 540, 
                1280, 720
            )
            # Returns: (640, 360) - proportionally scaled
        
        Use Case: Manually scale coordinates before clicking (for debugging/testing)
        
        Requirements: Accuracy within ±5px (SC-003)
        """
        raise NotImplementedError
    
    def get_absolute_screen_coords(
        self,
        window_x: int,
        window_y: int,
        window_handle: int
    ) -> Tuple[int, int]:
        """
        Convert window-relative coordinates to absolute screen coordinates.
        
        Args:
            window_x: X coordinate within window
            window_y: Y coordinate within window
            window_handle: Window handle for position lookup
        
        Returns:
            Tuple of (screen_x, screen_y) in absolute screen coordinates
        
        Example:
            # Click at (100, 100) within game window
            # Get absolute screen position for the click
            screen_x, screen_y = handler.get_absolute_screen_coords(
                100, 100, handle
            )
            # If window is at screen position (200, 150), returns (300, 250)
        
        Use Case: Internal conversion for sending click events
        """
        raise NotImplementedError
