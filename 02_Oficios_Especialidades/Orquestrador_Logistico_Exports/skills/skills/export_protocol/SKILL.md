---
name: Export Protocol
description: A standardized workflow for building games, packaging modules, and delivering releases from the studio.
---

# Export Protocol

## 1. Overview
This skill defines the standardized process for exporting content from the studio. Whether it's a full game executable for a specific platform or a zipped module of assets for backup/sharing, all outputs must go through this protocol to ensure consistency and traceability.

## 2. Default Export Structure
The export area is located at the project root: `_exports/`.
It contains the following subdirectories:
- `builds/`: For playable game executables.
    - Structure: `builds/<ProjectName>/<Version>/<Platform>/`
- `modules/`: For zipped components, asset packs, or isolated features.
    - Structure: `modules/<ModuleName>/`
- `packages/`: For Godot resource packs (.pck or .zip).

## 3. Naming Convention (Critical)
All exported files must follow a strict naming convention to avoid confusion.
- **Projects:** `ProjectName_vX.Y.Z_Platform_BuildType`
    - Example: `Puk97_v0.1.0_Windows_Debug.exe`
- **Modules:** `ModuleName_vX.Y.Z_Date`
    - Example: `HealthComponent_v1.0.2_2023-10-27.zip`

## 4. The Export Workflows

### Workflow A: Full Game Export (Godot)
1.  **Verify Project Settings:** Ensure the `project.godot` has the correct `application/config/version`.
2.  **Define Export Path:** Set the export path in Godot to `_exports/builds/<ProjectName>/<Version>/<Platform>`.
3.  **Debug vs. Release:**
    - **Debug:** Useful for internal testing (includes console, profiler). Append `_debug` to filename.
    - **Release:** Optimized for players. Remove checkmarks for "Extract Debug Symbols" if not needed.
4.  **Export:** Run the export.
5.  **Sanity Check:** Run the exported executable immediately to ensure it launches.
6.  **Zip (Optional):** If the build contains multiple files (exe + pck), zip the *folder* for easier distribution.

### Workflow B: Module Export (Zipping)
When you need to export a specific folder (e.g., a Skill, a Component, or an Asset Pack):
1.  **Identify Source:** Locate the folder (e.g., `studio_library/logic/health_component`).
2.  **Define Destination:** `_exports/modules/<ComponentName>_v<Version>.zip`.
3.  **Compress:** Use a compression tool (PowerShell `Compress-Archive` or similar) to zip the folder.
4.  **Verify:** Check the zip file size and contents.

## 5. Agent Responsibilities
When the user asks to "export" or "build":
1.  **Clarify Scope:** Ask if it's a "Game Build" or a "Module/Backup Export".
2.  **Check Version:** Ask if the version number needs bumping.
3.  **Execute:** Use `run_command` to trigger the export or zip process.
4.  **Report:** Confirm the location of the exported file in `_exports/...`.
