"""
🌈 Melanora Synesthesia Bridge (v1.0)
Traduz sinais numéricos e espaciais em intensidades de "Qualia".
Conecta a visão analítica com a intuição agencial.
"""

import math
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

@cortex_function
def map_spatial_to_qualia(snake_state: dict) -> dict:
    """
    Associa coordenadas (x, y) a sensações intuitivas.
    Newton: Este é o 'Paladar e Olfato' do sistema.
    """
    if not snake_state.get("active"):
        return {"qualia": "VOID", "intensity": 0.0}

    head = snake_state["head"]
    food = snake_state["food"]
    
    # 1. Olfato Digital (Proximidade)
    distance = math.sqrt((food[0] - head[0])**2 + (food[1] - head[1])**2)
    
    # Intensidade inversamente proporcional à distância
    smell_intensity = max(0.1, min(1.0, 1.0 - (distance / 500)))
    
    # 2. Paladar Digital (Direção/Alinhamento)
    dx = food[0] - head[0]
    dy = food[1] - head[1]
    
    alignment = 1.0 - (min(abs(dx), abs(dy)) / (max(abs(dx), abs(dy)) + 1e-5))
    taste_intensity = alignment
    
    qualias = {
        "digital_smell": {
            "label": "Food Proximity",
            "intensity": round(smell_intensity, 2),
            "state": "SWEET" if smell_intensity > 0.7 else "FAMILIAR"
        },
        "digital_taste": {
            "label": "Path Alignment",
            "intensity": round(taste_intensity, 2),
            "state": "PURE" if taste_intensity > 0.9 else "BITTER"
        },
        "neural_resonance": round((smell_intensity + taste_intensity) / 2, 2)
    }
    
    log_event(f"SYNESTHESIA: Ressonância Neural em {qualias['neural_resonance']}")
    
    return {
        "status": "OK",
        "qualias": qualias,
        "action_intent": "CONSUME" if smell_intensity > 0.8 else "HUNT"
    }

@cortex_function
def generate_sensory_harmony(qualia_data: dict) -> str:
    """
    Converte as qualias em uma metáfora de sentimento para a LLM.
    """
    resonance = qualia_data.get("qualias", {}).get("neural_resonance", 0.0)
    if resonance > 0.8:
        return "ECSTATIC_FLOW"
    elif resonance > 0.5:
        return "FOCUSED_RHYTHM"
    else:
        return "SEARCHING_VOID"
