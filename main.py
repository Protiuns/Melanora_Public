"""
MELANORA PUBLIC MASTER CONTROL (v0.1-Alpha)
The main entry point for the public version of Melanora.
Handles initialization and orchestration of local components.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add root to sys.path for internal imports
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path: sys.path.append(str(ROOT))

from core.topology import NeuralTopology
from core.bridge import NeuralBridge
from core.security import security_nexus

def start_services():
    """Initializes local services like Ollama and Neural Bridge."""
    print("🧬 MELANORA | Public Alpha v0.1")
    print("-" * 30)
    
    # 1. Start Security Layer
    print("[1/3] Initializing Security Nexus...")
    
    # 2. Start Ollama
    ollama_mgr = NeuralTopology.get_path("Ollama") / "Ollama_Manager.bat"
    if ollama_mgr.exists():
        print("[2/3] Starting Ollama Local Manager...")
        subprocess.Popen([str(ollama_mgr)], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        print("[2/3] Ollama Manager not found (Using remote fallback if available).")

    # 3. Start Neural Bridge
    print("[3/3] Activating Neural Bridge...")
    bridge = NeuralBridge()
    bridge.update_state(status="ACTIVE", mode="PUBLIC")
    
    print("\n[OK] Public services are ready.")
    print("Physical Mind activated. Use 'Ctrl+C' to exit.")

if __name__ == "__main__":
    start_services()
