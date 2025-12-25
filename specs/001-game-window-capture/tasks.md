# Tasks: Game Window Capture

**Input**: Design documents from `/specs/001-game-window-capture/`
**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/)

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are EXCLUDED from this breakdown.

**Vision-First Workflow**: This feature follows the constitution's vision-first principle:
1. Detection/capture infrastructure first (no automation)
2. Entity models and data structures
3. Click primitives (without randomization/jitter - that's for higher-level features)
4. OCR detection capabilities
5. Integration and observability

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- File paths follow single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Python automation structure

- [ ] T001 Create project directory structure: src/{models,vision,automation,utils}, tests/{unit,integration,fixtures}, assets/{templates,screenshots}
- [ ] T002 Initialize Python project with requirements.txt (opencv-python, pytesseract, pillow, mss, pywin32, pyautogui, numpy, pytest)
- [ ] T003 [P] Create README.md with Tesseract installation instructions and project overview
- [ ] T004 [P] Configure .gitignore for Python (venv/, __pycache__/, *.pyc, assets/screenshots/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core entities and utilities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Implement WindowState enum in src/models/game_window.py
- [ ] T006 [P] Implement GameWindow entity in src/models/game_window.py
- [ ] T007 [P] Implement WindowCapture entity in src/models/window_capture.py
- [ ] T008 [P] Implement CoordinateType enum in src/models/click_target.py
- [ ] T009 [P] Implement ClickType enum in src/models/click_target.py
- [ ] T010 [P] Implement ClickTarget entity in src/models/click_target.py
- [ ] T011 [P] Implement TextRegion entity in src/models/text_region.py
- [ ] T012 [P] Create custom exceptions (WindowNotFoundError, CaptureTimeoutError, etc.) in src/utils/exceptions.py
- [ ] T013 [P] Implement timeout decorator in src/utils/timing.py
- [ ] T014 [P] Implement StructuredLogger in src/utils/logger.py with JSON output format

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Window Detection (Priority: P1) 🎯 MVP

**Goal**: Detect Raid Shadow Legends game window by title, regardless of window state (minimized, background, foreground)

**Independent Test**: Launch game in various states (normal, minimized, background) and verify window is detected with correct handle, title, and dimensions. Test returns empty list when game not running.

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement find_windows_by_title() method in src/vision/window_detector.py using win32gui.EnumWindows
- [ ] T016 [P] [US1] Implement get_window_by_handle() method in src/vision/window_detector.py using win32gui.GetWindowText and GetWindowRect
- [ ] T017 [P] [US1] Implement get_window_state() method in src/vision/window_detector.py using win32gui.GetWindowPlacement
- [ ] T018 [P] [US1] Implement is_window_valid() method in src/vision/window_detector.py using win32gui.IsWindow
- [ ] T019 [US1] Implement refresh_window_info() method in src/vision/window_detector.py to update GameWindow dimensions
- [ ] T020 [US1] Add timeout guards to all detection methods using timeout decorator from T013
- [ ] T021 [US1] Add structured logging for window detection operations (found/not found, handle, dimensions)
- [ ] T022 [US1] Create test fixtures in tests/fixtures/ with mock window handles for unit testing

**Checkpoint**: Window detection complete - can detect game window in all states with proper timeout and logging

---

## Phase 4: User Story 2 - Window Content Capture (Priority: P2)

**Goal**: Capture visual state of game window as image for template matching and OCR, working at different window sizes and screen positions

**Independent Test**: Capture screenshots of game at different sizes (1920x1080, 1280x720) and positions (primary monitor, secondary monitor, different screen locations). Verify captured images match actual window content with correct dimensions.

### Implementation for User Story 2

- [ ] T023 [P] [US2] Implement capture_window() method in src/vision/screen_capture.py using mss to capture by window rectangle
- [ ] T024 [P] [US2] Implement capture_region() method in src/vision/screen_capture.py for ROI-based capture
- [ ] T025 [P] [US2] Implement capture_window_to_file() method in src/vision/screen_capture.py for debug screenshot saving
- [ ] T026 [US2] Add timeout guards to capture methods (default 5 seconds, configurable)
- [ ] T027 [US2] Implement color format conversion (BGR/RGB/GRAY) in capture methods
- [ ] T028 [US2] Add WindowCapture entity creation with timestamp and metadata
- [ ] T029 [US2] Implement get_capture_fps() method for performance benchmarking
- [ ] T030 [US2] Add structured logging for capture operations (size, duration, format)
- [ ] T031 [US2] Create test fixtures in tests/fixtures/screenshots/ with reference captures at different resolutions

**Checkpoint**: Screen capture complete - can capture full window or regions at any size with performance tracking

---

## Phase 5: User Story 3 - Coordinate-Based Clicking (Priority: P3)

**Goal**: Execute clicks at specific window coordinates with automatic scaling for different window sizes

**Independent Test**: Define test points (center, corners, 25%/75% positions) and verify clicks land correctly in windows of different sizes. Use debug overlay or coordinate logging to validate accuracy within ±5px.

### Implementation for User Story 3

- [ ] T032 [P] [US3] Implement scale_coordinates() method in src/vision/coordinate_scaler.py for reference→actual coordinate translation
- [ ] T033 [P] [US3] Implement get_absolute_screen_coords() method in src/automation/click_handler.py to convert window-relative to screen coordinates
- [ ] T034 [US3] Implement click() method in src/automation/click_handler.py using win32api.SetCursorPos and mouse_event
- [ ] T035 [US3] Implement click_at() convenience method in src/automation/click_handler.py for all coordinate types (ABSOLUTE, RELATIVE, SCALED)
- [ ] T036 [US3] Implement double_click_at() convenience method in src/automation/click_handler.py
- [ ] T037 [US3] Add bring_to_foreground logic using win32gui.SetForegroundWindow before clicks
- [ ] T038 [US3] Add coordinate validation (bounds checking, type checking for ABSOLUTE vs RELATIVE)
- [ ] T039 [US3] Implement configurable delay_ms between mouse down/up events
- [ ] T040 [US3] Add structured logging for click operations (coordinates, type, window handle, success/failure)
- [ ] T041 [US3] Create integration test in tests/integration/test_detection_capture_click_flow.py combining window detection, coordinate scaling, and click execution

**Checkpoint**: Click automation complete - can click at any coordinate type with proper scaling and logging

---

## Phase 6: User Story 4 - Text Detection & Clickable Elements (Priority: P3)

**Goal**: Locate text-based UI elements using OCR and enable clicking on detected text, working at different window sizes

**Independent Test**: Provide sample screenshots with known buttons ("BATTLE", "CLAIM", "CAMPAIGN") at different window sizes. Verify text is detected with correct bounding boxes and confidence scores ≥70%.

### Implementation for User Story 4

- [ ] T042 [P] [US4] Implement OCREngine initialization in src/vision/ocr_engine.py with pytesseract configuration (PSM mode, language, min_confidence)
- [ ] T043 [P] [US4] Implement preprocess_for_ocr() method in src/vision/ocr_engine.py (grayscale conversion, thresholding, denoising)
- [ ] T044 [US4] Implement detect_text() method in src/vision/ocr_engine.py using pytesseract.image_to_data with bounding box extraction
- [ ] T045 [US4] Implement find_text() method in src/vision/ocr_engine.py for single text search (exact or substring match)
- [ ] T046 [US4] Implement find_all_text() method in src/vision/ocr_engine.py for finding all occurrences of text
- [ ] T047 [US4] Add ROI parameter support to all OCR methods for region-limited text detection
- [ ] T048 [US4] Implement set_confidence_threshold() method to dynamically adjust OCR sensitivity
- [ ] T049 [US4] Add timeout guards to all OCR operations (default 5 seconds)
- [ ] T050 [US4] Add TextRegion entity creation with center_x, center_y properties for clicking
- [ ] T051 [US4] Add structured logging for OCR operations (text found, confidence, bounding box, duration)
- [ ] T052 [US4] Create test fixtures in tests/fixtures/screenshots/ with labeled game UI screenshots for OCR validation
- [ ] T053 [US4] Create integration test in tests/integration/test_capture_ocr_click_flow.py combining capture, OCR, and clicking on detected text

**Checkpoint**: OCR complete - can detect text in game UI and click on detected elements

---

## Phase 7: Window State Monitoring (Cross-Cutting)

**Purpose**: Monitor window state changes for graceful failure detection (supports all user stories)

- [ ] T054 [P] Implement start_monitoring() method in src/automation/window_monitor.py using background thread polling
- [ ] T055 [P] Implement stop_monitoring() method in src/automation/window_monitor.py
- [ ] T056 Add state change callback mechanism in src/automation/window_monitor.py for NORMAL/MINIMIZED/MAXIMIZED/CLOSED transitions
- [ ] T057 Add structured logging for window state changes (old state → new state, timestamp)
- [ ] T058 Create example usage in README.md for monitoring game closure during automation

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and observability improvements

- [ ] T059 [P] Create comprehensive examples in README.md covering all 4 user stories with code snippets
- [ ] T060 [P] Validate quickstart.md examples against implemented API (ensure all imports and methods exist)
- [ ] T061 Add type hints to all public methods in src/ modules
- [ ] T062 [P] Create accuracy validation script in tests/validate_accuracy.py to test SC-001 through SC-007 success criteria
- [ ] T063 Document Tesseract installation and PATH configuration in README.md
- [ ] T064 [P] Add docstrings to all public classes and methods following contracts/ format
- [ ] T065 Create example automation script in examples/detect_and_click_battle.py demonstrating full workflow
- [ ] T066 Add performance benchmarking script in tests/benchmark_performance.py for FPS and latency validation
- [ ] T067 [P] Validate compatibility on Windows 10 and Windows 11 systems (FR-013 verification)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational (Phase 2) completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order: US1 → US2 → US3 → US4
- **Window Monitoring (Phase 7)**: Can start after Foundational (Phase 2), runs in parallel with user stories
- **Polish (Phase 8)**: Depends on all user stories (Phases 3-6) being complete

### User Story Dependencies

- **User Story 1 (P1 - Window Detection)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2 - Content Capture)**: Can start after Foundational - Requires US1 for window handles but is independently testable
- **User Story 3 (P3 - Clicking)**: Can start after Foundational - Requires US1 for window handles, uses coordinate scaling independently
- **User Story 4 (P3 - OCR)**: Can start after Foundational - Requires US2 for captures, but can be tested with fixture images independently

### Within Each User Story

**User Story 1**: All tasks T015-T018 can run in parallel (different methods), T019 depends on T015-T018, T020-T022 can run in parallel after core implementation

**User Story 2**: T023-T025 can run in parallel (different methods), T026-T031 sequential after core methods

**User Story 3**: T032-T033 can run in parallel (different files), T034-T040 sequential (same file, method dependencies), T041 after all implementation

**User Story 4**: T042-T043 can run in parallel (different methods), T044-T053 mostly sequential due to method dependencies

### Parallel Opportunities

- **Setup (Phase 1)**: T003 and T004 can run in parallel
- **Foundational (Phase 2)**: T005-T011 (all entity models) can run in parallel, T012-T014 (utilities) can run in parallel
- **Within User Stories**: Tasks marked [P] can execute simultaneously
- **Across User Stories**: Once Phase 2 completes, all 4 user stories can be worked on in parallel by different developers

---

## Parallel Example: Foundational Phase

```bash
# Launch all entity models in parallel:
Task T005: "Implement WindowState enum in src/models/game_window.py"
Task T006: "Implement GameWindow entity in src/models/game_window.py"
Task T007: "Implement WindowCapture entity in src/models/window_capture.py"
Task T008: "Implement CoordinateType enum in src/models/click_target.py"
Task T009: "Implement ClickType enum in src/models/click_target.py"
Task T010: "Implement ClickTarget entity in src/models/click_target.py"
Task T011: "Implement TextRegion entity in src/models/text_region.py"

# Launch all utilities in parallel:
Task T012: "Create custom exceptions in src/utils/exceptions.py"
Task T013: "Implement timeout decorator in src/utils/timing.py"
Task T014: "Implement StructuredLogger in src/utils/logger.py"
```

---

## Parallel Example: User Story 1

```bash
# Launch all core detection methods in parallel:
Task T015: "Implement find_windows_by_title() in src/vision/window_detector.py"
Task T016: "Implement get_window_by_handle() in src/vision/window_detector.py"
Task T017: "Implement get_window_state() in src/vision/window_detector.py"
Task T018: "Implement is_window_valid() in src/vision/window_detector.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup → Project structure ready
2. Complete Phase 2: Foundational → All entities and utilities ready
3. Complete Phase 3: User Story 1 → Window detection working
4. **STOP and VALIDATE**: Test window detection with real game in various states
5. Delivers value: "Can I detect if Raid is running?"

**Time Estimate**: ~1-2 days for MVP (Setup + Foundational + US1)

### Incremental Delivery

1. Setup + Foundational → Foundation ready (~4 hours)
2. Add User Story 1 → Test independently → **MVP DEPLOYED** (window detection) (~4 hours)
3. Add User Story 2 → Test independently → **v0.2 DEPLOYED** (+ screen capture) (~4 hours)
4. Add User Story 3 → Test independently → **v0.3 DEPLOYED** (+ click automation) (~4 hours)
5. Add User Story 4 → Test independently → **v1.0 DEPLOYED** (+ OCR detection) (~6 hours)
6. Add Phase 7 + 8 → **v1.1 DEPLOYED** (+ monitoring + polish) (~4 hours)

**Total Estimate**: ~26 hours for full feature (1 week at 4-5 hours/day)

### Parallel Team Strategy

With 2-3 developers:

1. **Day 1**: Team completes Setup + Foundational together
2. **Day 2**: Once Foundational done:
   - Developer A: User Story 1 (window detection)
   - Developer B: User Story 2 (screen capture)
   - Developer C: Start on foundational utilities polish
3. **Day 3**: 
   - Developer A: User Story 3 (clicking) - requires US1 complete
   - Developer B: User Story 4 (OCR) - requires US2 complete
   - Developer C: Phase 7 (window monitoring)
4. **Day 4**: All developers on Phase 8 (polish, examples, validation)

---

## Task Count Summary

- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 10 tasks
- **Phase 3 (US1)**: 8 tasks
- **Phase 4 (US2)**: 9 tasks
- **Phase 5 (US3)**: 10 tasks
- **Phase 6 (US4)**: 12 tasks
- **Phase 7 (Monitoring)**: 5 tasks
- **Phase 8 (Polish)**: 9 tasks

**Total**: 67 tasks

**Parallelizable**: 28 tasks marked [P] (42% can run in parallel with proper staffing)

**Independent Stories**: All 4 user stories can be tested independently after Foundational phase completes

---

## Success Criteria Validation

Each user story maps to specific success criteria from spec.md:

- **US1 (Window Detection)** → SC-001: Detection <500ms, 100% accuracy when game running
- **US2 (Content Capture)** → SC-002: ≥10 FPS capture rate
- **US3 (Clicking)** → SC-003: Click accuracy within ±5px across window sizes
- **US4 (OCR)** → SC-004: ≥95% OCR accuracy on standard UI text

Validation script (T062) will test all success criteria systematically.

---

## Notes

- [P] tasks = different files, no dependencies, can execute simultaneously
- [Story] label maps task to specific user story (US1, US2, US3, US4) for traceability
- Each user story should be independently completable and testable after Foundational phase
- Tests are NOT included per feature specification (not explicitly requested)
- Commit after each task or logical group of parallel tasks
- Stop at any checkpoint to validate story independently before proceeding
- Foundational phase is CRITICAL - all user stories blocked until complete
- Vision-first: Detection (US1, US2, US4) implemented before automation (US3)
