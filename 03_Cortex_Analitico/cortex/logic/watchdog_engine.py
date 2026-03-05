"""
🛡️ Melanora Watchdog Engine v1.0
Monitora a saúde do sistema e previne estados de congelamento (frozen).
"""

import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
WATCHDOG_FILE = CONFIG_DIR / "watchdog.json"

def update_heartbeat(component_name):
    """Atualiza o timestamp de batimento de um componente."""
    data = {}
    if WATCHDOG_FILE.exists():
        try:
            with open(WATCHDOG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except: pass
    
    data[component_name] = {
        "last_pulse": time.time(),
        "status": "ALIVE"
    }
    
    with open(WATCHDOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def check_health():
    """Verifica a saúde de todos os componentes registrados."""
    if not WATCHDOG_FILE.exists():
        return {"status": "UNCERTAIN", "message": "Watchdog file missing"}
    
    try:
        with open(WATCHDOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return {"status": "ERROR", "message": "Corrupt watchdog data"}
    
    current_time = time.time()
    health_report = {"components": {}, "system_healthy": True}
    
    for comp, info in data.items():
        elapsed = current_time - info["last_pulse"]
        is_alive = elapsed < 15 # Considere "morto" se não houver pulso por 15s
        
        health_report["components"][comp] = {
            "status": "ALIVE" if is_alive else "DEAD",
            "latency_sec": round(elapsed, 2)
        }
        
        if not is_alive:
            health_report["system_healthy"] = False
            
    return health_report

if __name__ == "__main__":
    # Teste de leitura
    print(json.dumps(check_health(), indent=2))
