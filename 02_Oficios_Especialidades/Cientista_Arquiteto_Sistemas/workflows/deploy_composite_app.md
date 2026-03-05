---
description: How to create a simplified, composite application delivery folder from multiple source components.
---

1. **Define Delivery Plan**
   - Identify the target folder name (e.g., `Entrega_Final` or a specific product name like `ServidorJola`).
   - Identify the source components (modules/projects) to include.
   - Determine necessary launch scripts and setup procedures.

2. **Create Target Directory**
   - Clean or create the target directory.
   - Example: `mkdir "Entrega_Final"`

3. **Copy Source Components (Clean Copy)**
   - Copy each component folder to the target directory.
   - **CRITICAL**: Exclude heavy development directories (`node_modules`, `.git`, `.vscode`, `dist`, `release`, `test`).
   - Use `robocopy` for efficiency:
     ```bat
     robocopy "Source/ProjectA" "Target/ProjectA" /MIR /XD node_modules .git .vscode dist release test /XF .DS_Store Thumbs.db
     ```

4. **Generate Setup Automation**
   - Create a script (e.g., `Instalar_e_Compilar.bat`) to handle dependencies for the end-user.
   - The script must:
     - Navigate to each component folder.
     - Run `npm install`.
     - Run `npm run build` (if applicable).
     - Return to the root.
   - Make it user-friendly with progress messages (`echo [1/4] Installing...`).

5. **Generate Launch Automation**
   - Create a central launcher script (e.g., `Launch App.bat`).
   - It should:
     - Navigate to the main executable component (e.g., `ServerManager`).
     - Execute the start command (e.g., `npm run electron:dev` or the compiled binary).

6. **Create Documentation (README.md)**
   - Explain clearly how to:
     1. Run the setup script first (`Instalar_e_Compilar.bat`).
     2. Run the launcher script (`Launch App.bat`).
   - List the included components and their purpose.

7. **Verify**
   - Test the setup script in a clean environment (or simulate it).
   - Test the launcher script.
