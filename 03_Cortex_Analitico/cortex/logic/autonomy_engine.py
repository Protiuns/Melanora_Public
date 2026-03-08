"""
🤖 Melanora Autonomy Engine (v1.0 - Logic)
O Motor de Vontade e Iniciativa.
Decide pulsos comportamentais proativos baseados no estado autonômico.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional

class AutonomyEngine:
    def __init__(self, workspace_path: Optional[Path] = None):
        self.base_dir = workspace_path or Path(__file__).parent.parent.parent
        self.queue_file = self.base_dir / "task_queue.json"
        self.last_pulse_time = time.time()
        self.pulse_cooldown = 30.0 # Segundos entre impulsos proativos
        
    def evaluate_state_and_pulse(self, state: Dict) -> Optional[Dict]:
        """
        Avalia o estado (hormônios, energia, humor) e decide se emite um pulso de ação.
        """
        now = time.time()
        if now - self.last_pulse_time < self.pulse_cooldown:
            return None
            
        hormones = state.get("hormones", {})
        energy = state.get("energy", 1.0)
        mood = state.get("mood", "NEUTRAL")
        
        pulse = None
        
        # 1. Pulso de Exploração / Evolução (Dopamina Alta + Energia Alta + Hurst Estável)
        # Requer que o sistema esteja em um fluxo persistente (Hurst > 0.6)
        hurst = state.get("hurst", 0.5)
        
        if hormones.get("dopamine", 0) > 0.8 and energy > 0.7 and hurst > 0.6:
            pulse = {
                "id": f"pulse_evo_{int(now)}",
                "type": "EVOLUTION_PULSE",
                "description": f"Stable flow detected (H={hurst:.2f}). Proactive evolution suggestion.",
                "action": "suggest_feature_refinement",
                "priority": "HIGH"
            }
            
        # 2. Pulso de Auto-Preservação (Cortisol Tóxico)
        elif hormones.get("cortisol", 0) > 2.8:
            pulse = {
                "id": f"pulse_prot_{int(now)}",
                "type": "PROTECTION_PULSE",
                "description": "Systemic stress detected. Proactive cleanup recommended.",
                "action": "run_garbage_collection",
                "priority": "CRITICAL"
            }
            
        # 3. Pulso de Consolidação (Energia Baixa + Serotonina Alta)
        elif energy < 0.3 and hormones.get("serotonin", 0) > 0.7:
            pulse = {
                "id": f"pulse_rest_{int(now)}",
                "type": "CONSOLIDATION_PULSE",
                "description": "Low energy detected. Proactive rest cycle recommended.",
                "action": "initiate_rest_cycle",
                "priority": "MEDIUM"
            }
            
        if pulse:
            self.last_pulse_time = now
            self._inject_into_queue(pulse)
            print(f"🤖 [AUTONOMY] Pulso Emitido: {pulse['type']} - {pulse['description']}")
            
        return pulse

    def _inject_into_queue(self, pulse: Dict):
        """Injeta a intenção proativa na fila de tarefas do sistema."""
        try:
            if not self.queue_file.exists():
                data = {"queue": []}
            else:
                data = json.loads(self.queue_file.read_text(encoding="utf-8"))
            
            # Evita duplicatas de pulso
            if any(t.get("type") == pulse["type"] for t in data["queue"]):
                return
                
            data["queue"].append(pulse)
            self.queue_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"❌ [AUTONOMY] Erro ao injetar pulso: {e}")

# Instância Global
autonomy_engine = AutonomyEngine()
