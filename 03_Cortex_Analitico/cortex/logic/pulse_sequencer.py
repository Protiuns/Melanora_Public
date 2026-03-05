"""
🧬 Synaptic Pulse Sequencer v1.0
Orquestra o tempo e a ordem das disparos neurais para evitar sobrecarga do sistema.
Implementa o conceito de 'Ativação Esparsa' (Sparse Activation).
"""

import time
import threading
from pathlib import Path
from datetime import datetime

class PulseSequencer:
    # Grupos de Ativação (Maior Prioridade -> Menor Prioridade)
    GROUPS = {
        "CORE": {"priority": 1.0, "delay_after": 1.5},
        "INFRA": {"priority": 0.8, "delay_after": 1.0},
        "SECURITY": {"priority": 0.9, "delay_after": 0.5},
        "SPECIALIST": {"priority": 0.6, "delay_after": 0.2},
        "PERIPHERAL": {"priority": 0.4, "delay_after": 0.1}
    }

    def __init__(self):
        self._lock = threading.Lock()
        self.active_groups = set()
        self.load_factor = 0.0

    def sequence_activation(self, tool_id: str, group: str = "SPECIALIST"):
        """Agenda a ativação de uma ferramenta seguindo o sequenciamento sináptico."""
        group_meta = self.GROUPS.get(group, self.GROUPS["SPECIALIST"])
        
        with self._lock:
            # Simulando respiro sináptico se a carga estiver alta
            if self.load_factor > 0.8:
                wait_time = 1.0 * group_meta["priority"]
                print(f"[PULSE] Carga Alta ({self.load_factor*100:.1f}%). Aguardando {wait_time}s para {tool_id}...")
                time.sleep(wait_time)

            print(f"[PULSE] Ativando sequencia: {tool_id} (Grupo: {group})")
            self.active_groups.add(tool_id)
            self.load_factor += 0.1 # Incremento nominal de carga
            
            # Delay de estabilização pós-ativação
            time.sleep(group_meta["delay_after"])

    def release_pulse(self, tool_id: str):
        """Libera a carga de uma ferramenta após a conclusão."""
        with self._lock:
            if tool_id in self.active_groups:
                self.active_groups.remove(tool_id)
                self.load_factor = max(0.0, self.load_factor - 0.1)
                print(f"[PULSE] Pulso liberado: {tool_id}. Carga atual: {self.load_factor*100:.1f}%")

# Singleton Instance
sequencer = PulseSequencer()

def get_sequencer():
    return sequencer
