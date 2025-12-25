# Data Model: Game Window Capture

**Feature**: 001-game-window-capture  
**Date**: 2025-12-25  
**Phase**: 1 (Design & Contracts)

## Overview

This document defines the core entities for window detection, capture, clicking, and OCR operations. All entities are designed for OpenCV/NumPy integration and Windows automation workflows.

---

## Entities

### 1. GameWindow

Represents a detected game window instance with all metadata needed for capture and interaction.

**Fields**:
- `handle: int` - Windows window handle (HWND) for all window operations
- `title: str` - Window title text (e.g., "Raid: Shadow Legends")
- `width: int` - Window content width in pixels
- `height: int` - Window content height in pixels
- `x: int` - Window position X coordinate (screen-relative, left edge)
- `y: int` - Window position Y coordinate (screen-relative, top edge)
- `state: WindowState` - Current window state (see WindowState enum below)
- `is_visible: bool` - Whether window is currently visible (not minimized to tray)
- `process_id: int` - Process ID of the window owner (for multi-instance tracking)

**Relationships**:
- Source for `WindowCapture` (one GameWindow → many captures over time)
- Target for `ClickTarget` execution (clicks sent to this window)

**Validation Rules**:
- `handle` must be valid Windows HWND (non-zero, verifiable via `win32gui.IsWindow()`)
- `width`, `height` must be positive integers
- `title` can be empty string (valid for some windows)
- `x`, `y` can be negative (multi-monitor setups with negative coordinates)

**State Transitions**:
```
NORMAL ↔ MINIMIZED (user minimizes/restores)
NORMAL ↔ MAXIMIZED (user maximizes/restores)
NORMAL/MINIMIZED/MAXIMIZED → CLOSED (window closes)
```

**Example**:
```python
GameWindow(
    handle=263458,
    title="Raid: Shadow Legends",
    width=1920,
    height=1080,
    x=100,
    y=50,
    state=WindowState.NORMAL,
    is_visible=True,
    process_id=12345
)
```

---

### 2. WindowState (Enum)

Enumeration of possible window states.

**Values**:
- `NORMAL = 0` - Standard windowed mode
- `MINIMIZED = 1` - Minimized to taskbar
- `MAXIMIZED = 2` - Maximized to full screen
- `CLOSED = 3` - Window no longer exists (detected during monitoring)

**Usage**:
```python
from enum import IntEnum

class WindowState(IntEnum):
    NORMAL = 0
    MINIMIZED = 1
    MAXIMIZED = 2
    CLOSED = 3
```

---

### 3. WindowCapture

Represents a captured screenshot of a game window at a specific moment.

**Fields**:
- `image: np.ndarray` - Image data as NumPy array (shape: [height, width, 3], dtype: uint8, format: BGR for OpenCV)
- `width: int` - Capture width in pixels (matches image.shape[1])
- `height: int` - Capture height in pixels (matches image.shape[0])
- `timestamp: datetime` - When the capture was taken (UTC)
- `window_handle: int` - Reference to source GameWindow handle
- `format: str` - Color format ("BGR", "RGB", or "GRAY")

**Relationships**:
- Belongs to `GameWindow` (many WindowCaptures → one GameWindow)
- Source for `TextRegion` detection (OCR processes this image)

**Validation Rules**:
- `image` shape must match `(height, width, 3)` for color or `(height, width)` for grayscale
- `width`, `height` must match image array dimensions
- `format` must be one of: "BGR", "RGB", "GRAY"
- `window_handle` must reference existing GameWindow at time of capture

**Example**:
```python
import numpy as np
from datetime import datetime

WindowCapture(
    image=np.array([...], dtype=np.uint8),  # BGR image array
    width=1920,
    height=1080,
    timestamp=datetime.utcnow(),
    window_handle=263458,
    format="BGR"
)
```

---

### 4. ClickTarget

Specifies where and how to execute a mouse click within a game window.

**Fields**:
- `x: int | float` - X coordinate (absolute pixels or relative 0.0-1.0 if coordinate_type is RELATIVE)
- `y: int | float` - Y coordinate (absolute pixels or relative 0.0-1.0 if coordinate_type is RELATIVE)
- `window_handle: int` - Target GameWindow handle for the click
- `coordinate_type: CoordinateType` - How to interpret x/y (see CoordinateType enum below)
- `click_type: ClickType` - Type of click to execute (LEFT, RIGHT, DOUBLE, see ClickType enum)
- `delay_ms: int` - Delay in milliseconds between mouse down and mouse up events (default: 50ms)

**Relationships**:
- Targets `GameWindow` (many ClickTargets → one GameWindow)
- Can be derived from `TextRegion` (click at center of detected text)

**Validation Rules**:
- If `coordinate_type == ABSOLUTE`: `x`, `y` must be integers ≥ 0
- If `coordinate_type == RELATIVE`: `x`, `y` must be floats in range [0.0, 1.0]
- If `coordinate_type == SCALED`: `x`, `y` are reference resolution pixels (integers), scaled at execution time
- `window_handle` must reference existing GameWindow
- `delay_ms` must be positive integer (typically 10-200ms for natural feel)

