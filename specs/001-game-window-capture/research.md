# Research: Game Window Capture

**Feature**: 001-game-window-capture  
**Date**: 2025-12-25  
**Phase**: 0 (Outline & Research)

## Research Tasks

This document consolidates research findings for all technical unknowns identified in the Technical Context section of [plan.md](plan.md).

---

## 1. Window Detection on Windows (pywin32 vs alternatives)

### Decision
Use **pywin32 (win32gui)** for window enumeration and handle management.

### Rationale
- Native Windows API access provides complete control over window enumeration, title matching, and handle retrieval
- Widely used in Python automation projects with extensive documentation and community support
- Supports all required operations: EnumWindows, GetWindowText, GetWindowRect, IsWindowVisible, GetWindowPlacement
- No additional dependencies beyond pywin32 (required for other Windows automation tasks anyway)
- Direct handle access enables precise window state queries and integration with screen capture/click automation

### Alternatives Considered
- **PyGetWindow**: Higher-level abstraction but limited control over window states and less mature ecosystem
- **ctypes with user32.dll**: More verbose than pywin32 wrapper, requires manual type definitions, error-prone
- **pywinauto**: Focused on UI automation (clicking controls) rather than raw window detection; overkill for basic enumeration

### Implementation Notes
```python
# Example: Enumerate windows and find by title pattern
import win32gui

def find_game_windows(title_pattern="Raid"):
    windows = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title_pattern.lower() in title.lower():
                rect = win32gui.GetWindowRect(hwnd)
                windows.append({
                    'handle': hwnd,
                    'title': title,
                    'rect': rect  # (left, top, right, bottom)
                })
    win32gui.EnumWindows(callback, None)
    return windows
```

---

## 2. Screen Capture Methods (mss vs win32ui vs PIL)

### Decision
Use **mss (Multiple Screen Shot)** for primary screen capture with **win32ui** as fallback for specific window capture.

### Rationale
- **mss**: Fast cross-platform screen capture (10+ FPS easily), returns NumPy-compatible arrays directly for OpenCV processing
- Optimized for performance with minimal overhead (C-based implementation)
- Supports region capture (x, y, width, height) for windowed capture via bounding box
- Returns images in RGB/BGR format directly compatible with OpenCV (cv2)
- **win32ui fallback**: For cases requiring true window-specific capture (ignoring overlays), use BitBlt with window DC
- Both methods tested and proven in automation communities

### Alternatives Considered
- **PIL/Pillow ImageGrab**: Python-based, slower than mss (5-8 FPS typical), requires conversion for OpenCV
- **win32ui only**: Windows-specific, more complex setup (DC, bitmap creation), but handles overlapping windows better
- **OpenCV VideoCapture**: Designed for camera/video files, not screen capture; requires DirectShow setup on Windows

### Implementation Notes
```python
import mss
import numpy as np

def capture_window(window_rect):
    """Capture window using mss based on bounding rectangle."""
    with mss.mss() as sct:
        monitor = {
            "top": window_rect[1],     # y
            "left": window_rect[0],    # x
            "width": window_rect[2] - window_rect[0],
            "height": window_rect[3] - window_rect[1]
        }
        screenshot = sct.grab(monitor)
        # Convert to NumPy array (BGR for OpenCV)
        img = np.array(screenshot)
        return img[:, :, :3]  # Drop alpha channel
```

**Performance Benchmark** (from community reports):
- mss: 10-30 FPS depending on resolution
- win32ui BitBlt: 8-15 FPS (slightly slower due to DC setup)
- PIL ImageGrab: 5-10 FPS

---

## 3. OCR Engine Selection (Tesseract vs Cloud APIs)

### Decision
Use **Tesseract OCR (pytesseract)** for local, offline text detection with configurable language packs.

### Rationale
- Free, open-source, offline (no API rate limits or costs)
- Good accuracy on clean UI text (buttons, labels) with proper preprocessing
- Supports multiple languages (English default, expandable for localized game versions)
- Returns bounding box coordinates with confidence scores (required for FR-010)
- Well-integrated with Python via pytesseract wrapper
- Acceptable latency (<200ms for typical UI region) with PSM (Page Segmentation Mode) tuning

