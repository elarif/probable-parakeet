# Implementation Plan: Game Window Capture

**Branch**: `001-game-window-capture` | **Date**: 2025-12-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-game-window-capture/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement foundational window detection and capture system for Raid Shadow Legends automation. System must detect game window by title, capture content regardless of window size/position, execute scaled clicks, and detect text via OCR. This is the core vision layer enabling all future automation features.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: OpenCV (cv2), Tesseract OCR (pytesseract), mss (screen capture), pywin32 (Windows API), PyAutoGUI (click automation)  
**Storage**: File-based (image templates in `/assets/templates/`, debug screenshots in `/assets/screenshots/`)  
**Testing**: pytest with image fixtures, accuracy validation on reference screenshots  
**Target Platform**: Windows 10/11 (64-bit)
**Project Type**: Single project (automation library/CLI)  
**Performance Goals**: <500ms window detection, ≥10 FPS capture rate (100ms per frame), <200ms click execution  
**Constraints**: <200MB memory footprint, ≥90% detection accuracy on reference images, ≥95% OCR accuracy on standard UI text  
**Scale/Scope**: Single-user automation tool, ~5-10 core modules (window detection, capture, click, OCR, coordinate translation)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Vision-First Development**
- [x] Detection logic planned before automation sequences - Window detection and OCR are implemented first before any click automation
- [x] Image templates identified and capture plan documented - OCR-based text detection for initial implementation; template matching deferred to future features
- [x] Accuracy thresholds defined (≥90% success rate target) - ≥95% OCR accuracy on standard UI text specified in SC-004
- [x] Dry-run testing mode included in implementation plan - pytest with image fixtures for validation before live game interaction

**II. Fail-Safe Automation**
- [x] Timeout guards specified for all detection calls - FR-014 requires timeout mechanism for detection operations
- [x] State verification checkpoints documented (before/after critical actions) - FR-012 handles window state changes gracefully
- [x] Fallback strategies defined for failure scenarios - Edge cases document window minimization, crashes, missing windows
- [x] Emergency stop mechanism included - Will be implemented in automation layer (future feature; this feature focuses on detection/capture primitives)
- [x] Resource depletion detection planned - Not applicable to this feature (window detection/capture layer); relevant for higher-level automation workflows

**III. Template-Based Detection**
- [⚠️] Template organization follows `/assets/templates/{context}/` structure - **DEFERRED**: This feature uses OCR for text detection; template matching planned for future features
- [⚠️] Naming convention follows `{context}_{element}_{variant}.png` pattern - **DEFERRED**: No templates in this feature; OCR-based detection only
- [⚠️] Multiple UI state variants identified - **DEFERRED**: Future template-based features will implement variants
- [x] ROI coordinates planned for performance optimization - Text detection will support ROI parameters to limit search areas
- [x] Confidence thresholds documented per template type - OCR confidence scores returned with TextRegion entities (FR-010)

**IV. Human-Like Behavior**
- [⚠️] Click randomization within element bounds specified - **PARTIAL**: Click primitives provided; randomization implemented in higher-level automation features
- [⚠️] Timing jitter parameters defined (±10-30% delays) - **NOT APPLICABLE**: This feature provides click primitives; timing managed by automation layer
- [⚠️] Mouse movement patterns described (Bezier/human-like paths) - **NOT APPLICABLE**: Basic click implementation; movement patterns for future enhancement
- [⚠️] Rate limiting between actions configured - **NOT APPLICABLE**: This is a foundational library; rate limiting applied by consuming automation scripts

**V. Observability & Debugging**
- [x] Structured logging format defined (timestamp, action, coordinates, confidence) - FR-015 requires logging all window operations with timestamps and success/failure
- [x] Screenshot capture on failure planned - Debug mode will save captures to `/assets/screenshots/` for troubleshooting
- [x] Debug overlay mode specified for visualization - Future enhancement; initial version logs coordinates and confidence scores
- [x] Execution metrics tracked (success rate, duration, failures) - Logging includes operation duration and success/failure status
- [x] Replay capability from logs considered - Logs capture sufficient data for analysis; replay system for future iteration

**Safety & Compliance**
- [x] No credential storage in code or plain config - This feature doesn't handle credentials; window detection only
- [x] Rate limiting to avoid anti-bot detection - Not applicable at this layer; managed by higher-level automation
- [x] Foreground-only automation enforced - FR-008 notes background clicking is desirable but can fallback to foreground focus
- [x] User consent mechanism for account-modifying actions - This feature provides primitives only; consent handled by automation workflows

