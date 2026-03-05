"""
🧮 Melanora Match Module (v1.0 - StdLib Edition)
Operações matemáticas rápidas para o Córtex Analítico.
"""

import math
from cortex.utils.cortex_utils import cortex_function

@cortex_function
def fast_energy_sum(energies: list[float]) -> float:
    """Soma rápida de energias sinápticas."""
    return sum(energies)

@cortex_function
def calculate_norm(vector: list[float]) -> float:
    """Calcula a norma euclidiana de um vetor de energia."""
    return math.sqrt(sum(x*x for x in vector))

@cortex_function
def softmax_normalization(values: list[float]) -> list[float]:
    """Normalização Softmax para distribuição de energia."""
    if not values: return []
    max_val = max(values)
    exp_values = [math.exp(x - max_val) for x in values]
    sum_exp = sum(exp_values)
    return [x / sum_exp for x in exp_values]

@cortex_function
def logistic_activation(x: float, k: float = 1.0, x0: float = 0.5) -> float:
    """Função logística para ativação de agentes."""
    return 1 / (1 + math.exp(-k * (x - x0)))

@cortex_function
def high_frequency_ping(n: int = 1000) -> dict:
    """Teste de latência de loop matemático local."""
    import time
    start = time.time()
    for i in range(n):
        _ = math.sqrt(i) * math.sin(i)
    elapsed = time.time() - start
    return {
        "iterations": n,
        "total_time_ms": round(elapsed * 1000, 3),
        "freq_hz": round(n / elapsed, 1) if elapsed > 0 else "inf"
    }