### Alternatives Considered
- **Cloud OCR APIs (Google Vision, Azure OCR, AWS Textract)**: Higher accuracy but introduces network latency (100-500ms), API costs, requires internet, potential privacy concerns with game screenshots
- **EasyOCR**: Neural network-based, higher accuracy but slower (500ms-1s per region), requires PyTorch (large dependency)
- **PaddleOCR**: Similar to EasyOCR, good for complex text but overkill for clean game UI

### Configuration & Best Practices
```python
import pytesseract
from PIL import Image

def detect_text(image_array, roi=None):
    """Detect text in image using Tesseract with game UI optimizations."""
    # Preprocess: Convert to grayscale, threshold for better OCR
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # PSM 6: Assume uniform block of text (typical for UI buttons)
    # PSM 11: Sparse text (for scattered UI elements)
    config = '--psm 6 --oem 3'  # LSTM OCR Engine, uniform text block
    
    data = pytesseract.image_to_data(
        Image.fromarray(thresh), 
        config=config, 
        output_type=pytesseract.Output.DICT
    )
    
    # Filter by confidence threshold (>60% typical for UI text)
    results = []
    for i, conf in enumerate(data['conf']):
        if int(conf) > 60:
            results.append({
                'text': data['text'][i],
                'confidence': int(conf),
                'bbox': (data['left'][i], data['top'][i], 
                        data['width'][i], data['height'][i])
            })
    return results
```

**Accuracy Expectations**:
- Clean UI text (high contrast buttons): 95-98% accuracy
- Stylized text (gradients, shadows): 80-90% accuracy
- Small text (<12px): 70-80% accuracy (may require scaling)

---

## 4. Click Automation Method (PyAutoGUI vs win32api vs SendInput)

### Decision
Use **win32api + SendInput** for reliable, window-targeted click events with **PyAutoGUI** as convenience wrapper for simple cases.

### Rationale
- **win32api SendInput**: Low-level Windows input injection, works with background windows (if window accepts messages), precise control over mouse events
- More reliable than PyAutoGUI for automation scenarios (less interference from screen savers, focus changes)
- Can send clicks to specific window handles without requiring foreground focus (via PostMessage/SendMessage for certain controls)
- **PyAutoGUI** used for simple cases where foreground click is acceptable (easier API, cross-platform potential later)
- Enables future enhancements like drag-and-drop, right-click, hover

### Alternatives Considered
- **PyAutoGUI only**: Simpler API but requires window in foreground, less control over event timing, potential issues with UAC/admin windows
- **pywinauto**: Focused on UI control clicking (by control ID/class), not coordinate-based clicking; overkill for pixel-based automation
- **ctypes SendInput**: Possible but win32api provides cleaner wrapper

### Implementation Notes
```python
import win32api
import win32con
import time

def click_at_coords(x, y, window_handle=None):
    """Execute click at screen coordinates with optional window targeting."""
    # Option 1: Screen-based click (requires foreground)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.05)  # Small delay for natural feel
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    
    # Option 2: Message-based click (background window, if supported)
    # if window_handle:
    #     lParam = win32api.MAKELONG(rel_x, rel_y)
    #     win32api.PostMessage(window_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    #     win32api.PostMessage(window_handle, win32con.WM_LBUTTONUP, 0, lParam)
```

**Note**: Many games ignore PostMessage/SendMessage for anti-bot reasons. Fallback to foreground click (bring window to front, click, restore previous window) is the reliable approach.

---

## 5. Coordinate Translation for Resolution Independence

### Decision
Implement **proportional scaling** with reference resolution (1920x1080 baseline) and test at multiple window sizes.

### Rationale
- Game UI typically scales proportionally when window is resized (elements maintain relative positions)
- Simple formula: `actual_x = (reference_x / reference_width) * actual_width`
- Handles arbitrary window sizes without hardcoding multiple resolution mappings
- Allows automation scripts to define clicks in reference coordinates (easier to maintain)
- Template matching provides automatic tolerance for slight UI shifts; coordinate scaling handles size changes

