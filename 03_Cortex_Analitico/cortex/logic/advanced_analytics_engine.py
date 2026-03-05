"""
📉 Motor Analítico Avançado
Responsável por realizar cálculos complexos em cima de dados tabulares ou geométricos.
Gera estatísticas comparativas, calcula proporções (ex: espaço livre vs obstáculos)
e mantém a memória estatística das falhas e sucessos passados.
"""

import math
import logging
import json
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ANALYTICS] %(message)s")

class AdvancedAnalyticsEngine:
    def __init__(self, memory_size=50):
        # Memória das últimas N ações e seus desfechos (0.0 = Falha Total, 1.0 = Sucesso)
        # Formato: {"scenario_hash": "...", "action": "ArrowUp", "success_rate": 0.8, "attempts": 5}
        self.statistical_memory = {}
        # Histórico puramente cronológico
        self.action_history = deque(maxlen=memory_size)
        
    def calculate_space_proportions(self, entities, resolution=(400, 400)):
        """
        Recebe as massas 2D da cena e tenta calcular proporções numéricas.
        Retorna dicionário com % de área ocupada e distâncias críticas.
        """
        if not entities:
            return {"occupied_ratio": 0.0, "density": "empty"}
            
        total_area = resolution[0] * resolution[1]
        occupied = 0
        head_pos = None
        target_pos = None
        
        for e in entities:
            occupied += e.get("area", 0)
            if e.get("type") == "green_mass" and head_pos is None: # Assumir a primeira verde como a cobra
                # Central point of bounding box [x, y, w, h]
                bbox = e["bbox"]
                head_pos = (bbox[0] + bbox[2]/2, bbox[1] + bbox[3]/2)
            elif e.get("type") == "red_mass" and target_pos is None:
                bbox = e["bbox"]
                target_pos = (bbox[0] + bbox[2]/2, bbox[1] + bbox[3]/2)
                
        # Proporção de ocupação
        occupied_ratio = min(1.0, occupied / total_area if total_area > 0 else 0)
        
        # Geometria comparativa
        data = {
            "occupied_ratio": round(occupied_ratio, 4),
            "density": "high" if occupied_ratio > 0.2 else "low",
        }
        
        if head_pos and target_pos:
            dist = math.hypot(target_pos[0] - head_pos[0], target_pos[1] - head_pos[1])
            data["distance_to_target"] = round(dist, 2)
            
            # Cálculo de vetores propostos
            data["dx"] = target_pos[0] - head_pos[0]
            data["dy"] = target_pos[1] - head_pos[1]
            
        return data

    def hash_scenario(self, proportions):
        """Cria um hash numérico simplificado do cenário para bater com a memória."""
        dens = proportions.get("density", "unknown")
        # Simplifica dx e dy em quadrantes
        dx = proportions.get("dx", 0)
        dy = proportions.get("dy", 0)
        quadX = "pos" if dx > 0 else "neg" if dx < 0 else "zero"
        quadY = "pos" if dy > 0 else "neg" if dy < 0 else "zero"
        return f"{dens}_{quadX}_{quadY}"

    def record_outcome(self, scenario_data, action: str, success: float):
        """Salva a eficácia de uma ação tomada num determinado cenário estatístico."""
        scenario_hash = self.hash_scenario(scenario_data)
        key = f"{scenario_hash}_{action}"
        
        if key not in self.statistical_memory:
            self.statistical_memory[key] = {"success_rate": success, "attempts": 1}
        else:
            mem = self.statistical_memory[key]
            # Média móvel simples
            mem["success_rate"] = ((mem["success_rate"] * mem["attempts"]) + success) / (mem["attempts"] + 1)
            mem["attempts"] += 1
            
        self.action_history.append({"hash": scenario_hash, "action": action, "success": success})

    def evaluate_risk(self, scenario_data, proposed_action: str) -> dict:
        """
        Consulta o histórico estatístico e as proporções para devolver
        o nível de Risco (0.0 a 1.0) e uma recomendação.
        """
        proportions = self.calculate_space_proportions(scenario_data.get("entities", []))
        scenario_hash = self.hash_scenario(proportions)
        key = f"{scenario_hash}_{proposed_action}"
        
        risk = 0.5 # Normal
        reasoning = "Sem dados prévios. Risco base."
        
        # 1. Avaliação de Histórico (Análise Estatística Frequentista)
        if key in self.statistical_memory:
            mem = self.statistical_memory[key]
            if mem["attempts"] >= 3:
                risk = 1.0 - mem["success_rate"]
                reasoning = f"Baseado em {mem['attempts']} tentativas, esta ação falha {risk*100:.0f}% das vezes."
                
        # 2. Avaliação de Densidade (Risco Espacial Proporcional)
        if proportions.get("occupied_ratio", 0) > 0.4: # A tela/nível está muito apertada
            risk += 0.3
            reasoning += " | A densidade da fase é alta, chance de colisão elevada."
            
        risk = min(1.0, max(0.0, risk))
        
        return {
            "proposed_action": proposed_action,
            "calculated_risk": round(risk, 2),
            "proportions": proportions,
            "reasoning": reasoning
        }

analytics_engine = AdvancedAnalyticsEngine()

if __name__ == "__main__":
    print("Testando Motor Numérico...")
    fake_scene = {
        "entities": [
            {"type": "green_mass", "bbox": [50, 50, 20, 20], "area": 400},
            {"type": "red_mass", "bbox": [100, 50, 10, 10], "area": 100}
        ]
    }
    props = analytics_engine.calculate_space_proportions(fake_scene["entities"])
    print(f"Proporções: {props}")
    
    analytics_engine.record_outcome(fake_scene, "ArrowRight", 1.0)
    analytics_engine.record_outcome(fake_scene, "ArrowRight", 0.0)
    
    risk = analytics_engine.evaluate_risk(fake_scene, "ArrowRight")
    print(f"Risco da Ação 'ArrowRight': {json.dumps(risk, indent=2)}")
