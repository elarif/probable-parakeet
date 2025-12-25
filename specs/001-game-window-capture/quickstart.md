# Quickstart Guide: Game Window Capture

**Feature**: 001-game-window-capture  
**Date**: 2025-12-25  
**Audience**: Developers integrating window capture into automation scripts

## Overview

This guide demonstrates how to use the window detection, capture, OCR, and click automation APIs for Raid Shadow Legends automation. All examples assume the game is running on Windows.

---

## Prerequisites

1. **Install Dependencies**:
   ```powershell
   pip install opencv-python pytesseract pillow mss pywin32 pyautogui numpy
   ```

2. **Install Tesseract OCR**:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Add Tesseract to PATH or configure `pytesseract.pytesseract.tesseract_cmd`

3. **Game Running**: Launch Raid Shadow Legends before running automation scripts

---

## Basic Usage Examples

### 1. Detect Game Window

```python
from src.vision.window_detector import WindowDetector

# Initialize detector
detector = WindowDetector()

# Find all Raid Shadow Legends windows
windows = detector.find_windows_by_title("Raid")

if windows:
    game_window = windows[0]  # Use first match
    print(f"Found game: {game_window.title}")
    print(f"Size: {game_window.width}x{game_window.height}")
    print(f"Position: ({game_window.x}, {game_window.y})")
else:
    print("Game not found - is it running?")
```

**Output Example**:
```
Found game: Raid: Shadow Legends
Size: 1920x1080
Position: (100, 50)
```

---

### 2. Capture Window Screenshot

```python
from src.vision.screen_capture import ScreenCapture
import cv2

# Initialize capture
capturer = ScreenCapture()

# Detect window first
detector = WindowDetector()
windows = detector.find_windows_by_title("Raid")
game_window = windows[0]

# Capture current game state
capture = capturer.capture_window(game_window.handle)

print(f"Captured {capture.width}x{capture.height} image")
print(f"Timestamp: {capture.timestamp}")

# Display capture (for debugging)
cv2.imshow("Game Capture", capture.image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save for debugging
capturer.capture_window_to_file(game_window.handle, "debug_capture.png")
```

---

### 3. Detect Text with OCR

```python
from src.vision.ocr_engine import OCREngine

# Initialize OCR (min confidence 70% for game UI)
ocr = OCREngine(min_confidence=70, language="eng", psm_mode=6)

# Capture window
capture = capturer.capture_window(game_window.handle)

# Detect all text
text_regions = ocr.detect_text(capture.image, game_window.handle)

print(f"Found {len(text_regions)} text regions:")
for region in text_regions:
    print(f"  '{region.text}' at ({region.x}, {region.y}) - confidence: {region.confidence}%")
```

**Output Example**:
```
Found 12 text regions:
  'BATTLE' at (850, 920) - confidence: 92%
  'CAMPAIGN' at (120, 150) - confidence: 88%
  'ARENA' at (120, 250) - confidence: 95%
  'CLAN' at (120, 350) - confidence: 91%
```

---

### 4. Find Specific Text (e.g., BATTLE button)

```python
# Find "BATTLE" button
battle_button = ocr.find_text(capture.image, "BATTLE", game_window.handle)

if battle_button:
    print(f"BATTLE button found at ({battle_button.center_x}, {battle_button.center_y})")
    print(f"Confidence: {battle_button.confidence}%")
else:
    print("BATTLE button not found")
```

---

### 5. Click at Specific Coordinates

