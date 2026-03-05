"""
🧠⚖️ Percepção Heurística (Sistema 1)
Módulo responsável por emular a cognição instintiva e rápida antes da execução analítica profunda.
Avalia o 'grau de estranheza' ou 'novidade' de uma entrada e decide se há um Dilema Cognitivo.
"""

import json
import random
from datetime import datetime

# Import Matemático (Sistema 1a)
try:
    from cortex.perception.math_vision import MathVisionCortex
except ImportError:
    MathVisionCortex = None

# Semântico (Sistema 1b)
try:
    from cortex.heuristics.local_semantic_engine import run_semantic_reflex
except ImportError:
    run_semantic_reflex = None

class HeuristicSystem1:
    def __init__(self):
        self.confidence_threshold = 0.5
        
        # Padrões conhecidos de módulos do Córtex (Affordances mentais imediatas)
        self.familiar_affordances = [
            "vision", "memory", "speech", "system", "file", "network"
        ]
        
    def analyze_input(self, module: str, function: str, params: dict) -> dict:
        """
        Avalia rapidamente a entrada e retorna um nível de confiança instintiva.
        Simula a primeira olhada de um humano para um problema.
        """
        confidence = 1.0
        reasons = []
        
        # 1. Análise de Familiaridade do Módulo
        module_lower = module.lower()
        if not any(a in module_lower for a in self.familiar_affordances):
            confidence -= 0.3
            reasons.append(f"Módulo estruturalmente desconhecido: '{module}'")
            
        # 2. Heurística de Complexidade (Muitos parâmetros = alerta)
        if len(params) > 3:
            confidence -= 0.2
            reasons.append("Carga cognitiva alta (muitos parâmetros)")
            
        # 3. Anomalias nos parâmetros
        for k, v in params.items():
            if isinstance(v, str) and (len(v) > 200 and not v.startswith("http")):
                confidence -= 0.2
                reasons.append(f"Parâmetro '{k}' excepcionalmente verboso")
            if "unknown" in str(v).lower() or "undefined" in str(v).lower():
                confidence -= 0.4
                reasons.append("Parametrização incompleta / ambígua")
        
        # Clamp confidence
        confidence = max(0.0, min(1.0, confidence))
        
        # --- NOVO: Integração com Visão Biomimética (Se for módulo de visão e params contiverem screenshot)
        semantic_action = "none"
        if "vision" in module_lower and "screen_data" in params and run_semantic_reflex:
            # Fakeamos o envio do JSON de OpenCV para a engine semântica local
            reflex_response = run_semantic_reflex(params["screen_data"])
            if reflex_response.get("action") == "press_key":
                semantic_action = reflex_response["key"]
                reasons.append(f"GATILHO SEMÂNTICO (LLM Local): Ação instintiva '{semantic_action}' ({reflex_response['reasoning']})")
                confidence = 1.0 # Sem dúvida!
            elif reflex_response.get("action") == "dilemma":
                confidence = 0.2
                reasons.append("Visão 2D semântica não encontrou padrão claro (Dilema!)")
        
        # Resultado da Percepção
        result = {
            "timestamp": datetime.now().isoformat(),
            "confidence": round(confidence, 2),
            "dilemma_triggered": confidence < self.confidence_threshold,
            "instinctive_notes": reasons,
            "semantic_action": semantic_action,
            "mode": "SYSTEM_1_HEURISTICS"
        }
        
        return result

# Singleton do Sistema 1
system1 = HeuristicSystem1()

def run_heuristic_perception(module: str, function: str, params: dict) -> dict:
    """Entry point para o Neural Bridge acionar o Sistema 1."""
    return system1.analyze_input(module, function, params)
