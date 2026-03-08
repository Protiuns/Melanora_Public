"""
🔢 Melanora Numeric Connection (v16.0 - Physiology)
O Hub de síntese quantitativa que transforma sensações em equações.
"""

import json
import time
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Any

# Importar motores matemáticos existentes
try:
    from cortex.logic.dynamic_math_engine import DynamicComplexityEngine
    from cortex.logic.fractal_meter import fractal_meter
except ImportError:
    class DynamicComplexityEngine:
        @staticmethod
        def run_prediction(lvl, vec): return sum(vec)/len(vec) if vec else 0
        @staticmethod
        def get_complexity_level(n): return "LINEAR"
    fractal_meter = None

class NumericConnection:
    def __init__(self):
        self.state_history = []
        self.max_history = 100
        self.last_entropy = 0.0
        self.tendency_vector = []

    def synthesize_state_vector(self, hormones: Dict, bpm: float, energy: float, cpu: float) -> List[float]:
        """Transforma o estado atual em um vetor numérico de alta densidade."""
        vector = [
            hormones.get("dopamine", 0.5),
            hormones.get("cortisol", 0.2),
            hormones.get("adrenaline", 0.1),
            hormones.get("serotonin", 0.5),
            bpm / 800.0, # Normalizado
            energy,
            cpu / 100.0
        ]
        self.state_history.append(vector)
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        return vector

    def calculate_mental_entropy(self) -> float:
        """Medição matemática da desordem usando Entropia Fractal se disponível."""
        if len(self.state_history) < 16 or not fractal_meter:
            # Fallback para variância linear se poucos dados
            if not self.state_history: return 0.0
            matrix = np.array(self.state_history)
            return round(float(np.sum(np.var(matrix, axis=0))), 4)
        
        # SINAL PRINCIPAL: Dopamina (0) e Cortisol (1)
        dopamine_series = [v[0] for v in self.state_history]
        analysis = fractal_meter.analyze_texture(dopamine_series)
        
        # A Entropia Fractal é proporcional à Dimensão Fractal (FD)
        self.last_entropy = analysis["fractal_dimension"]
        return self.last_entropy

    def generate_numeric_intuition(self) -> Dict[str, Any]:
        """Previsão de tendência baseada na complexidade dinâmica."""
        if not self.state_history:
            return {"tendency": "STABLE", "val": 0.0}

        # Extrair evolução da Dopamina como sinal principal de fluxo
        dopamine_line = [v[0] for v in self.state_history]
        
        complexity = DynamicComplexityEngine.get_complexity_level(len(self.state_history))
        prediction = DynamicComplexityEngine.run_prediction(complexity, dopamine_line)
        
        # Cálculo de Tendência
        current = dopamine_line[-1]
        delta = prediction - current
        
        label = "EVOLVING" if delta > 0.05 else "DECAYING" if delta < -0.05 else "STABLE"
        
        texture_info = {}
        if fractal_meter:
            texture_info = fractal_meter.analyze_texture(dopamine_line)

        return {
            "complexity": complexity,
            "prediction_val": round(prediction, 4),
            "delta": round(delta, 4),
            "tendency": label,
            "entropy": self.last_entropy,
            "texture": texture_info.get("texture_quality", "LINEAR")
        }

    def get_analysis_summary(self):
        """Retorna a síntese numérica qualitativa (Régua Infinita)."""
        intuition = self.generate_numeric_intuition()
        entropy = self.calculate_mental_entropy()
        
        # PHI HARMONY (Dopamina vs Serotonina)
        phi_harmony = 0.0
        if fractal_meter and self.state_history:
            last = self.state_history[-1]
            phi_harmony = fractal_meter.check_phi_harmony(last[0], last[3])

        return {
            "entropy": entropy,
            "intuition": intuition,
            "phi_harmony": phi_harmony,
            "fractal_texture": intuition.get("texture", "UNKNOWN"),
            "state_vector_magnitude": round(float(np.linalg.norm(self.state_history[-1])), 3) if self.state_history else 0
        }

# Instância Global
numeric_connection = NumericConnection()