```python
from src.automation.click_handler import ClickHandler
from contracts.click_api import ClickType, CoordinateType

# Initialize click handler (1920x1080 reference resolution)
click_handler = ClickHandler(reference_width=1920, reference_height=1080)

# Method 1: Click at absolute coordinates
click_handler.click_at(
    x=960, y=540,  # Center of 1920x1080 window
    window_handle=game_window.handle,
    coordinate_type=CoordinateType.ABSOLUTE,
    click_type=ClickType.LEFT
)

# Method 2: Click at relative coordinates (50% = center)
click_handler.click_at(
    x=0.5, y=0.5,  # Center of window (any size)
    window_handle=game_window.handle,
    coordinate_type=CoordinateType.RELATIVE,
    click_type=ClickType.LEFT
)

# Method 3: Click using scaled coordinates (resolution-independent)
# Click at (960, 540) in 1920x1080 reference, auto-scales to actual window size
click_handler.click_at(
    x=960, y=540,
    window_handle=game_window.handle,
    coordinate_type=CoordinateType.SCALED,
    click_type=ClickType.LEFT
)
```

---

### 6. Click on Detected Text

```python
# Find button by text and click it
battle_button = ocr.find_text(capture.image, "BATTLE", game_window.handle)

if battle_button:
    # Click at center of detected text region
    click_handler.click_at(
        x=battle_button.center_x,
        y=battle_button.center_y,
        window_handle=game_window.handle,
        coordinate_type=CoordinateType.ABSOLUTE
    )
    print("Clicked BATTLE button")
else:
    print("BATTLE button not visible")
```

---

### 7. Complete Workflow: Detect → Capture → Find → Click

```python
from src.vision.window_detector import WindowDetector
from src.vision.screen_capture import ScreenCapture
from src.vision.ocr_engine import OCREngine
from src.automation.click_handler import ClickHandler
from contracts.click_api import CoordinateType
import time

# 1. Detect game window
detector = WindowDetector()
windows = detector.find_windows_by_title("Raid")
if not windows:
    raise RuntimeError("Game not running")
game_window = windows[0]
print(f"Found game: {game_window.title} ({game_window.width}x{game_window.height})")

# 2. Initialize tools
capturer = ScreenCapture()
ocr = OCREngine(min_confidence=70)
click_handler = ClickHandler()

# 3. Capture current screen
capture = capturer.capture_window(game_window.handle)
print("Captured game screen")

# 4. Find "BATTLE" button via OCR
battle_button = ocr.find_text(capture.image, "BATTLE", game_window.handle)

if battle_button:
    # 5. Click the button
    click_handler.click_at(
        x=battle_button.center_x,
        y=battle_button.center_y,
        window_handle=game_window.handle,
        coordinate_type=CoordinateType.ABSOLUTE
    )
    print(f"Clicked BATTLE at ({battle_button.center_x}, {battle_button.center_y})")
    
    # Wait for battle to load
    time.sleep(2)
    
    # Verify state change (optional)
    new_capture = capturer.capture_window(game_window.handle)
    battle_check = ocr.find_text(new_capture.image, "BATTLE", game_window.handle)
    if not battle_check:
        print("State changed - battle started successfully")
    else:
        print("Warning: Still on same screen")
else:
    print("BATTLE button not found - different game screen?")
```

---

## Advanced Examples

### Handle Window Resizing

```python
# Initial detection
windows = detector.find_windows_by_title("Raid")
game_window = windows[0]

# ... user resizes window ...

# Refresh window info before clicking
updated_window = detector.refresh_window_info(game_window.handle)
print(f"Window resized to {updated_window.width}x{updated_window.height}")

# Scaled coordinates automatically adjust
click_handler.click_at(
    x=960, y=540,  # Reference 1920x1080
    window_handle=updated_window.handle,
    coordinate_type=CoordinateType.SCALED  # Auto-scales to actual size
)
```

---

### Capture Specific Region for OCR (Performance Optimization)

```python
# Only capture bottom 20% of screen (where buttons typically are)
window_height = game_window.height
roi_capture = capturer.capture_region(
    window_handle=game_window.handle,
    x=0,
    y=int(window_height * 0.8),
    width=game_window.width,
    height=int(window_height * 0.2)
)

# OCR on smaller region (faster)
buttons = ocr.detect_text(roi_capture.image, game_window.handle)
print(f"Found {len(buttons)} buttons in bottom region")
```

---

### Monitor Window State Changes