**Example (absolute coordinates)**:
```python
ClickTarget(
    x=960,
    y=540,
    window_handle=263458,
    coordinate_type=CoordinateType.ABSOLUTE,
    click_type=ClickType.LEFT,
    delay_ms=50
)
```

**Example (relative coordinates, center of window)**:
```python
ClickTarget(
    x=0.5,
    y=0.5,
    window_handle=263458,
    coordinate_type=CoordinateType.RELATIVE,
    click_type=ClickType.LEFT,
    delay_ms=50
)
```

**Example (scaled coordinates from 1920x1080 reference)**:
```python
ClickTarget(
    x=960,  # Center of 1920x1080 reference
    y=540,
    window_handle=263458,
    coordinate_type=CoordinateType.SCALED,
    click_type=ClickType.LEFT,
    delay_ms=50
)
# At runtime, if window is 1280x720, this becomes (640, 360)
```

---

### 5. CoordinateType (Enum)

Enumeration of coordinate interpretation modes.

**Values**:
- `ABSOLUTE = 0` - x/y are absolute pixel coordinates within the window
- `RELATIVE = 1` - x/y are percentages (0.0-1.0) of window width/height
- `SCALED = 2` - x/y are reference resolution pixels, scaled proportionally to actual window size

**Usage**:
```python
from enum import IntEnum

class CoordinateType(IntEnum):
    ABSOLUTE = 0
    RELATIVE = 1
    SCALED = 2
```

---

### 6. ClickType (Enum)

Enumeration of mouse click types.

**Values**:
- `LEFT = 0` - Left mouse button click
- `RIGHT = 1` - Right mouse button click
- `MIDDLE = 2` - Middle mouse button click
- `DOUBLE = 3` - Double-click (two rapid left clicks)

**Usage**:
```python
from enum import IntEnum

class ClickType(IntEnum):
    LEFT = 0
    RIGHT = 1
    MIDDLE = 2
    DOUBLE = 3
```

---

### 7. TextRegion

Represents detected text from OCR with location and confidence.

**Fields**:
- `text: str` - Detected text content (e.g., "BATTLE", "CLAIM", "Campaign")
- `x: int` - Bounding box top-left X coordinate (window-relative pixels)
- `y: int` - Bounding box top-left Y coordinate (window-relative pixels)
- `width: int` - Bounding box width in pixels
- `height: int` - Bounding box height in pixels
- `confidence: int` - OCR confidence score (0-100, higher is more confident)
- `capture_timestamp: datetime` - When the source capture was taken
- `window_handle: int` - Source GameWindow handle

**Relationships**:
- Derived from `WindowCapture` (many TextRegions → one WindowCapture)
- Can be converted to `ClickTarget` (click at center of text region)

**Validation Rules**:
- `text` must be non-empty string (empty results filtered out)
- `x`, `y`, `width`, `height` must be positive integers
- `confidence` must be in range [0, 100]
- `x + width` and `y + height` should be within source capture dimensions (but not strictly enforced; OCR can be imprecise)

**Derived Properties**:
- `center_x: int = x + width // 2` - Center X coordinate for clicking
- `center_y: int = y + height // 2` - Center Y coordinate for clicking
- `area: int = width * height` - Bounding box area (useful for filtering small detections)

**Example**:
```python
from datetime import datetime

TextRegion(
    text="BATTLE",
    x=850,
    y=920,
    width=220,
    height=80,
    confidence=92,
    capture_timestamp=datetime.utcnow(),
    window_handle=263458
)
```

---

## Entity Relationships Diagram

```
GameWindow (1) ──< WindowCapture (N)
    ↑                    ↓
    │              TextRegion (N)
    │                    ↓
    └──< ClickTarget (N) ←┘
         (can be derived from TextRegion or specified directly)
```

**Flow Example**:
1. Detect `GameWindow` by title → get window handle and dimensions
2. Capture `WindowCapture` from GameWindow → get image array
3. Run OCR on WindowCapture → extract `TextRegion` results
4. Create `ClickTarget` from TextRegion center coordinates
5. Execute click on ClickTarget → send mouse event to original GameWindow

---

## Validation Summary

| Entity | Critical Validation |
|--------|-------------------|
| GameWindow | handle exists, width/height > 0 |
| WindowCapture | image shape matches width/height, format valid |
| ClickTarget | coordinates valid for type, window exists |
| TextRegion | text non-empty, confidence 0-100, bbox within capture bounds |

---

## State Management

**Window State Monitoring**:
- GameWindow state transitions tracked via periodic polling (every 1s)
- State changes logged for debugging automation issues
- WindowCapture references may become stale if window resizes between capture and click

**Coordinate Staleness**:
- ClickTarget coordinates should be recalculated if window dimensions change between detection and execution
- Automation scripts should re-detect window dimensions before executing clicks if >5 seconds elapsed

**Error Handling**:
- Invalid window handle (window closed): raise `WindowNotFoundError`
- Capture timeout (>5s): raise `CaptureTimeoutError`
- OCR no results: return empty list (not an error; no text found)
- Click execution failure (window unresponsive): log warning, raise `ClickFailedError` if critical

---

Next: [contracts/](contracts/) directory for API function signatures and [quickstart.md](quickstart.md) for usage examples.
