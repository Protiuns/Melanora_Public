"""
Neural Topology Engine (Public v1.0)
Maps the public architecture of Melanora, ensuring modularity and 
consistency across different environments.
"""

from pathlib import Path
import os
import sys

# The root directory is where main.py lives
ROOT_DIR = Path(__file__).resolve().parent.parent

class NeuralTopology:
    # Public Areas
    AREAS = {
        "CORE": "core",
        "ENVIRONMENTS": "environments",
        "DOCS": "docs"
    }
    
    # Capacities (Functional Paths)
    CAPACITIES = {
        "Ollama": ("ENVIRONMENTS", "ollama"),
        "OllamaBin": ("ENVIRONMENTS", "ollama/bin/ollama.exe"),
        "OllamaModels": ("ENVIRONMENTS", "ollama/models")
    }
    
    @classmethod
    def get_path(cls, capacity_id: str) -> Path:
        """Resolves the absolute physical path for a system capacity."""
        if capacity_id not in cls.CAPACITIES:
            raise KeyError(f"Capacity not recognized in Public Topology: {capacity_id}")
            
        area_id, sub_path = cls.CAPACITIES[capacity_id]
        if area_id not in cls.AREAS:
             raise KeyError(f"Area not recognized in Public Topology: {area_id}")
             
        return ROOT_DIR / cls.AREAS[area_id] / sub_path

# Global Helper
def get_path(capacity_id: str) -> Path:
    return NeuralTopology.get_path(capacity_id)
