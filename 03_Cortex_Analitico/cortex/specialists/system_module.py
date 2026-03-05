"""
🖥️ Melanora System Module (v1.0)
Interface entre o Córtex Analítico e o Hardware do computador.
"""

import json
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

PROFILE_FILE = Path(__file__).parent.parent.parent / "config" / "machine_profile.json"

@cortex_function
def get_hardware_summary() -> dict:
    """Retorna o resumo do hardware detectado."""
    if not PROFILE_FILE.exists():
        return {"error": "Machine profile not found. Run hardware_profiler.py"}
    
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    hw = data.get("hardware", {})
    prof = data.get("profile", {})
    
    return {
        "machine": data.get("machine_id"),
        "cpu": hw.get("cpu", {}).get("name"),
        "cores": hw.get("cpu", {}).get("logical_cores"),
        "perfil": prof.get("perfil"),
        "freq_limite_hz": prof.get("freq_max_hz")
    }

@cortex_function
def check_thermal_status() -> dict:
    """Retorna telemetria real de carga e memória do hardware."""
    if not PSUTIL_AVAILABLE:
        return {"status": "LIMITED", "message": "Instale psutil para telemetria completa."}
    
    cpu_usage = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    
    status = "OPTIMAL"
    if cpu_usage > 85 or ram.percent > 90:
        status = "STRESSED"
        
    return {
        "status": status,
        "cpu_load": cpu_usage,
        "ram_usage": ram.percent,
        "active_processes": len(psutil.pids())
    }
