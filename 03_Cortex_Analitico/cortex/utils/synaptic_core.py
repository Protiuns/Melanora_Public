import json
import os
from pathlib import Path
from typing import Dict, Optional

# Caminho para persistência das sinapses individuais
SYNAPSE_BASE_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico/config/synapses")

class NeuralNode:
    """
    Representa um único nó neural (neurônio) autônomo.
    Gerencia seu próprio potencial de ação, limiar e decaimento.
    """
    def __init__(self, node_id: str, threshold: float = 100.0, decay_rate: float = 0.05):
        self.node_id = node_id
        self.threshold = threshold
        self.decay_rate = decay_rate
        self.potential = 0.0
        self.state_file = SYNAPSE_BASE_DIR / f"{node_id}.json"
        self.load_state()

    def load_state(self):
        """Carrega o potencial persistente do disco."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.potential = data.get("potential", 0.0)
            except Exception:
                self.potential = 0.0

    def save_state(self):
        """Salva o potencial atual para persistência."""
        SYNAPSE_BASE_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump({"potential": self.potential, "last_update": os.path.getmtime(self.state_file) if self.state_file.exists() else 0}, f)
        except Exception:
            pass

    def charge(self, amount: float):
        """Aplica uma carga ao neurônio e processa o decaimento passivo."""
        # Decaimento passivo antes de aplicar nova carga (Leakage)
        self.potential *= (1.0 - self.decay_rate)
        
        self.potential += amount
        self.save_state()

    def evaluate_firing(self) -> bool:
        """Verifica se o neurônio atingiu o limiar de disparo."""
        if self.potential >= self.threshold:
            self.potential -= self.threshold # Disparo! Mantém o excedente.
            self.save_state()
            return True
        return False

class SynapticCore:
    """Roteador para os NeuralNodes descentralizados."""
    _nodes: Dict[str, NeuralNode] = {}

    @classmethod
    def get_node(cls, node_id: str) -> NeuralNode:
        if node_id not in cls._nodes:
            cls._nodes[node_id] = NeuralNode(node_id)
        return cls._nodes[node_id]

    @classmethod
    def charge_and_check(cls, node_id: str, amount: float) -> bool:
        """Interface simplificada para carregar e verificar disparo."""
        node = cls.get_node(node_id)
        node.charge(amount)
        return node.evaluate_firing()
