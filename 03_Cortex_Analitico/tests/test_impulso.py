import logging
import sys
import os

# Garantir que o diretório root do script seja alcançado
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex.logic.neural_impulse import NeuralImpulse, ImpulseScheduler
from cortex.logic.axiom_associator import AxiomAssociator

logging.basicConfig(level=logging.INFO, format="%(message)s")

def simulate_bullet_time_synapse():
    print("="*60)
    print("SIMULADOR DE CORTEX SEGMENTADO (Priority Queue Biomimetica)")
    print("="*60)
    
    scheduler = ImpulseScheduler()
    associator = AxiomAssociator(scheduler)
    
    # 1. Injetando Tarefas Lentas (Peso baixo = Rotina)
    print("\n[>>] Injetando 3 Impulsos de Manutencao Lenta (Peso: 10 a 20)...")
    scheduler.inject_raw(weight=10.0, source="system", target="clear_logs", payload={}, tags=["interno"])
    scheduler.inject_raw(weight=15.0, source="memory", target="defrag", payload={}, tags=["interno"])
    scheduler.inject_raw(weight=20.0, source="ui", target="update_frame", payload={}, tags=["visual"])
    
    # 2. Injetando Emergencia (Peso Alto = Sobrevivencia/Dilema)
    print("[!!] INJETANDO IMPULSO CRITICO: DETECCAO DE MOVIMENTO RAPIDO (Peso: 95.0)")
    # Esse pulso possui tags atreladas a conhecimentos (axiomas) guardados.
    emerg_id = scheduler.inject_raw(
        weight=95.0, 
        source="sensory_engine", 
        target="evaluate_action_validity", 
        payload={"pixels_moved": 400, "entities": [{"type": "green_mass", "bbox": [5, 200, 20, 20]}]}, 
        tags=["visual", "proximidade", "bloqueio"]
    )
    
    # 3. Processamento Continuo (Mimetizando Neural Bridge em estado passivo)
    print("\n[==] INICIANDO ROTEADOR NERVO CENTRAL (Retirada via HeapQueue)...\n")
    pass_number = 1
    
    while scheduler.has_pending_impulses():
        # Roteador sempre pega o mais pesado na matematica do MinHeap
        impulse = scheduler.get_highest_priority()
        
        print(f"TICK {pass_number}: Processando '{impulse.target_function}' (Peso original: {impulse.original_weight:.1f})")
        
        # 4. Magia Biomimetica: Se uma memoria tiver afinidade, ela é pré-despertada e jogada na fila instantaneamente!
        associator.propagate_associations(impulse)
        
        pass_number += 1

if __name__ == "__main__":
    simulate_bullet_time_synapse()