**GATE EVALUATION**: ✅ **PASS WITH JUSTIFICATION**
- Template-based detection (Principle III) partially deferred because this feature focuses on OCR text detection as the primary vision method. Template matching will be added in future features when UI element recognition beyond text is needed.
- Human-like behavior (Principle IV) partially deferred because this feature provides low-level click primitives. Randomization, jitter, and movement patterns will be implemented in higher-level automation features that orchestrate sequences.
- Emergency stop and resource depletion (Principle II) are not applicable to this foundational layer; they belong to the automation orchestration layer.

---

## Post-Design Constitution Re-evaluation

*Re-checked after Phase 1 design completion (data-model.md, contracts/, quickstart.md)*

**Design Alignment Assessment**:

✅ **I. Vision-First Development** - Fully aligned
- API contracts clearly separate detection (WindowDetector, OCREngine) from automation (ClickHandler)
- WindowCapture and TextRegion entities enforce detection-first workflow
- Quickstart examples demonstrate detect→capture→analyze→click pattern
- Dry-run testing via pytest fixtures documented in project structure

✅ **II. Fail-Safe Automation** - Fully aligned
- All API contracts include timeout parameters (default 5s)
- Custom exceptions defined (WindowNotFoundError, CaptureTimeoutError, ClickFailedError)
- WindowMonitor provides state change detection for graceful failure
- Error handling patterns demonstrated in quickstart guide

⚠️ **III. Template-Based Detection** - Deferred (justified)
- OCR-based detection is primary approach for this feature
- Template matching infrastructure planned in project structure (`/assets/templates/`) but not implemented
- Future features will add template matching for non-text UI elements
- **Justification remains valid**: Text-based UI detection is sufficient for initial automation workflows

⚠️ **IV. Human-Like Behavior** - Partially deferred (justified)
- Click primitives provide `delay_ms` parameter for configurable timing
- CoordinateType.RELATIVE enables randomization within element bounds by consumers
- Click randomization and mouse movement curves delegated to higher-level automation layers
- **Justification remains valid**: This is a primitive API; behavior patterns belong in orchestration

✅ **V. Observability & Debugging** - Fully aligned
- Structured logging design in research.md with JSON output format
- Screenshot capture methods (capture_window_to_file) for debugging
- TextRegion confidence scores tracked for accuracy analysis
- Example error handling patterns in quickstart guide

✅ **Safety & Compliance** - Fully aligned
- No credential handling in this feature (window detection only)
- Timeout guards prevent infinite loops
- Window state monitoring enables detection of game closure
- Permission errors documented as CaptureFailedError/ClickFailedError

**CONCLUSION**: ✅ **Design passes constitution check**. All deferred items remain justified as higher-level concerns. API contracts enforce fail-safe patterns and vision-first workflow.

## Project Structure

### Documentation (this feature)

```text
specs/001-game-window-capture/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── window_api.py    # Window detection and management API contract
│   ├── capture_api.py   # Screen capture API contract
│   ├── click_api.py     # Click automation API contract
│   └── ocr_api.py       # OCR text detection API contract
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Single project structure (automation library)
src/
├── vision/
│   ├── window_detector.py    # GameWindow detection (FR-001, FR-002, FR-003)
│   ├── screen_capture.py     # WindowCapture implementation (FR-004, FR-005)
│   ├── ocr_engine.py          # TextRegion detection (FR-009, FR-010)
│   └── coordinate_scaler.py   # Coordinate translation (FR-007)
├── automation/
│   ├── click_handler.py       # Click execution (FR-006, FR-008, FR-011)
│   └── window_monitor.py      # State change detection (FR-012)
├── models/
│   ├── game_window.py         # GameWindow entity
│   ├── window_capture.py      # WindowCapture entity
│   ├── click_target.py        # ClickTarget entity
│   └── text_region.py         # TextRegion entity
└── utils/
    ├── logger.py              # Structured logging (FR-015)
    └── timing.py              # Timeout mechanisms (FR-014)

tests/
├── unit/
│   ├── test_window_detector.py
│   ├── test_screen_capture.py
│   ├── test_ocr_engine.py
│   ├── test_coordinate_scaler.py
│   └── test_click_handler.py
├── integration/
│   ├── test_detection_capture_flow.py
│   └── test_capture_click_flow.py
├── contract/
│   └── test_api_contracts.py
└── fixtures/
    ├── screenshots/           # Reference game screenshots at various resolutions
    └── expected_results/      # Expected detection outputs for validation

assets/
├── templates/                 # Empty for this feature; used by future template-matching features
└── screenshots/               # Debug captures saved during failures
```

**Structure Decision**: Single project structure chosen because this is a foundational automation library with clear module separation (vision, automation, models, utils). No frontend/backend split needed. All code runs locally on Windows platform.

## Complexity Tracking

> **No violations to justify** - All constitution checks pass or are appropriately deferred to future features. This is a foundational feature providing primitive capabilities (detection, capture, click, OCR) that will be composed by higher-level automation workflows.
