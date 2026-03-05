"""
🧮 Melanora Advanced Calculator (v1.0)
Motor matemático de alta performance para o modelo PRTM v4.1.
Focado em álgebra linear e funções de ativação sináptica (Zero-Dep).
"""

import math
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

@cortex_function
def compute_synaptic_activation(weights: list[float], intensities: list[float]) -> float:
    """Calcula a ativação combinada de uma sub-rede (Dot Product simplificado)."""
    if len(weights) != len(intensities):
        return 0.0
    
    # Soma ponderada
    dot = sum(w * i for w, i in zip(weights, intensities))
    
    # Ativação via Sigmoide (Logística) para normalização entre 0 e 1
    return 1 / (1 + math.exp(-dot))

@cortex_function
def compute_softmax(values: list[float]) -> list[float]:
    """Normaliza um conjunto de energias para que a soma seja 1.0."""
    if not values: return []
    
    # Estabilidade numérica: subtrair o máximo
    max_val = max(values)
    exp_values = [math.exp(v - max_val) for v in values]
    total_exp = sum(exp_values)
    
    return [round(v / total_exp, 4) for v in exp_values]

@cortex_function
def vector_distance(v1: list[float], v2: list[float], p: int = 2) -> float:
    """Calcula a distância (Minkowski) entre dois estados neurais (P=2 é Euclidiana)."""
    if len(v1) != len(v2): return -1.0
    
    sum_diff = sum(abs(a - b) ** p for a, b in zip(v1, v2))
    return round(sum_diff ** (1/p), 6)

@cortex_function
def validate_hypothesis_probability(evidence_weight: float, prior_probability: float = 0.5) -> float:
    """
    Usa Teorema de Bayes simplificado para validar uma hipótese da LLM.
    Newton: Este é o 'validador' que você pediu para a mente física.
    """
    # P(H|E) = (P(E|H) * P(H)) / P(E)
    # Aqui usamos o evidence_weight como P(E|H)
    likelihood = edge_clip(evidence_weight)
    
    # Probabilidade marginal P(E) estimada
    marginal = (likelihood * prior_probability) + (0.5 * (1 - prior_probability))
    
    posterior = (likelihood * prior_probability) / marginal
    return round(posterior, 4)

def edge_clip(val, min_v=0.01, max_v=0.99):
    return max(min_v, min(max_v, val))
