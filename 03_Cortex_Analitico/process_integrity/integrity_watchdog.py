"""
👮 Melanora Integrity Engine: Process Watchdog (v0.1)
Monitora a saúde dos processos e estima o tempo de conclusão.
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

# Caminhos
BASE_DIR = Path(__file__).parent.parent.parent
QUEUE_FILE = BASE_DIR / "03_Cortex_Analitico" / "task_queue.json"
INTEGRITY_LOG = BASE_DIR / "03_Cortex_Analitico" / "process_integrity" / "integrity_report.json"

# Configurações de TTL (Segundos)
DEFAULT_TASK_TTL = 300  # 5 minutos
MODEL_DOWNLOAD_TTL = 3600 # 1 hora

def check_process_integrity():
    """Verifica se há processos travados e estima progresso."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "status": "IDLE",
        "system_health": "STABLE",
        "active_tasks": 0,
        "alerts": [],
        "message": ""
    }

    if not QUEUE_FILE.exists():
        report["message"] = "Nenhuma tarefa em fila."
        return report

    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue_data = json.load(f)
    except:
        report["status"] = "ERROR"
        report["system_health"] = "CRITICAL"
        report["message"] = "Falha ao ler task_queue.json"
        return report

    tasks = queue_data.get("tasks", [])
    report["active_tasks"] = len(tasks)
    
    if not tasks:
        report["message"] = "Fila vazia."
        return report

    report["status"] = "BUSY"
    now = time.time()
    
    for task in tasks:
        start_time = task.get("start_time", now)
        duration = now - start_time
        task_id = task.get("id", "unknown")
        
        limit = DEFAULT_TASK_TTL
        if "download" in task.get("type", "").lower():
            limit = MODEL_DOWNLOAD_TTL
            
        if duration > limit:
            report["alerts"].append({
                "task_id": task_id,
                "duration_sec": round(duration, 1),
                "severity": "CRITICAL",
                "issue": "PROCESS_STUCK_OR_OVERLIMIT"
            })
            
    if report["alerts"]:
        report["system_health"] = "ANOMALY_DETECTED"

    # Persistir relatório
    INTEGRITY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(INTEGRITY_LOG, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    return report

if __name__ == "__main__":
    res = check_process_integrity()
    print(f"👮 Auditoria Integridade: {res['system_health']} [{res['status']}]")
    if res['message']:
        print(f"  ℹ️  {res['message']}")
    if res['alerts']:
        for a in res['alerts']:
            print(f"  ⚠️ ALERTA: Task {a['task_id']} rodando há {a['duration_sec']}s")
