"""
📊 Melanora Metrics Counter (v1.0)
Telemetria em tempo real das ondas sinápticas e ritos neurais.
Armazena estatísticas de performance do Córtex Analítico.
"""

import json
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

METRICS_FILE = Path(__file__).parent.parent / "config" / "neural_metrics.json"

@cortex_function
def add_pulse_metric(task_id: str, elapsed_ms: float, status: str = "OK"):
    """Registra a performance de um único pulso (tarefa)."""
    data = _load_metrics()
    
    # Atualizar estatísticas globais
    stats = data.get("stats", {"total_pulses": 0, "avg_latency_ms": 0.0, "error_rate": 0.0, "errors": 0})
    
    stats["total_pulses"] += 1
    # Média móvel simples
    stats["avg_latency_ms"] = (stats["avg_latency_ms"] * (stats["total_pulses"] - 1) + elapsed_ms) / stats["total_pulses"]
    
    if status != "OK":
        stats["errors"] += 1
    
    stats["error_rate"] = stats["errors"] / stats["total_pulses"]
    
    data["stats"] = stats
    data["last_update"] = time.ctime()
    
    # Manter as últimas 100 métricas em um log circular (opcional)
    history = data.get("history", [])
    history.append({"id": task_id, "ms": elapsed_ms, "status": status, "t": time.time()})
    data["history"] = history[-100:] 
    
    _save_metrics(data)
    return stats

@cortex_function
def get_neural_telemetry() -> dict:
    """Retorna o estado de saúde e performance do cérebro físico."""
    return _load_metrics().get("stats", {})

def _load_metrics():
    if not METRICS_FILE.exists():
        return {"stats": {"total_pulses": 0, "avg_latency_ms": 0.0, "error_rate": 0.0, "errors": 0}, "history": []}
    try:
        return json.loads(METRICS_FILE.read_text(encoding="utf-8"))
    except:
        return {"stats": {"total_pulses": 0, "avg_latency_ms": 0.0, "error_rate": 0.0, "errors": 0}, "history": []}

def _save_metrics(data):
    METRICS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
