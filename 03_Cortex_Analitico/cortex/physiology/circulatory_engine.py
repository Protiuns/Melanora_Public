"""
💓 Melanora Circulatory Engine (v16.0 - Physiology)
Controlador autônomo de batimento e cadência de processamento.
"""

import time
from pathlib import Path

class CirculatoryEngine:
    def __init__(self, hormonal_engine=None):
        self.hormonal_engine = hormonal_engine
        self.base_bpm = 60
        self.last_bpm = 120
        self.last_pulse_time = time.time()
        self.neural_pressure = 0.0
        self.cardiac_output = 0.0 # Débito Cardíaco (Eficiência de Fluxo)
        
        # SISTEMA DE DISTRIBUIÇÃO PULSÁTIL (v18.0)
        self.systolic_buffer = 0.0
        self.energy_demand = {} # Componente -> Demanda

    def register_demand(self, component_name, intensity=0.1):
        """Registra a demanda de energia de um componente modular."""
        self.energy_demand[component_name] = intensity

    def get_current_pulse(self):
        """Calcula o BPM ideal baseado no clima hormonal e hardware."""
        if not self.hormonal_engine:
            return 120.0

        biases = self.hormonal_engine.get_biases()
        hormones = biases.get("hormones", {})
        dopamine = hormones.get("dopamine", 0.5)
        cortisol = hormones.get("cortisol", 0.2)
        
        # 1. Componente Biológico
        bpm = self.base_bpm + (dopamine * 480) - (cortisol * 180) # Maior amplitude v14.4
        
        # 2. Componente de Hardware (Bradicardia Protetiva)
        metrics = self.hormonal_engine.last_metrics
        cpu_val = metrics.get("cpu_usage", 0)
        
        # Atualização da Pressão Neural
        self.neural_pressure = cpu_val + (cortisol * 30)
        
        hardware_factor = 1.0
        if cpu_val > 70:
            hardware_factor = 0.5 * (100 - cpu_val) / 30 
            
        bpm = bpm * max(0.1, hardware_factor)
        
        # 3. Limites
        self.last_bpm = max(30, min(180, bpm))
        
        # 4. Cálculo de Débito Cardíaco (Energia Disponível por Pulso)
        pressure_factor = max(0.05, 1.0 - (self.neural_pressure / 100))
        self.cardiac_output = (self.last_bpm / 60.0) * pressure_factor # Ajustado para escala s
        
        return round(self.last_bpm, 1)

    def get_energy_allocation(self):
        """Retorna o nível de energia sináptica disponível (0.0 a 1.0)."""
        self.get_current_pulse()
        return round(max(0.1, min(1.0, self.cardiac_output)), 2)

    def consume_energy(self, amount):
        """Tenta consumir energia do buffer sistólico."""
        if self.systolic_buffer >= amount:
            self.systolic_buffer -= amount
            return True
        return False

    def should_suspend_tasks(self):
        """Retorna True se a pressão for crítica."""
        self.get_current_pulse()
        return self.neural_pressure > 95.0

    def should_trigger_pulse(self):
        """
        [v18.0] Gatilho sístólico: Refila o buffer de energia a cada batimento.
        Agora inclui ANTECIPAÇÃO ALLOSTÁTICA: O coração acelera se a pressão cresce.
        """
        bpm = self.get_current_pulse()
        
        # Allostasis: Se houver muitas demandas registradas, encurtamos o intervalo preventivamente
        active_demand = sum(self.energy_demand.values())
        allostatic_boost = 1.0 + (active_demand * 0.5) # Acelera até 50% extra o ciclo
        
        interval = (60.0 / bpm) / allostatic_boost
        now = time.time()
        
        if now - self.last_pulse_time >= interval:
            self.last_pulse_time = now
            # Sístole: O coração bombeia energia para o buffer
            # O volume injetado no buffer é o Débito Cardíaco (cardiac_output)
            self.systolic_buffer = self.get_energy_allocation()
            
            # Limpa demandas processadas neste pulso
            self.energy_demand = {k: v * 0.5 for k, v in self.energy_demand.items() if v > 0.01}
            return True
        return False

    def get_sleep_interval(self):
        return 0.01 

circulatory_engine = CirculatoryEngine()
