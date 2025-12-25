# Copilot Instructions

## Project Overview
Raid Shadow Legends automation tool for detecting game elements and automating repetitive actions. This project uses computer vision, image recognition, and UI automation to interact with the game client.

## Architecture

### Core Components
- **Vision Module** - Screen capture, image recognition, OCR for detecting UI elements, champions, artifacts
- **Automation Engine** - Click automation, action sequences, macro execution
- **Game State Manager** - Tracks current game state (battle, tavern, campaign, etc.)
- **Configuration System** - User settings, coordinates, image templates, thresholds

### Data Flow
1. Screen capture → Image processing → Element detection
2. Game state analysis → Decision making → Action execution
3. Results logging → Performance metrics → User feedback

## Development Workflow

### Build & Run
```powershell
# TODO: Add specific commands once framework is chosen
# python main.py          # For Python-based automation
# dotnet run              # For C# automation
```

### Testing
```powershell
# Test image recognition without game interaction
# TODO: Add test commands for vision accuracy

# Dry-run mode for testing action sequences
# TODO: Add safe testing mode that simulates clicks
```

### Debugging
- Use debug overlay to visualize detected elements
- Log all screen captures and decisions for replay analysis
- Test with static screenshots before live game interaction
- Adjust confidence thresholds for image matching

## Code Conventions

### Coordinate System
- Always use relative coordinates or anchor points
- Document resolution dependencies (1920x1080 vs other resolutions)
- Use template matching with tolerance for slight UI variations

### Action Patterns
```python
# Example: Safe click with verification
def click_element(template, timeout=5, verify=True):
    location = find_element(template, timeout)
    click(location)
    if verify:
        wait_for_state_change()
```

### Image Templates
- Store UI element templates in `/assets/templates/`
- Use PNG format with alpha channel for better matching
- Name templates by function: `button_battle_start.png`, `hero_level_indicator.png`
- Include multiple variants for different UI states

### Error Handling
- Always timeout on element detection (avoid infinite loops)
- Implement fallback strategies when elements not found
- Log failures with screenshots for debugging
- Graceful degradation when game state is unexpected

## Key Files & Directories
```
/assets/
  /templates/          # UI element images for matching
  /screenshots/        # Captured screens for debugging
/src/
  /vision/            # Image recognition, OCR
  /automation/        # Click handlers, action sequences
  /game/              # Game-specific logic (battles, farming)
/config/
  settings.json       # User preferences, coordinates
  accounts.json       # Multi-account configuration (encrypted)
```

## Game-Specific Knowledge

### Common Automation Tasks
- **Campaign farming** - Repeat specific stages for XP/gear
- **Arena battles** - Auto-battle sequence with team selection
- **Clan Boss** - Daily automated attacks with optimal team
- **Artifact management** - Auto-sell low quality items
- **Champion training** - Level up food champions

### UI Detection Challenges
- Loading screens vary in duration (implement smart waiting)
- Pop-ups and rewards interrupt workflows (handle modally)
- Energy/key depletion stops automation (detect and notify)
- Connection errors require retry logic

### Safety Considerations
- Randomize timing between actions (avoid bot detection patterns)
- Implement human-like mouse movement curves
- Add configurable delays and jitter
- Respect rate limits to avoid account flags

## Dependencies & Integration
- Computer vision library (OpenCV, PIL, pytesseract for OCR)
- UI automation (PyAutoGUI, AutoIt, or Windows API)
- Screen capture (mss, win32gui for Windows)
- Image matching with configurable confidence thresholds

## Common Tasks

### Adding New Automation Sequence
1. Capture screenshots of all UI states in the sequence
2. Create image templates for key elements
3. Map the decision tree (if X visible, do Y)
4. Implement with proper error handling and timeouts
5. Test with dry-run mode before live execution

### Optimizing Detection Accuracy
- Adjust confidence threshold (0.7-0.9 typical range)
- Use ROI (region of interest) to limit search area
- Implement multi-scale template matching for resolution independence
- Add color-based pre-filtering for faster detection

### Common Pitfalls
- Game updates change UI layouts (maintain template library)
- Different screen resolutions break coordinate-based code
- Network lag causes timing issues (implement adaptive waits)
- Background processes interfere with screen capture
- Game must be in foreground for reliable automation

---
*Last updated: December 25, 2025*
