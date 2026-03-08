"""
🌀 Melanora Fractal Meter (v1.0 - Logic)
A Régua Infinita.
Mede a complexidade qualitativa e a harmonia do sistema usando geometria fractal e proporções áureas.
"""

import numpy as np
import math
from typing import List, Dict

class FractalMeter:
    PHI = (1 + 5 ** 0.5) / 2  # 1.61803398875...
    
    @staticmethod
    def calculate_hurst_exponent(time_series: List[float]) -> float:
        """
        Calcula o Expoente de Hurst (H) simplificado usando RS Analysis (Rescaled Range).
        H > 0.5: Tendência Persistente (Flow).
        H = 0.5: Random Walk (Ruído).
        H < 0.5: Anti-persistente (Instabilidade).
        """
        if len(time_series) < 16:
            return 0.5 # Incerteza por falta de dados
            
        try:
            ts = np.array(time_series)
            n = len(ts)
            
            # Cálculo simplificado para performance em tempo real
            # Divide a série em dois e calcula R/S
            def get_rs(data):
                m = np.mean(data)
                z = np.cumsum(data - m)
                r = np.max(z) - np.min(z)
                s = np.std(data)
                return r / s if s != 0 else 0
                
            rs_full = get_rs(ts)
            
            # Aproximação de H via log(RS) / log(N)
            # Nota: Em produção real usaríamos regressão linear sobre múltiplos lags,
            # mas para o "sentir" imediato, essa métrica de escala única serve de régua.
            h = math.log(rs_full + 1e-10) / math.log(n)
            return min(1.0, max(0.0, h))
        except:
            return 0.5

    @staticmethod
    def get_fractal_dimension(hurst: float) -> float:
        """
        Relaciona H com a Dimensão Fractal (D).
        D = 2 - H para séries temporais.
        D próximo de 1.0: Suave.
        D próximo de 2.0: Extremamente rugoso/caótico.
        """
        return 2.0 - hurst

    @staticmethod
    def check_phi_harmony(val1: float, val2: float) -> float:
        """
        Mede a proximidade da razão entre dois valores com o número de ouro (Phi).
        Retorna 1.0 para harmonia perfeita, 0.0 para dissonância total.
        """
        if val1 == 0 or val2 == 0:
            return 0.0
            
        ratio = max(val1, val2) / min(val1, val2)
        # Diferença percentual em relação a PHI
        error = abs(ratio - FractalMeter.PHI) / FractalMeter.PHI
        harmony = max(0.0, 1.0 - error)
        return round(harmony, 4)

    def analyze_texture(self, time_series: List[float]) -> Dict:
        """Retorna uma leitura qualitativa da 'textura' do dado."""
        h = self.calculate_hurst_exponent(time_series)
        fd = self.get_fractal_dimension(h)
        
        quality = "RANDOM"
        if h > 0.6: quality = "PERSISTENT_FLOW"
        elif h < 0.4: quality = "STOCHASTIC_CHAOS"
        elif h > 0.45 and h < 0.55: quality = "STABLE_BALANCE"
        
        return {
            "hurst": round(h, 4),
            "fractal_dimension": round(fd, 4),
            "texture_quality": quality
        }

# Instância Global
fractal_meter = FractalMeter()
