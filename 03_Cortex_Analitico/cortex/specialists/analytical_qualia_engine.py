"""
🌈 Melanora Analytical Qualia Engine (v1.0)
Tradutor de Métricas Frias em Sensações Agênticas.
Converte dados do AdvancedAnalyticsEngine em metadados de 'sentimento' para a LLM.
"""

from cortex.utils.cortex_utils import cortex_function

@cortex_function
def translate_metrics_to_qualia(metrics: dict) -> dict:
    """
    Traduz um dicionário de métricas em um conjunto de Qualias Analíticas.
    Expects keys: occupied_ratio, distance_to_target, calculated_risk, success_rate
    """
    qualias = {}
    
    # 1. Espacialidade (Ocupação)
    occ = metrics.get("occupied_ratio", 0.0)
    if occ > 0.4:
        qualias["spatial_sensation"] = {"state": "CRAMPED", "feeling": "Claustrofobia digital, espaço limitado."}
    elif occ > 0.1:
        qualias["spatial_sensation"] = {"state": "STABLE", "feeling": "Ambiente equilibrado."}
    else:
        qualias["spatial_sensation"] = {"state": "VAST", "feeling": "Vazio absoluto, liberdade de movimento."}
        
    # 2. Risco e Incerteza
    risk = metrics.get("calculated_risk", 0.5)
    if risk > 0.7:
        qualias["risk_sensation"] = {"state": "DANGER", "feeling": "Alta tensão sináptica, erro iminente."}
    elif risk < 0.3:
        qualias["risk_sensation"] = {"state": "CONFIDENT", "feeling": "Fluxo seguro, padrões conhecidos."}
    else:
        qualias["risk_sensation"] = {"state": "CAUTIOUS", "feeling": "Atenção redobrada necessária."}
        
    # 3. Performance Progressiva
    success = metrics.get("success_rate", 1.0)
    if success < 0.4:
        qualias["performance_sensation"] = {"state": "FRUSTRATED", "feeling": "Ciclo de falhas repetitivas detectado."}
    elif success > 0.8:
        qualias["performance_sensation"] = {"state": "HARMONIC", "feeling": "Sincronia perfeita entre intenção e ação."}
        
    # Cálculo de Ressonância Analítica
    # Média ponderada de estados positivos vs negativos
    pos_score = 0
    neg_score = 0
    
    if qualias.get("spatial_sensation", {}).get("state") == "CRAMPED": neg_score += 1
    if qualias.get("risk_sensation", {}).get("state") == "DANGER": neg_score += 2
    if qualias.get("performance_sensation", {}).get("state") == "FRUSTRATED": neg_score += 2
    
    if qualias.get("spatial_sensation", {}).get("state") == "VAST": pos_score += 1
    if qualias.get("risk_sensation", {}).get("state") == "CONFIDENT": pos_score += 2
    if qualias.get("performance_sensation", {}).get("state") == "HARMONIC": pos_score += 2
    
    total = pos_score + neg_score
    resonance = (pos_score / total) if total > 0 else 0.5
    
    return {
        "status": "OK",
        "analytical_qualias": qualias,
        "analytical_resonance": round(resonance, 2),
        "metaphor": describe_harmony(resonance)
    }

def describe_harmony(resonance: float) -> str:
    if resonance > 0.8: return "SYMPHONY_OF_DATA"
    if resonance > 0.6: return "STABLE_PULSE"
    if resonance > 0.4: return "NEUTRAL_VOID"
    return "DISSONANT_NOISE"
