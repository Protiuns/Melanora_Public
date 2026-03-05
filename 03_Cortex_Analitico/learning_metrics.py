"""
🏆 Melanora Learning Metrics (v1.0)
Registra e analisa a evolução do desempenho em tarefas agenciais.
"""

import json
import time
from pathlib import Path

METRICS_FILE = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico/config/learning_metrics.json")

def record_match(match_id, score, resonance_avg, duration_s):
    """Registra o resultado de uma partida."""
    metrics = {"history": []}
    if METRICS_FILE.exists():
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            metrics = json.load(f)
    
    entry = {
        "match_id": match_id,
        "score": score,
        "resonance_avg": round(resonance_avg, 2),
        "duration_s": round(duration_s, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    metrics["history"].append(entry)
    metrics["best_score"] = max(metrics.get("best_score", 0), score)
    metrics["total_matches"] = metrics.get("total_matches", 0) + 1
    
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
        
    print(f"[METRICS] Partida {match_id} | Score: {score} | Melhor: {metrics['best_score']}")
    return metrics

def get_stats():
    """Retorna estatísticas sumárias."""
    if not METRICS_FILE.exists():
        return None
    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
