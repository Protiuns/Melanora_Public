"""
🧠 Melanora Neural Bridge (Public v1.0)
Adaptive communication layer for local execution and monitoring.
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime

# Root detection
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "config"
LOGS_DIR = ROOT_DIR / "logs"

class NeuralBridge:
    def __init__(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.state_file = CONFIG_DIR / "neural_state.json"
        self.queue_file = CONFIG_DIR / "task_queue.json"

    def update_state(self, **kwargs):
        """Updates the internal neural state."""
        state = {}
        if self.state_file.exists():
            try:
                state = json.loads(self.state_file.read_text(encoding="utf-8"))
            except: pass
        
        state.update(kwargs)
        state["last_sync"] = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def log_event(self, event: str, level: str = "INFO"):
        """Logs an event to the local filesystem."""
        log_file = LOGS_DIR / f"bridge_{datetime.now().strftime('%Y%m%d')}.log"
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {event}\n")

    def start_listening(self):
        """Starts the main polling loop for tasks."""
        self.log_event("Neural Bridge started in Public mode.")
        if not self.queue_file.exists():
            self.queue_file.write_text(json.dumps({"queue": []}), encoding="utf-8")
        
        # Polling logic (Stub for public release)
        print("[MIND] Neural Bridge listening for local impulses...")

if __name__ == "__main__":
    bridge = NeuralBridge()
    bridge.start_listening()
