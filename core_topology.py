"""
Neural Topology Engine v1.0
Mapeia a arquitetura da Mente Física através de Áreas e Capacidades,
eliminando dependência de caminhos hardcoded no sistema cognitivo.
"""

from pathlib import Path
import os
import sys

# O root da mente física é o diretório superior onde melanora.py vive
ROOT_DIR = Path(__file__).resolve().parent

class NeuralTopology:
    AREAS = {
        "THEORETICAL": "00_Mente_Teorica",
        "ENVIRONMENT": "01_Ambientes_Ferramentas",
        "COGNITIVE": "03_Cortex_Analitico",
        "WORKPLACE": "04_Manifestacao_Projetos",
        "EVOLUTION": "03_Cortex_Analitico/cortex/evolution", # Migrada transversalmente
        "VENV": ".venv"
    }
    
    # Capacidades (Diretórios de função dentro das Áreas)
    CAPACITIES = {
        # Cognitive Subsystems
        "Config": ("COGNITIVE", "config"),
        "Logs": ("COGNITIVE", "logs"),
        "Heuristics": ("COGNITIVE", "cortex/heuristics"),
        "Logic": ("COGNITIVE", "cortex/logic"),
        "ProcessIntegrity": ("COGNITIVE", "process_integrity"),
        "StaticUI": ("COGNITIVE", "static"),
        
        # Tools
        "Python": ("VENV", "Scripts/python.exe"),
        "Node": ("ENVIRONMENT", "Node/node.exe"),
    }
    
    @classmethod
    def get_area_path(cls, area_id: str) -> Path:
        """Resolve o caminho físico absoluto de uma Área do sistema."""
        if area_id not in cls.AREAS:
            raise KeyError(f"Área não reconhecida na Topologia Neural: {area_id}")
            
        return ROOT_DIR / cls.AREAS[area_id]

    @classmethod
    def get_capacity_path(cls, capacity_id: str) -> Path:
        """Resolve o caminho absoluto baseado no registro de Capacidades."""
        if capacity_id not in cls.CAPACITIES:
            raise KeyError(f"Capacidade não reconhecida na Topologia Neural: {capacity_id}")
            
        area_id, sub_path = cls.CAPACITIES[capacity_id]
        base_area = cls.get_area_path(area_id)
        return base_area / sub_path

# Helpers expostos globalmente para facilidade de import
def get_path(capacity_id: str) -> Path:
    return NeuralTopology.get_capacity_path(capacity_id)

def get_area(area_id: str) -> Path:
    return NeuralTopology.get_area_path(area_id)
