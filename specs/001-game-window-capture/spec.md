# Feature Specification: Game Window Capture

**Feature Branch**: `001-game-window-capture`  
**Created**: 2025-12-25  
**Status**: Draft  
**Input**: User description: "Detect game window by name, capture window content, and click at specific locations. Must work regardless of window size and support text detection even when window is not maximized"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Window Detection (Priority: P1)

Automation users need to detect when Raid Shadow Legends is running by identifying the game window, regardless of whether it's minimized, in the background, or running in a specific display mode.

**Why this priority**: Window detection is the absolute foundation - without reliably finding the game window, no automation or capture can occur. This is the entry point for all other functionality.

**Independent Test**: Can be fully tested by launching the game in various states (normal, minimized, background, different positions) and verifying the window is correctly identified by its title. Delivers immediate value by answering "Is the game running?"

**Acceptance Scenarios**:

1. **Given** the game is running in normal window mode, **When** the detection runs, **Then** the game window is identified with its handle and title
2. **Given** the game is minimized to taskbar, **When** the detection runs, **Then** the game window is still identified correctly
3. **Given** the game is behind other windows, **When** the detection runs, **Then** the game window is identified without requiring it to be in foreground
4. **Given** the game is not running, **When** the detection runs, **Then** the system reports no game window found (not an error, expected state)
5. **Given** multiple game client instances are running, **When** the detection runs, **Then** all game windows are identified and enumerated

---

### User Story 2 - Window Content Capture (Priority: P2)

Automation users need to capture the current visual state of the game window as an image for template matching and OCR processing, working correctly regardless of window size or screen position.

**Why this priority**: Capturing window content is required for vision-based detection (templates, OCR, state analysis). This enables reading game state without manual inspection.

**Independent Test**: Can be tested independently by capturing screenshots of the game window at different sizes/positions and verifying the captured images contain the correct game content with proper dimensions and quality.

**Acceptance Scenarios**:

1. **Given** the game window is at default size (e.g., 1920x1080), **When** a capture is requested, **Then** a complete screenshot of the game content is returned
2. **Given** the game window is resized to a smaller dimension (e.g., 1280x720), **When** a capture is requested, **Then** the screenshot matches the actual window content with correct proportions
3. **Given** the game window is on a secondary monitor, **When** a capture is requested, **Then** the screenshot captures the correct monitor's content
4. **Given** the game window is partially obscured by another window, **When** a capture is requested, **Then** the screenshot contains the game window's content (may include overlapping window depending on capture method)
5. **Given** the game is displaying a loading screen, **When** multiple captures are taken 1 second apart, **Then** each capture reflects the current visual state at that moment

---

### User Story 3 - Coordinate-Based Clicking (Priority: P3)

Automation users need to programmatically click at specific locations within the game window, with coordinates that automatically scale/adapt to different window sizes while maintaining accuracy.

**Why this priority**: Clicking is the primary interaction method for automation. This enables executing game actions after detecting UI elements. Position-independent clicking ensures automation works across different resolutions and window sizes.

**Independent Test**: Can be tested by defining test points (e.g., "top-left corner", "center", "75% right, 50% down") and verifying clicks land at the correct locations in windows of different sizes. Can use a test overlay or debug mode to visualize click points.

**Acceptance Scenarios**:

1. **Given** a click target at relative position (50%, 50%) in a 1920x1080 window, **When** the click is executed, **Then** the click occurs at pixel (960, 540) within the game window
2. **Given** the same relative position (50%, 50%) in a resized 1280x720 window, **When** the click is executed, **Then** the click occurs at pixel (640, 360) maintaining center position
3. **Given** a click target specified as absolute pixels within a reference resolution, **When** the click is executed in a different window size, **Then** the coordinates are scaled proportionally to match the same UI element
4. **Given** the game window is moved to a different screen position, **When** a click is executed, **Then** the click occurs at the correct location within the window (not affected by window position on screen)
5. **Given** multiple rapid clicks are queued (e.g., 5 clicks in sequence), **When** executed, **Then** all clicks occur at their intended coordinates with appropriate timing delays

---

### User Story 4 - Text Detection & Clickable Elements (Priority: P3)

Automation users need to locate and click on text-based UI elements (buttons with text, menu items, labels) using OCR, working correctly regardless of window size or maximization state.

**Why this priority**: Many game UI elements are text-based (button labels, menus, champion names). OCR-based detection provides resilience to UI updates that change button graphics but preserve text. This is complementary to template matching.

**Independent Test**: Can be tested by providing sample screenshots with known text elements (e.g., "BATTLE" button, "CLAIM" button) at different window sizes and verifying the text is detected with correct bounding box coordinates.

**Acceptance Scenarios**:

1. **Given** a button with text "BATTLE" visible in a maximized game window, **When** text detection runs, **Then** the text is found with its bounding box coordinates
2. **Given** the same "BATTLE" button in a non-maximized 1280x720 window, **When** text detection runs, **Then** the text is found with correctly scaled coordinates relative to the smaller window
3. **Given** a UI element with text at 75% window width and 40% height, **When** text-based click is requested, **Then** the click occurs at the center of the detected text region
4. **Given** multiple text elements on screen (e.g., "BATTLE", "CLAIM", "CANCEL"), **When** detection runs for specific text "CLAIM", **Then** only the matching text element is identified and returned
5. **Given** text with slight visual variations (anti-aliasing differences due to window scaling), **When** OCR runs, **Then** the text is still recognized correctly (tolerance for minor rendering differences)

