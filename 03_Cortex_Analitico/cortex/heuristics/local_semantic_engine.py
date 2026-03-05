"""
🧠 Heurística Semântica Local (Sistema 1b)
Recebe as geometrias extraídas do Sistema 1a (OpenCV) e toma decisões imediatas.
Atua como um 'LLM Local/Regras Rápidas' para reflexos instantâneos.
"""

import json
import time
import logging

try:
    from cortex.motor.virtual_actuators import physical_press
except ImportError:
    def physical_press(key): pass

class LocalSemanticEngine:
    def __init__(self):
        self.last_snake_head = None
        self.last_direction = None
    
    def process_snake_scene(self, scene_data: dict) -> dict:
        """
        Interpretação heurística ultra-rápida.
        scene_data = {"entities": [...]}
        Retorna uma ação imediata (ex: press_key) se a heurística estiver confiante.
        """
        entities = scene_data.get("entities", [])
        green_masses = [e for e in entities if e["type"] == "green_mass"]
        red_masses = [e for e in entities if e["type"] == "red_mass"]
        
        if not green_masses:
            return {"confidence": 0.0, "action": "none"}
            
        # Simplificação extema: assume que a cabeça da cobra é o maior/mais ativo bloco verde
        # ou apenas tentamos achar a maçã e virar para ela.
        head = green_masses[0]["bbox"] # x, y, w, h
        
        # Onde está a maçã?
        if red_masses:
            apple = red_masses[0]["bbox"]
            dx = apple[0] - head[0]
            dy = apple[1] - head[1]
            
            # Reflexo direcional simples
            action = "none"
            if abs(dx) > abs(dy):
                # Move horizontal
                action = "ArrowRight" if dx > 0 else "ArrowLeft"
            else:
                # Move vertical
                action = "ArrowDown" if dy > 0 else "ArrowUp"
                
            # Dispara a ação física real através do Córtex Motor
            physical_press(action)
                
            return {
                "confidence": 0.9, 
                "action": "press_key", 
                "key": action,
                "reasoning": f"Maçã detectada em rel offset ({dx}, {dy}). Tecla {action} pressionada fisicamente."
            }
            
        # Se não há maçã visível, continua reto ou aciona Dilema
        return {
            "confidence": 0.3,
            "action": "dilemma",
            "reasoning": "Não vejo a maçã, ou estado ambíguo."
        }

semantic_engine = LocalSemanticEngine()

def run_semantic_reflex(scene_data: dict) -> dict:
    return semantic_engine.process_snake_scene(scene_data)
