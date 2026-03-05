---
description: Export a game project or independent module to the _exports directory.
---

# Export Project / Module Workflow

1.  **Analyze Request:**
    - Is it a **Full Game Build**? (e.g., "Build Puk 97 for Windows")
    - Is it a **Module Export**? (e.g., "Export the Health Component")

2.  **Determine Version:**
    - Check current version in `project.godot` (for games) or `component_registry.json` (for modules).
    - Ask user if they want to bump the version (Patch/Minor/Major).

3.  **Execute Export:**

    **If Game Build:**
    - (Agent Note: Godot CLI export is preferred if configured, otherwise guide user or skip to manual).
    - If CLI is available: `godot --headless --export-release "Windows Desktop" _exports/builds/Game_v1.0.exe`
    - If not, instruct user or assume manual export for now.

    **If Module Export:**
    - // turbo
    - Compress the target directory to `_exports/modules`.
    - Example: `Compress-Archive -Path "studio_library/logic/health_component" -DestinationPath "_exports/modules/health_component_v1.0.zip"`

4.  **Verify:**
    - listing the `_exports` directory to show the result.
