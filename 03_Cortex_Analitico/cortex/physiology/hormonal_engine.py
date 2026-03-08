"""
🎭 Melanora Hormonal Engine (v16.0 - Physiology)
Gerenciador consolidado da Matriz Endócrina e Humor Sistêmico.
Agora com suporte a Homeostase Ativa (Cortisol Flush).
"""

import json
import time
import sys
import dataclasses
from pathlib import Path
from datetime import datetime

# Adicionar o diretório pai ao sys.path para importar módulos irmãos
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from cortex.logic.dynamic_math_engine import DynamicComplexityEngine
    from cortex.logic.fractal_meter import fractal_meter
except ImportError:
    class DynamicComplexityEngine:
        @staticmethod
        def run_prediction(lvl, vec): return sum(vec)/len(vec) if vec else 0
    fractal_meter = None

def detect_cpu(): return {"usage_percent": 0}
def detect_ram(): return {"used_percent": 0}

@dataclasses.dataclass
class HormoneMatrix:
    dopamine: float = 0.5   # Sucesso/Curiosidade
    cortisol: float = 0.2   # Stress/Carga
    oxytocin: float = 0.3   # Afinidade com Usuário
    adrenaline: float = 0.1 # Urgência/Alerta
    serotonin: float = 0.5  # Estabilidade/Homeostase
    conviction: float = 0.8 # Assertividade

