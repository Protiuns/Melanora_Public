"""
🧬 Melanora Synthesis Engine (v1.0)
Destilador de Sensações: Transformando padrões em Pensamento (Neural Qualia).
Integra Percepção com Memória de Longo Prazo.
"""

import os
import json
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

BASE_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico")
QUALIA_FILE = BASE_DIR / "config" / "neural_qualia.json"

@cortex_function
def process_sensory_pulse(source_type: str, features: dict) -> dict:
    """
    Processa um pulso sensorial e verifica se ele ressoa com padrões existentes.
    source_type: 'VISION' | 'AUDIO' | 'ABSTRACT'
    features: {'color': '#00FFAB', 'peak_freq': 440, etc}
    """
    qualia_data = load_qualia()
    context = qualia_data.get("buffer", {})
    
    # Adicionar ao buffer de observação temporal
    if source_type not in context:
        context[source_type] = []
        
    entry = {
        "timestamp": time.time(),
        "data": features
    }
    context[source_type].append(entry)
    
    # Limitar buffer (Pattern Observation Window)
    if len(context[source_type]) > 20:
        context[source_type].pop(0)
        
    qualia_data["buffer"] = context
    save_qualia(qualia_data)
    
    return identify_recurring_patterns(source_type)

def identify_recurring_patterns(source_type: str) -> dict:
    """Analisa o buffer para encontrar padrões que atingiram o limiar de solidificação."""
    qualia_data = load_qualia()
    buffer = qualia_data.get("buffer", {}).get(source_type, [])
    
    if len(buffer) < 5:
        return {"status": "OBSERVING", "coherence": 0.0}
        
    # Lógica de Coerência Simples: Frequência de valores similares
    # Ex: Se a cor dominante for a mesma em 70% das amostras
    # (Poderia ser expandido para clusters vetoriais no futuro)
    
    patterns = {}
    for entry in buffer:
        for k, v in entry["data"].items():
            key = f"{k}:{v}"
            patterns[key] = patterns.get(key, 0) + 1
            
    total_samples = len(buffer)
    solidified = []
    
    for key, count in patterns.items():
        coherence = count / total_samples
        if coherence >= 0.7: # Limiar de Solidificação (v1.0)
            k, v = key.split(":")
            solidified.append({"feature": k, "value": v, "coherence": coherence})
            crystallize_qualia(source_type, k, v, coherence)
            
    return {
        "status": "SOLIDIFYING" if solidified else "OBSERVING",
        "patterns": solidified
    }

def crystallize_qualia(source_type: str, feature: str, value: str, coherence: float):
    """Cristaliza um padrão como Qualia oficial e persistente."""
    data = load_qualia()
    registry = data.setdefault("stable_qualia", {})
    
    qualia_id = f"{source_type}_{feature}"
    
    registry[qualia_id] = {
        "value": value,
        "coherence": coherence,
        "last_solidified": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hits": registry.get(qualia_id, {}).get("hits", 0) + 1
    }
    
    save_qualia(data)
    log_event(f"QUALIA SOLIDIFICADA: {qualia_id} = {value} (Coerência: {coherence:.2%})")

def load_qualia() -> dict:
    if not QUALIA_FILE.exists():
        return {"stable_qualia": {}, "buffer": {}}
    with open(QUALIA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_qualia(data: dict):
    if not QUALIA_FILE.parent.exists():
        QUALIA_FILE.parent.mkdir(parents=True)
    with open(QUALIA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