### Implementation
```python
class CoordinateScaler:
    def __init__(self, reference_width=1920, reference_height=1080):
        self.ref_width = reference_width
        self.ref_height = reference_height
    
    def scale_coords(self, ref_x, ref_y, window_width, window_height):
        """Convert reference coordinates to actual window coordinates."""
        actual_x = int((ref_x / self.ref_width) * window_width)
        actual_y = int((ref_y / self.ref_height) * window_height)
        return (actual_x, actual_y)
    
    def scale_region(self, ref_bbox, window_width, window_height):
        """Scale bounding box (x, y, w, h) to actual window size."""
        x, y, w, h = ref_bbox
        actual_x = int((x / self.ref_width) * window_width)
        actual_y = int((y / self.ref_height) * window_height)
        actual_w = int((w / self.ref_width) * window_width)
        actual_h = int((h / self.ref_height) * window_height)
        return (actual_x, actual_y, actual_w, actual_h)
```

**Validation**: Test with window sizes: 1920x1080 (baseline), 1280x720 (720p), 1600x900, 2560x1440 (1440p). Verify clicks land within ±5px of intended UI element center.

---

## 6. Timeout Mechanism for Detection Operations

### Decision
Use **decorator-based timeout** with threading.Timer for all detection operations, default 5-second timeout.

### Rationale
- Prevents infinite loops when game window not found or OCR hangs
- Configurable per operation (quick detection vs thorough OCR scan)
- Graceful failure with exception (TimeoutError) for automation scripts to handle
- Thread-based timeout allows interruption of blocking operations (EnumWindows, OCR processing)

### Implementation
```python
import functools
import threading

class TimeoutError(Exception):
    pass

def timeout(seconds=5):
    """Decorator to add timeout to any function."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout=seconds)
            
            if thread.is_alive():
                raise TimeoutError(f"{func.__name__} exceeded {seconds}s timeout")
            if exception[0]:
                raise exception[0]
            return result[0]
        
        return wrapper
    return decorator

# Usage
@timeout(seconds=5)
def find_game_window():
    # Window enumeration logic
    pass
```

---

## 7. Logging Strategy for Window Operations

### Decision
Use Python **logging module** with structured JSON output and configurable verbosity levels.

### Rationale
- Standard library solution, no additional dependencies
- Structured format enables parsing for analytics/debugging
- Different log levels (DEBUG, INFO, WARNING, ERROR) for filtering
- File + console output for both real-time monitoring and historical analysis
- Includes timestamps, operation names, coordinates, success/failure, duration

### Configuration
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name="rsl_automation", log_file="automation.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # File handler (JSON structured logs)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        
        # Console handler (human-readable)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def log_operation(self, operation, status, details=None, duration=None):
        """Log window operation with structured data."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": status,  # "success" | "failure"
            "details": details or {},
            "duration_ms": duration
        }
        
        if status == "success":
            self.logger.info(json.dumps(log_entry))
        else:
            self.logger.error(json.dumps(log_entry))
```

**Example Log Entries**:
```json
{"timestamp": "2025-12-25T10:30:45.123", "operation": "window_detection", "status": "success", "details": {"title": "Raid: Shadow Legends", "handle": 12345, "rect": [100, 100, 2020, 1180]}, "duration_ms": 120}
{"timestamp": "2025-12-25T10:30:50.456", "operation": "screen_capture", "status": "success", "details": {"size": [1920, 1080]}, "duration_ms": 85}
{"timestamp": "2025-12-25T10:31:00.789", "operation": "ocr_detection", "status": "failure", "details": {"error": "No text found with confidence >60%"}, "duration_ms": 350}
```

---

## Summary

All technical unknowns from the Technical Context section have been resolved:

✅ **Window Detection**: pywin32 (win32gui) for native Windows API access  
✅ **Screen Capture**: mss for fast multi-screen support, win32ui as fallback  
✅ **OCR Engine**: Tesseract (pytesseract) for offline, free text detection  
✅ **Click Automation**: win32api SendInput with PyAutoGUI convenience wrapper  
✅ **Coordinate Scaling**: Proportional scaling from 1920x1080 reference resolution  
✅ **Timeout Mechanism**: Decorator-based threading.Timer approach  
✅ **Logging**: Python logging module with JSON structured output

Next phase: [data-model.md](data-model.md) to define entities and [contracts/](contracts/) for API specifications.