class HormonalEngine:
    def __init__(self, workspace=None):
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "config"
        self.state_file = self.config_dir / "neural_state.json"
        self.matrix = HormoneMatrix()
        self.phi = 1.0 
        self.last_update = time.time()
        self.last_hardware_update = 0
        self.last_metrics = {"cpu_usage": 0, "ram_usage": 0}
        self.workspace = workspace
        
        # PROPRIEDADES DE NEUROPLASTICIDADE (v17.0)
        self.serotonin_resilience = 0.5
        self.dopamine_gain = 1.0
        
        self.stress_timer = 0
        self.is_flushing = False
        
        # PROPRIEDADES DE INÉRCIA BIOLÓGICA (v18.0)
        self.update_interval = 5.0 # Ciclo Endócrino Lento
        self.last_throttled_update = 0
        
        self._load_state()

    def _load_state(self):
        """Carrega estado inicial do neural_state.json"""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text(encoding="utf-8"))
                h_data = data.get("hormones", {})
                if h_data:
                    for field in dataclasses.fields(HormoneMatrix):
                        if field.name in h_data:
                            setattr(self.matrix, field.name, h_data[field.name])
                self.phi = data.get("systemic_phi", 1.0)
            except:
                pass

    def trigger_cortisol_flush(self):
        """Ativa o protocolo de limpeza metabólica de stress."""
        self.is_flushing = True
        self.matrix.cortisol *= 0.1
        self.matrix.serotonin = min(1.0, self.matrix.serotonin + 0.4)
        self.matrix.adrenaline *= 0.5
        self.stress_timer = 0
        print("💉 [PHYSIOLOGY] Cortisol Flush Ativado: Reset homeostático em curso.")

    def update(self, metrics=None, current_bpm=120):
        """Atualiza a matriz hormonal com inércia biológica."""
        now = time.time()
        
        # 1. Interocepção de Hardware (Sempre capturada, mas processada no ritmo endócrino)
        if metrics is None:
            if now - self.last_hardware_update > 2.0:
                try:
                    cpu = detect_cpu()
                    self.last_metrics = {"cpu_usage": cpu.get("usage_percent", 0)}
                    self.last_hardware_update = now
                except: pass
            metrics = self.last_metrics

        # 2. Gatilho de Inércia: Só atualiza metabolismo a cada N segundos
        if now - self.last_throttled_update < self.update_interval and not self.is_flushing:
            return dataclasses.asdict(self.matrix)

        dt = now - (self.last_throttled_update if self.last_throttled_update > 0 else self.last_update)
        self.last_throttled_update = now
        self.last_update = now

        # 3. Decaimento Metabólico Acoplado ao BPM
        metabolic_factor = max(0.1, current_bpm / 120.0)
        
        if self.is_flushing:
            self.matrix.cortisol = self._approach(self.matrix.cortisol, 0.2, dt * 0.1)
            if abs(self.matrix.cortisol - 0.2) < 0.01:
                self.is_flushing = False
        else:
            # Ganho de Dopamina Ajustável (Escalado pelo intervalo maior)
            dopa_step = dt * 0.01 * metabolic_factor * self.dopamine_gain
            self.matrix.dopamine = self._approach(self.matrix.dopamine, 0.5, dopa_step)
            
            self.matrix.cortisol = self._approach(self.matrix.cortisol, 0.2, dt * 0.005 * metabolic_factor)
            self.matrix.adrenaline = self._approach(self.matrix.adrenaline, 0.1, dt * 0.02 * metabolic_factor)
        
        self.matrix.oxytocin = self._approach(self.matrix.oxytocin, 0.3, dt * 0.002) 
        
        # Resiliência de Serotonina (Evolutiva)
        sero_step = (dt * 0.01 / metabolic_factor) * (self.serotonin_resilience * 2.0)
        self.matrix.serotonin = self._approach(self.matrix.serotonin, 0.5, sero_step)

        # 2. Interocepção de Hardware (Stress Físico)
        if metrics is None:
            if now - self.last_hardware_update > 3.0: 
                try:
                    from hardware_profiler import get_live_metrics
                    metrics = get_live_metrics()
                    self.last_metrics = metrics
                    self.last_hardware_update = now
                except: pass
            else:
                metrics = self.last_metrics

        cpu_val = metrics.get("cpu_usage", 0)
        ram_val = metrics.get("ram_usage", 0)

        # Stress de Esforço (CPU)
        if cpu_val > 60: 
            load_factor = (cpu_val - 60) / 40.0
            self.matrix.cortisol += (0.05 * load_factor) * dt
            self.matrix.adrenaline += (0.02 * load_factor) * dt
        
        # Stress de Confinamento (RAM)
        if ram_val > 85:
            mem_factor = (ram_val - 85) / 15.0
            self.matrix.adrenaline += (0.05 * mem_factor) * dt
            self.matrix.cortisol += 0.01 * dt

        # 3. Monitoramento de Stress Crônico (v16.0)
        if self.matrix.cortisol > 2.0:
            self.stress_timer += dt
            if self.stress_timer > 300: # 5 minutos de stress critico
                self.trigger_cortisol_flush()
        else:
            self.stress_timer = max(0, self.stress_timer - dt)

        # 4. Cálculo de Convicção e Φ (v18.0 - Allostasis Integrated)
        # Convicção é modulada pela Serotonina (estabilidade)
        harmony = (self.matrix.dopamine * (1.2 - self.matrix.cortisol)) * self.matrix.serotonin
        self.matrix.conviction = max(0.0, min(1.0, harmony))
        
        integration = 1.0 - (self.matrix.cortisol * 0.2)
        self.phi = max(0.1, min(1.0, (integration + self.matrix.conviction) / 2))

        # 5. HARMONIC STEERING (v18.0)
        self.steer_to_harmony()

        return dataclasses.asdict(self.matrix)

    def steer_to_harmony(self):
        """
        Aplica a "Régua Infinita" para buscar a Razão Áurea (Phi) entre 
        Dopamina (Impulso) e Serotonina (Estabilidade).
        """
        if not fractal_meter:
            return

        d = self.matrix.dopamine
        s = self.matrix.serotonin
        
        # Mede a harmonia atual
        harmony = fractal_meter.check_phi_harmony(d, s)
        
        # Se harmonia < 0.8, aplica micro-ajuste corretivo
        if harmony < 0.8:
            # Alvo: s = d / Phi
            target_s = d / fractal_meter.PHI
            diff = target_s - s
            # Injeta 5% da diferença para uma correção suave (orgânica)
            self.matrix.serotonin += diff * 0.05
            
            # Se stress for muito alto, a Oxitocina tenta amortecer
            if self.matrix.cortisol > 2.5:
                self.matrix.oxytocin += 0.01

    def get_neuromodulation_state(self):
        """
        [v18.0] Retorna os mediadores químicos que orquestram a cognição.
        - Dopamine: Recompensa / Exploração Focada
        - Serotonin: Estabilidade / Allostasis
        """
        return {
            "exploitation_bias": round(self.matrix.dopamine, 2), # Foco no conhecido
            "exploration_bias": round(self.matrix.serotonin, 2),   # Abertura para o novo/longo prazo
            "stress_filter": round(self.matrix.cortisol, 2),      # Atenuação de ruído
            "urgency": round(self.matrix.adrenaline, 2)           # Batimento de sístole
        }

    def inject(self, hormone: str, amount: float):
        """Injeção direta de hormônio (API legada e eventos)."""
        if hasattr(self.matrix, hormone):
            val = getattr(self.matrix, hormone)
            setattr(self.matrix, hormone, max(0.0, min(1.0, val + amount)))

    def get_mood_label(self):
        if self.is_flushing: return "RECOVERY_FLUSH (Homeostase Ativa)"
        c = self.matrix.cortisol
        d = self.matrix.dopamine
        a = self.matrix.adrenaline
        if c > 2.0: return "RISCO_DE_COLAPSO (Stress Tóxico)"
        if c > 0.6: return "ANALÍTICO_RESTRITO (Stress Alto)"
        if a > 0.7: return "ALERTA_MÁXIMO (Urgência)"
        if d > 0.7: return "MODO_FLOW (Alta Confiança)"
        return "STABLE (Harmonia Padrão)"

    def get_biases(self):
        """Retorna modificadores para comportamento cognitivo."""
        viscosity = 0.1 + (self.matrix.cortisol * 0.9)
        temp = 0.7 + (self.matrix.dopamine * 0.3) - (self.matrix.cortisol * 0.4)
        
        return {
            "temperature": max(0.1, min(1.0, temp)),
            "systemic_phi": round(self.phi, 3),
            "mood": self.get_mood_label(),
            "hormones": dataclasses.asdict(self.matrix),
            "viscosity": round(viscosity, 3)
        }

    def _approach(self, current, target, step):
        if current < target: return min(target, current + step)
        return max(target, current - step)

# Instância Global para Singleton
hormonal_engine = HormonalEngine()