```python
from src.automation.window_monitor import WindowMonitor
from contracts.window_api import WindowState

def on_state_change(old_state, new_state, window):
    print(f"Window state: {old_state} → {new_state}")
    if new_state == WindowState.CLOSED:
        print("Game closed - stopping automation")
        # Trigger shutdown logic
    elif new_state == WindowState.MINIMIZED:
        print("Game minimized - pausing automation")

monitor = WindowMonitor()
monitor.start_monitoring(
    game_window.handle,
    poll_interval_seconds=1.0,
    on_state_change=on_state_change
)

# Automation runs in main thread
# Monitor runs in background, calls callback on changes
```

---

### Multiple Game Instances

```python
# Detect all running game instances
all_game_windows = detector.find_windows_by_title("Raid")
print(f"Found {len(all_game_windows)} game instances")

for i, window in enumerate(all_game_windows):
    print(f"Instance {i+1}: {window.title} (PID: {window.process_id})")
    
    # Automate each instance separately
    capture = capturer.capture_window(window.handle)
    # ... process each window ...
```

---

### Error Handling

```python
from contracts.window_api import WindowNotFoundError
from contracts.capture_api import CaptureTimeoutError
from contracts.click_api import ClickFailedError

try:
    # Detect window
    windows = detector.find_windows_by_title("Raid", timeout_seconds=5)
    if not windows:
        raise RuntimeError("Game not found within timeout")
    
    game_window = windows[0]
    
    # Capture with timeout
    capture = capturer.capture_window(game_window.handle, timeout_seconds=3)
    
    # Click with validation
    battle_button = ocr.find_text(capture.image, "BATTLE", game_window.handle)
    if battle_button:
        click_handler.click_at(
            battle_button.center_x, 
            battle_button.center_y,
            game_window.handle
        )
    else:
        print("Button not visible - wrong screen?")
        
except CaptureTimeoutError:
    print("Screen capture timed out - game frozen?")
except ClickFailedError:
    print("Click failed - window became invalid?")
except WindowNotFoundError:
    print("Window closed during operation")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Performance Tips

1. **Use ROI for OCR**: Limit OCR to specific screen regions instead of full window
2. **Adjust Confidence Threshold**: Lower for stylized text, higher for clean UI
3. **Cache Window Handle**: Don't re-detect window every frame if it doesn't change
4. **Preprocess Images**: Use `ocr.preprocess_for_ocr()` for difficult text
5. **Batch Operations**: Capture once, run multiple OCR searches on same image

---

## Common Patterns

### Pattern: Wait for Specific Text (Loading Screen)

```python
import time

def wait_for_text(text, timeout=10):
    """Wait until specific text appears on screen."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        capture = capturer.capture_window(game_window.handle)
        if ocr.find_text(capture.image, text, game_window.handle):
            return True
        time.sleep(0.5)
    return False

# Wait for battle to start (loading complete)
if wait_for_text("AUTO", timeout=15):
    print("Battle loaded - AUTO button visible")
    # Click AUTO button
else:
    print("Battle load timeout")
```

---

### Pattern: Click Until Text Disappears

```python
def click_until_gone(button_text, max_clicks=10):
    """Click a button repeatedly until it's no longer visible."""
    for i in range(max_clicks):
        capture = capturer.capture_window(game_window.handle)
        button = ocr.find_text(capture.image, button_text, game_window.handle)
        
        if not button:
            print(f"'{button_text}' disappeared after {i} clicks")
            return True
        
        click_handler.click_at(
            button.center_x, button.center_y,
            game_window.handle
        )
        time.sleep(0.5)
    
    print(f"'{button_text}' still visible after {max_clicks} clicks")
    return False

# Example: Claim multiple rewards
click_until_gone("CLAIM", max_clicks=5)
```

---

## Next Steps

- See [data-model.md](data-model.md) for entity details
- See [contracts/](contracts/) for complete API reference
- See [plan.md](plan.md) for architecture and design decisions
- See [tasks.md](tasks.md) for implementation task breakdown (created by `/speckit.tasks` command)

---

**Last Updated**: 2025-12-25