---

### Edge Cases

- **Window state changes**: What happens when the game window is minimized or brought to foreground during capture/click operations?
- **Multiple monitors**: How does the system handle game window detection and capture across multi-monitor setups?
- **Window resizing mid-operation**: If the window is resized between detection and click execution, how are stale coordinates handled?
- **Missing game window**: If the game crashes or closes during automation, how does the system detect and report this?
- **Overlapping windows**: When another window partially covers the game, do captures include the overlay or only the game content?
- **DPI scaling**: On high-DPI displays (4K, retina), are window dimensions and click coordinates correctly adjusted?
- **Permission errors**: If the system lacks permissions to capture or send clicks to the game window, how is this reported?
- **OCR failures**: When text is stylized, rotated, or in non-standard fonts, what happens if OCR cannot detect it?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST detect Raid Shadow Legends game window by matching window title pattern (e.g., contains "Raid" or "Shadow Legends")
- **FR-002**: System MUST return window handle, title, dimensions (width, height), and position (x, y) for detected game windows
- **FR-003**: System MUST support detection of multiple game instances simultaneously and return all matching windows
- **FR-004**: System MUST capture the visible content of the game window as an image (bitmap/array format suitable for OpenCV processing)
- **FR-005**: System MUST capture window content regardless of window size, position, or monitor location
- **FR-006**: System MUST execute clicks at specified coordinates within the game window coordinate space (relative or absolute)
- **FR-007**: System MUST translate click coordinates from reference resolution to actual window size (coordinate scaling)
- **FR-008**: System SHOULD support sending click events to game window when not in foreground (background clicking); MUST implement foreground focus fallback when background clicking unavailable
- **FR-009**: System MUST detect text within captured window images using OCR
- **FR-010**: System MUST return bounding box coordinates (x, y, width, height) for each detected text region
- **FR-011**: System MUST support clicking at the center or specific position of detected text regions
- **FR-012**: System MUST handle window state changes gracefully (detect when window is closed, minimized, or becomes unavailable)
- **FR-013**: System MUST work on Windows 10/11 operating systems (primary platform for game automation)
- **FR-014**: System MUST provide timeout mechanism for detection operations (avoid infinite waits if game not found)
- **FR-015**: System MUST log all window operations (detection, capture, clicks) with timestamps and success/failure status

### Key Entities

- **GameWindow**: Represents a detected game window with handle, title, dimensions (width, height), position (x, y), and state (minimized, normal, maximized)
- **WindowCapture**: Image data captured from a game window with dimensions, format (BGR/RGB array), timestamp, and source window reference
- **ClickTarget**: Coordinate specification with x, y position (absolute or relative), target window reference, and coordinate type (absolute pixels, relative percentage, or text-based)
- **TextRegion**: Detected text with content string, bounding box (x, y, width, height), confidence score, and source capture reference

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Game window detection completes in under 500ms and correctly identifies the window in 100% of cases when game is running
- **SC-002**: Window capture operates at minimum 10 FPS (100ms per capture) for continuous monitoring scenarios
- **SC-003**: Click coordinate translation maintains accuracy within ±5 pixels for SCALED coordinate type across window sizes from 800x600 to 2560x1440 (ABSOLUTE and RELATIVE coordinates are pixel-perfect by definition)
- **SC-004**: OCR text detection achieves 95% accuracy on standard game UI text (buttons, menus, labels) across different window sizes
- **SC-005**: System detects and reports window state changes (closed, minimized) within 1 second of occurrence
- **SC-006**: Automation scripts can reliably perform "detect → capture → analyze → click" workflows without manual window manipulation
- **SC-007**: Multi-monitor setups correctly identify and capture game window regardless of which monitor it's displayed on

## Assumptions

- **Window Title Pattern**: The game window title contains identifiable text such as "Raid: Shadow Legends" or similar consistent pattern across game versions
- **OCR Language**: Game text is primarily English (default OCR configuration; multi-language support can be added later)
- **Capture Method**: Using Windows API (win32gui, win32ui) or cross-platform libraries (mss) for screen capture
- **Click Method**: Using PyAutoGUI, win32api, or similar for sending click events
- **Coordinate System**: Standard top-left origin (0,0) with x increasing right, y increasing down
- **Permissions**: User running automation has necessary Windows permissions to enumerate windows, capture screen content, and send input events
- **Performance**: Target system has sufficient CPU/memory for real-time capture and OCR without impacting game performance

## Dependencies

- **External Tools**: OCR engine (Tesseract) or cloud OCR API for text detection
- **Libraries**: Window management (win32gui), screen capture (mss, PIL), click automation (PyAutoGUI, win32api)
- **Game Client**: Raid Shadow Legends PC client installed and operational
