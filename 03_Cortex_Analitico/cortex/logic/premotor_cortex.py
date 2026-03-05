import logging
from typing import Dict, Any, List
from cortex.logic.neural_irrigation import global_gland

logger = logging.getLogger("PremotorCortex")

class PremotorCortex:
    """
    O Oráculo Biológico. 
    Simula o futuro dos fluídos químicos em até 80 ciclos temporais ANTES de
    permitir que o Córtex Central aplique um neurotransmissor massivo.
    Dita a Segurança e a Gestão de Fadiga Mental.
    """
    def __init__(self):
        self.lookahead_ticks = 80
        self.decay_rate = 0.02
        self.critical_energy_threshold = 400.0 # Acima disso a mente "surta" por estafa térmica
        
    def forecast_dilemma(self, proposed_hormone: str, proposed_amount: float) -> Dict[str, Any]:
        """
        Recebe uma proposta de injeção química (ex: 1.0 de Adrenalina por ter visto algo agudo).
        Simula o futuro temporal e retorna um Relatório de Previsão de Colapso (ForecastReport).
        """
        # Snapshot do agora
        current = global_gland.extract_climate()
        sim_adren = current.get("adrenaline", 0.0)
        sim_dopa = current.get("dopamine", 0.0)
        sim_sero = current.get("serotonin", 0.5)
        
        # Injeta hipoteticamente
        if proposed_hormone == "adrenaline":
            sim_adren = min(1.0, sim_adren + proposed_amount)
        elif proposed_hormone == "dopamine":
            sim_dopa = min(1.0, sim_dopa + proposed_amount)
        elif proposed_hormone == "serotonin":
            sim_sero = min(1.0, sim_sero + proposed_amount)
            
        warnings = []
        peak_energy = 0.0
        serotonin_starvation_ticks = 0
        
        # Roda a simulação no tempo
        for t in range(self.lookahead_ticks):
            
            # Checa o calor
            heat = (sim_adren * 1.5) + (sim_dopa * 1.2) + abs(0.5 - sim_sero)
            energy_burn = heat * 100
            if energy_burn > peak_energy:
                peak_energy = energy_burn
                
            if energy_burn > self.critical_energy_threshold:
                warnings.append(f"CRITICAL_TICK_{t}: Colapso Térmico Iminente ({energy_burn:.1f}E)")
                break # Para a simulação, já é lixo fatal
                
            # Verifica estafa de serotonina
            if sim_sero < 0.1:
                serotonin_starvation_ticks += 1
                if serotonin_starvation_ticks > 25:
                    warnings.append(f"WARNING_TICK_{t}: Manutenção Aniquilada. Fadiga Estrutural Grave.")
            else:
                serotonin_starvation_ticks = 0
                
            # Decaimento preditivo
            sim_adren = max(0.0, sim_adren - self.decay_rate)
            sim_dopa = max(0.0, sim_dopa - self.decay_rate)
            if sim_sero > 0.5:
                sim_sero = max(0.5, sim_sero - self.decay_rate)
            elif sim_sero < 0.5:
                sim_sero = min(0.5, sim_sero + self.decay_rate)
                
        forecast_report = {
            "approved": True,
            "peak_energy_predicted": peak_energy,
            "warnings": warnings,
            "compensatory_action_required": False,
            "delay_ticks_for_gaba": 0
        }
        
        # AVALIAÇÃO DE VETO OU FRAGMENTAÇÃO
        if warnings:
            logger.warning(f"👁️‍🗨️ [PREMOTOR] Projeção acusou falha orgânica fatal se injetar {proposed_amount} de {proposed_hormone}.")
            
            # Estratégia B: Fragmentação Ritmica
            # Se for faltar Serotonina (Fadiga Estrutural), nós APROVAMOS o pânico agora, 
            # mas FORÇAMOS uma injeção de Gaba/Serotonina em no máximo 15 ciclos.
            if any("Fadiga Estrutural" in w for w in warnings):
                forecast_report["compensatory_action_required"] = True
                forecast_report["delay_ticks_for_gaba"] = 15
                logger.warning("👁️‍🗨️ [PREMOTOR] Aplicando Estratégia de Fragmentação: Pânico Autorizado, Mas Respiro Compulsório agendado em T-15.")
                
            if any("Colapso Térmico" in w for w in warnings):
                 # Veto absoluto. A máquina não aguenta. Reduz a injeção artificialmente.
                 forecast_report["approved"] = False
                 logger.error("👁️‍🗨️ [PREMOTOR] VETO ABSOLUTO EXERCIDO. Injeção letal abortada.")
                 
        return forecast_report

global_premotor = PremotorCortex()
