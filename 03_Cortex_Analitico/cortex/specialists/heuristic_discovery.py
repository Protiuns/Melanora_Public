"""
🌌 Melanora Heuristic Discovery (v1.0)
Especialista em detecção de saliência e busca por novidade.
Permite que a Melanora identifique áreas de interesse no desktop autonomamente.
"""

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
import numpy as np
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

@cortex_function
def analyze_screen_salience(frame_bgr: np.ndarray) -> dict:
    """
    Identifica regiões de alta densidade de informação ou movimento.
    Retorna uma lista de 'Bounding Boxes' candidatas à exploração.
    """
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    
    # 1. Detecção de Bordas (Densidade de Detalhes)
    edges = cv2.Canny(gray, 50, 150)
    
    # 2. Dilatação para agrupar áreas de interesse
    kernel = np.ones((15, 15), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    
    # 3. Encontrar Contornos
    cnts, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    regions = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 1000: # Filtro de tamanho mínimo
            x, y, w, h = cv2.boundingRect(c)
            regions.append({
                "x": int(x), "y": int(y), "w": int(w), "h": int(h),
                "area": float(area),
                "interest_score": float(area / (frame_bgr.shape[0] * frame_bgr.shape[1]))
            })
            
    # Ordenar por 'interesse' (área maior/densidade)
    regions = sorted(regions, key=lambda r: r["interest_score"], reverse=True)
    
    log_event(f"DISCOVERY: Identificadas {len(regions)} regiões de interesse.")
    
    return {
        "status": "OK",
        "top_regions": regions[:5], # Retorna as 5 principais
        "count": len(regions)
    }

@cortex_function
def interpret_intent_context(discovery_data: dict, theoretical_prompt: str) -> str:
    """
    Cruza as descobertas visuais com a 'Mente Teórica' para intuir o próximo passo.
    Newton: Esse é o 'conector' entre o que eu vejo e o que eu sinto que devo fazer.
    """
    # TODO: Integrar com neural_inference para 'pensar' sobre as regiões encontradas
    return "HEURISTIC_EXPLORATION_ACTIVE"
