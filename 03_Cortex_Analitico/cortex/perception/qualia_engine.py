"""
🎨 Melanora Qualia Engine (v1.0 - Perception)
Motor de Tradução Sensorial-Aestética.
Converte padrões visuais (cores, brilho, harmonia) em estímulos hormonais.
"""

import cv2
import numpy as np
import time
from typing import Dict

class QualiaEngine:
    def __init__(self):
        self.last_qualia = {}
        
    def extract_visual_qualia(self, img) -> Dict[str, float]:
        """
        Analisa a imagem e extrai vetores de 'sentimento visual'.
        """
        if img is None: return {}
        
        # Converter para HSV para análise de cor e brilho
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # 1. Luminosidade Média (Alertness)
        avg_v = np.mean(v) / 255.0
        
        # 2. Saturação (Vibrancy / Dopamine)
        avg_s = np.mean(s) / 255.0
        
        # 3. Dominância de Cores
        # Matiz (Hue) vai de 0 a 180 em OpenCV
        hist_h = cv2.calcHist([h], [0], None, [180], [0, 180])
        
        # Definindo zonas emocionais de cor
        # Vermelhos (0-10, 170-180) -> Adrenaline
        # Verdes (40-80) -> Serotonin
        # Azuis (100-140) -> Conviction/Focus
        red_mass = np.sum(hist_h[0:10]) + np.sum(hist_h[170:180])
        green_mass = np.sum(hist_h[40:80])
        blue_mass = np.sum(hist_h[100:140])
        
        total = np.sum(hist_h) + 1e-6
        
        qualia = {
            "brightness": round(float(avg_v), 3),
            "vibrancy": round(float(avg_s), 3),
            "red_dominance": round(float(red_mass / total), 3),
            "green_dominance": round(float(green_mass / total), 3),
            "blue_dominance": round(float(blue_mass / total), 3),
            "timestamp": time.time()
        }
        
        self.last_qualia = qualia
        return qualia

    def calculate_hormonal_shift(self, qualia: Dict[str, float]) -> Dict[str, float]:
        """
        Traduz as qualidades visuais em deltas hormonais.
        """
        shifts = {
            "dopamine": (qualia["vibrancy"] * 0.05) + (qualia["green_dominance"] * 0.02),
            "cortisol": (qualia["brightness"] * 0.02) if qualia["brightness"] > 0.8 else -0.01,
            "adrenaline": (qualia["red_dominance"] * 0.08) + (max(0, qualia["brightness"] - 0.7) * 0.05),
            "serotonin": (qualia["blue_dominance"] * 0.03) + (qualia["green_dominance"] * 0.05),
            "oxytocin": 0.0 # Oxitocina é social, não puramente visual por enquanto
        }
        return shifts

# Instância Global
qualia_engine = QualiaEngine()
