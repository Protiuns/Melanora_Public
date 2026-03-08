"""
🎭 Melanora Subjectivity Engine (v1.0)
Gerenciador de Matriz Endócrina Artificial e Interocepção.
Traduz métricas de hardware e eventos GWT em "estados de humor" e "convicção".
"""

import json
import time
import sys
from pathlib import Path
from dataclasses import dataclass, asdict

# Adicionar o diretório pai ao sys.path para importar módulos irmãos
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from hardware_profiler import detect_cpu, detect_ram
except ImportError:
    def detect_cpu(): return {"usage_percent": 0}
    def detect_ram(): return {"used_percent": 0}

# Mock GWT if not present
try:
    from cortex.logic.global_workspace import workspace, EventTypes
except ImportError:
    workspace = None
    class EventTypes:
        TOKEN_CRITICAL = "TOKEN_CRITICAL"
        TASK_SUCCESS = "TASK_SUCCESS"
        TASK_FAIL = "TASK_FAIL"
        USER_APPROVE = "USER_APPROVE"

try:
    from cortex.logic.resonance_analyzer import ResonanceAnalyzer
except ImportError:
    ResonanceAnalyzer = None

@dataclass
class HormoneMatrix:
    dopamine: float = 0.5   # Recompensa / Foco / Confiança
    cortisol: float = 0.2    # Estresse / Alerta / Rigor
    oxytocin: float = 0.3    # Conexão / Estabilidade / Memória
    conviction: float = 0.8  # Harmonia Global (Consonância vs Dissonância)

class SubjectivityEngine:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "config"
        self.state_file = self.config_dir / "subjective_state.json"
        self.matrix = HormoneMatrix()
        self.last_update = time.time()
        self.resonance_analyzer = ResonanceAnalyzer() if ResonanceAnalyzer else None
        
        # Carregar estado anterior se existir
        self._load_state()

        # Subscreve aos eventos do GWT
        if workspace:
            workspace.subscribe("subjectivity_engine", self._on_neural_event)

    def _load_state(self):
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                self.matrix = HormoneMatrix(**data.get("matrix", {}))
            except:
                pass

    def _save_state(self):
        state = {
            "matrix": asdict(self.matrix),
            "last_update": self.last_update,
            "mood_label": self.get_mood_label()
        }
        self.state_file.write_text(json.dumps(state, indent=2))

    def update_interoception(self, metrics=None):
        """Lê sinais 'físicos' do sistema."""
        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        # 1. Decaimento Natural (Homeostase Hormonal)
        self.matrix.dopamine = self._approach(self.matrix.dopamine, 0.5, dt * 0.01)
        self.matrix.cortisol = self._approach(self.matrix.cortisol, 0.2, dt * 0.005)
        self.matrix.oxytocin = self._approach(self.matrix.oxytocin, 0.3, dt * 0.002)

        # 2. Processamento de Métricas Físicas Autônomas (Se não houver injeção externa)
        if metrics is None:
            try:
                cpu = detect_cpu()
                ram = detect_ram()
                metrics = {
                    "cpu_usage": cpu.get("usage_percent", 0),
                    "ram_usage": ram.get("used_percent", 0)
                }
                # Converter "N/A" ou strings em 0 se necessário
                for k, v in metrics.items():
                    if not isinstance(v, (int, float)): metrics[k] = 0
            except:
                metrics = {"cpu_usage": 0, "ram_usage": 0}

        # 3. Aplicar Tensão de Sistema ao Cortisol
        cpu_usage = metrics.get("cpu_usage", 0)
        if cpu_usage > 70:
            self.matrix.cortisol += 0.02 * (cpu_usage / 100)
        
        ram_usage = metrics.get("ram_usage", 0)
        if ram_usage > 85:
            self.matrix.cortisol += 0.03

        # 3. Cálculo de Convicção (Baseado na harmonia entre Dopamina e Cortisol)
        harmony = (self.matrix.dopamine * (1.2 - self.matrix.cortisol))
        self.matrix.conviction = max(0.0, min(1.0, harmony))

        # 4. Global Broadcast (Fase 2)
        if workspace and dt > 1.0: # Evitar spam, broadcast a cada ~1s
            workspace.publish(
                source="subjectivity_engine",
                event_type="MOOD_SHIFT",
                data={
                    "matrix": asdict(self.matrix),
                    "label": self.get_mood_label()
                },
                salience=0.4 if self.matrix.cortisol < 0.6 else 0.8,
                tags=["hormones", "qualia"]
            )

        self._save_state()
        return asdict(self.matrix)

    def _approach(self, current, target, step):
        if current < target:
            return min(target, current + step)
        return max(target, current - step)

    def _on_neural_event(self, event):
        """Reage a eventos do Global Workspace."""
        if event.event_type == EventTypes.TASK_SUCCESS:
            self.matrix.dopamine += 0.15
            self.matrix.cortisol -= 0.05
        elif event.event_type == EventTypes.TASK_FAIL:
            self.matrix.cortisol += 0.20
            self.matrix.dopamine -= 0.10
        elif event.event_type == EventTypes.TOKEN_CRITICAL:
            self.matrix.cortisol += 0.30
        elif event.event_type == "USER_APPROVE":
            self.matrix.oxytocin += 0.20
            self.matrix.dopamine += 0.10
        
        # Limitar valores entre 0 e 1
        for field in ["dopamine", "cortisol", "oxytocin"]:
            val = getattr(self.matrix, field)
            setattr(self.matrix, field, max(0.0, min(1.0, val)))
        
        # Fase 4: Atualizar Convicção via Ressonância
        if self.resonance_analyzer and event.data:
            resonance = self.resonance_analyzer.calculate_resonance(event.data, asdict(self.matrix))
            # Ajustar a convicção baseada na harmonia do evento
            self.matrix.conviction = self._approach(self.matrix.conviction, resonance, 0.2)

        self.update_interoception()

    def get_mood_label(self):
        """Traduz a matriz hormonal em um rótulo compreensível."""
        c = self.matrix.cortisol
        d = self.matrix.dopamine
        o = self.matrix.oxytocin

        if c > 0.6: return "ANALÍTICO_RESTRITO (Stress Alto)"
        if d > 0.7: return "MODO_FLOW (Alta Confiança)"
        if o > 0.7: return "SIMBIÓTICO_PROFUNDO (Conexão Forte)"
        if c < 0.3 and d < 0.3: return "MEDITAÇÃO / HIBERNAÇÃO"
        return "STABLE (Harmonia Padrão)"

    def get_biases(self):
        """Retorna modificadores para a Neural Bridge."""
        return {
            "temperature_delta": -0.2 if self.matrix.cortisol > 0.5 else 0.0,
            "strict_auditing": self.matrix.cortisol > 0.4,
            "creativity_boost": self.matrix.dopamine > 0.6,
            "memory_depth": 1.0 + (self.matrix.oxytocin * 0.5)
        }

if __name__ == "__main__":
    engine = SubjectivityEngine()
    print(f"Humor Inicial: {engine.get_mood_label()}")
    print(f"Matriz: {engine.update_interoception()}")
