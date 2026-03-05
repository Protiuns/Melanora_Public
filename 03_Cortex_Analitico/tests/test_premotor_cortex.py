import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex.logic.neural_impulse import NeuralImpulse, ImpulseScheduler
from cortex.logic.axiom_associator import AxiomAssociator
from cortex.logic.neural_irrigation import global_gland

logging.basicConfig(level=logging.INFO, format="%(message)s")

def simulate_premotor_intervention():
    print("="*60)
    print("🔭 PREMOTOR CORTEX - SIMULADOR DE COLAPSO VIRTUAL (VETO PREDITIVO)")
    print("="*60)
    
    # Resetando a Glandula para garantir estresse artificial acumulativo
    global_gland.fluids = {"adrenaline": 0.8, "dopamine": 0.0, "serotonin": 0.1}
    
    scheduler = ImpulseScheduler()
    associator = AxiomAssociator(scheduler)
    
    # 1. Injetando Tarefas Lentas (Lump sum de processos parados)
    scheduler.inject_raw(weight=10.0, source="sys", target="clean_mem", payload={}, tags=["interno", "log"])
    
    # 2. Causando um engasgo na mente. Tentaremos empurrar 10 ataques visuais seguidos.
    # Nossa glande virtual já está estressada. O Axiom Associator varrerá os limites futuros.
    print("[!!] INJETANDO LOOPING DE PÂNICO: 3 Impulsos Seguidos de Alto Contraste (Ameaça)\n")
    
    for _ in range(3):
        imp = NeuralImpulse.create(
            weight=95.0, 
            source="sensory", 
            target="analyze_threat", 
            payload={}, 
            tags=["visual", "movimento_rapido", "alto_contraste", "proximidade", "bloqueio"]
        )
        
        # A interceptação Premotor ocorrerá AQUI DENTRO (na tentativa de associar o pânico químico)
        associator.propagate_associations(imp)

    print("\n[==] LENDO A FILA DE PRIORIDADES RESULTANTE (POS-VETO)...\n")
    
    pass_number = 1
    warnings_mitigados = 0
    
    while scheduler.has_pending_impulses():
        pulso = scheduler.get_highest_priority()
        # Se for um pulso artificial agendado pela Estratégia B
        marker = "🔥"
        if pulso.target_function == "force_homeostasis":
            marker = "🛡️ ESTRATÉGIA B (RESPIRO AGENDADO) ->"
            warnings_mitigados += 1
            
        print(f"{marker} Pulso Enxertado: '{pulso.target_function}' (Priority Weight: {pulso.original_weight:.1f})")
        pass_number += 1
        
    print(f"\n✅ O Sistema Previu a Falha Orgânica e embutiu {warnings_mitigados} resfriadores Gaba/Serotonina de ultra-prioridade na Fila.")

if __name__ == "__main__":
    simulate_premotor_intervention()
