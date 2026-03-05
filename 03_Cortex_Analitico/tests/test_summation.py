import logging
import sys
import os

# Garantir que o diretorio root do script seja alcancado
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cortex.logic.neural_impulse import NeuralImpulse, ImpulseScheduler
from cortex.logic.axiom_associator import AxiomAssociator

logging.basicConfig(level=logging.INFO, format="%(message)s")

def test_neural_summation():
    print("="*60)
    print("TESTE DE SOMACAO NEURAL (ACCUMULATED ENERGY MATRIX)")
    print("="*60)
    
    scheduler = ImpulseScheduler()
    associator = AxiomAssociator(scheduler)
    LOW_WEIGHT = 8.0
    
    print(f"\n[>>] Iniciando sequencia de disparos (15 pulsos de peso {LOW_WEIGHT})...")
    for i in range(15):
        scheduler.inject_raw(
            weight=LOW_WEIGHT, 
            source="sensor", 
            target="dummy", 
            payload={}, 
            tags=["visual", "proximidade", "bloqueio"]
        )
        
        while scheduler.has_pending_impulses():
            impulse = scheduler.get_highest_priority()
            associator.propagate_associations(impulse)
            
    print(f"\nCarga final de ax_spatial_collision: {associator.energy_matrix.get('ax_spatial_collision', 0):.1f}")
    
    # 15 pulsos de 7.2 = 108.0. 
    # Apos disparo de 100.0, deve sobrar 8.0.
    if 7.0 <= associator.energy_matrix.get('ax_spatial_collision', 0) <= 9.0:
         print("\n[SUCCESS] O neurônio disparou e a carga residual está correta (~8.0)!")
    else:
         print(f"\n[FAILURE] O neurônio não disparou ou a carga está incorreta: {associator.energy_matrix.get('ax_spatial_collision', 0)}")

if __name__ == "__main__":
    test_neural_summation()
