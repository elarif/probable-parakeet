<!--
SYNC IMPACT REPORT
==================
Version: 0.0.0 → 1.0.0
Reason: Initial constitution creation for RSL automation project

Modified Principles:
- PRINCIPLE_1: Template → Vision-First Development
- PRINCIPLE_2: Template → Fail-Safe Automation
- PRINCIPLE_3: Template → Template-Based Detection
- PRINCIPLE_4: Template → Human-Like Behavior
- PRINCIPLE_5: Template → Observability & Debugging

Added Sections:
- Core Principles (5 automation-specific principles)
- Safety & Compliance
- Development Standards
- Governance

Templates Status:
✅ plan-template.md - Aligned with constitution gates
✅ spec-template.md - User stories support vision-first workflow
✅ tasks-template.md - Task organization supports incremental testing
✅ copilot-instructions.md - Synced with automation principles

Follow-up TODOs:
- None - all placeholders filled

Date: 2025-12-25
-->

# RSL Automation Constitution

## Core Principles

### I. Vision-First Development

**All features must start with vision/detection capabilities before automation.**

- Image templates and detection logic must be created and validated independently before click automation
- Every UI element must have a detection method (template matching, OCR, color detection, or pixel analysis)
- Detection accuracy thresholds documented and tested (minimum 90% success rate on reference screenshots)
- Template library organized by game screen/context with version tracking for UI updates
- Dry-run mode mandatory for testing detection without executing actions

**Rationale**: Game state detection is the foundation - automation without reliable vision creates brittle, dangerous bots that can misclick or loop infinitely.

### II. Fail-Safe Automation (NON-NEGOTIABLE)

**Every automation sequence must include timeout guards, state verification, and graceful failure modes.**

- All element detection calls MUST have timeout parameters (no infinite waits)
- State verification required before and after critical actions (verify before click, verify result after)
- Fallback strategies documented for common failure scenarios (element not found, unexpected pop-up, connection error)
- Emergency stop mechanism accessible during execution (hotkey or process monitor)
- Resource depletion detection (energy, keys, silver) must halt automation gracefully with notification

**Rationale**: Game automation can cause account damage if unchecked. Fail-safe design protects user accounts and prevents runaway processes.

### III. Template-Based Detection

**UI element detection must use template matching with tolerance for UI variations.**

- Store templates in `/assets/templates/` organized by screen context (battle/, tavern/, campaign/, etc.)
- PNG format with alpha channel for partial matching
- Naming convention: `{context}_{element}_{variant}.png` (e.g., `battle_start_button_normal.png`, `battle_start_button_highlighted.png`)
- Multiple variants for different UI states (normal, highlighted, disabled)
- Confidence thresholds configurable per template (0.7-0.95 range)
- ROI (region of interest) coordinates documented to limit search area and improve performance

**Rationale**: Game UI changes with updates. Template-based detection with variants provides resilience and maintainability.

### IV. Human-Like Behavior

**All automated actions must include randomization to avoid bot detection patterns.**

- Click coordinates randomized within element bounds (not fixed pixel clicks)
- Action timing includes configurable jitter (±10-30% of base delay)
- Mouse movement uses Bezier curves or human-like paths (not instant teleport)
- Interaction patterns vary (don't always click center, vary click duration)
- Configurable rate limiting between actions (respect minimum delays)

**Rationale**: Game developers implement bot detection. Human-like patterns reduce detection risk and account safety.

### V. Observability & Debugging

**All automation runs must be fully traceable and reproducible.**

- Structured logging with timestamp, action, coordinates, confidence scores
- Screenshot capture on failure cases (element not found, timeout, unexpected state)
- Debug overlay mode visualizes detected elements, ROIs, click points in real-time
- Execution metrics tracked (success rate, average duration, failure reasons)
- Replay capability from logged actions for debugging and optimization

**Rationale**: Vision-based automation is inherently probabilistic. Observability enables diagnosis, optimization, and confidence in production use.

## Safety & Compliance

**Account Safety Requirements**:
- Never store credentials in code or unencrypted configuration
- Multi-account support uses secure credential storage (OS keychain or encrypted vault)
- Rate limiting enforced to avoid triggering anti-bot systems
- Game client must be in foreground (no background automation that could interfere with other apps)
- User consent required for any account-modifying actions

**Performance Standards**:
- Resolution independence: Support 1920x1080 baseline with scaling for other resolutions
- Detection latency: <500ms for single element detection (95th percentile)
- Memory footprint: <200MB for automation engine + vision processing
- Template matching optimized (multi-scale, ROI-based, cached)

**Technology Constraints**:
- Computer vision: OpenCV or equivalent (template matching, feature detection)
- Screen capture: Platform-specific (mss, win32gui for Windows)
- UI automation: PyAutoGUI, AutoIt, or native Windows API
- OCR: Tesseract or cloud OCR API for text detection when needed

## Development Standards

**Testing Workflow**:
1. Create image templates from manual game screenshots
2. Test detection on static images (validate confidence thresholds)
3. Implement dry-run automation (log actions without executing)
4. Validate with real game interaction under supervision
5. Iterative refinement based on failure analysis

**Code Organization**:
```
/src/
  /vision/          # Detection logic (template matching, OCR)
  /automation/      # Click handlers, action sequences
  /game/            # Game-specific workflows (farming, arena, etc.)
/assets/
  /templates/       # UI element images
  /screenshots/     # Debug captures
/config/
  settings.json     # User preferences
  thresholds.json   # Detection confidence values
```

**Version Control**:
- Template library versioned alongside code
- Game version compatibility documented in README
- Breaking UI changes tracked in changelog
- Template updates documented with game patch notes reference

## Governance

**Constitution Authority**: This constitution supersedes all other development practices. All features, code reviews, and automation sequences must comply.

**Amendment Process**:
1. Propose change with rationale and impact analysis
2. Validate against existing automation workflows
3. Update version (MAJOR for principle changes, MINOR for new sections, PATCH for clarifications)
4. Migrate existing code/templates to comply
5. Document in sync impact report

**Compliance Verification**:
- All spec files must include constitution compliance check
- Code reviews verify fail-safe patterns and timeout guards
- Template PRs require accuracy metrics and variant coverage
- Runtime guidance in `.github/copilot-instructions.md` aligns with principles

**Version**: 1.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-25
