# -*- coding: utf-8 -*-
"""
⚖️ Melanora Neural Load Balancer (v1.0)
Gerencia o esforço analítico e sugere expansão de hardware.
Newton: Este é o coordenador de esforço que protege o núcleo central.
"""

import time
import json
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"

@cortex_function
def evaluate_neural_load() -> dict:
    """Analisa a carga de trabalho atual e sugere delegação se necessário."""
    metrics_path = CONFIG_DIR / "neural_metrics.json"
    
    # Simulação de carga baseada em latência recente
    if not metrics_path.exists():
        return {"status": "CALIBRATING", "load": 0.0}
        
    try:
        with open(metrics_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            stats = data.get("stats", {})
            avg_ms = stats.get("avg_latency_ms", 0.0)
            
            # Heurística: se latência > 1000ms, a mente está sob esforço analítico intenso
            load_factor = min(1.0, avg_ms / 2000)
            
            recommendation = "OPTIMAL_FLOW"
            if load_factor > 0.7:
                recommendation = "EXPANSION_REQUIRED"
                log_event("Esforço analítico intenso detectado. Sugerindo expansão de Hub.", "WARNING")
            
            return {
                "load": round(load_factor * 100, 1),
                "avg_latency": avg_ms,
                "recommendation": recommendation,
                "timestamp": time.time()
            }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

@cortex_function
def suggest_new_hubs() -> list:
    """Analisa a topologia e sugere novos hubs com base na densidade de arquivos."""
    graph_path = CONFIG_DIR / "knowledge_graph.json"
    if not graph_path.exists():
        return ["ARCHITECTURAL_EXPLORATION_HUB"]
        
    try:
        with open(graph_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            nodes = data.get("nodes", [])
            # Agrupar por camada/diretório
            layers = {}
            for n in nodes:
                layer = n.get("metadata", {}).get("layer", "ROOT")
                layers[layer] = layers.get(layer, 0) + 1
            
            # Sugerir expansão para a camada mais densa
            dense_layer = max(layers, key=layers.get)
            return [f"SUPER_SPECIALIZED_{dense_layer}_HUB", "CROSS_REFERENCING_UNIT"]
    except:
        return ["DYNAMIC_GROWTH_UNIT"]
