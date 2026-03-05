"""
🧪 Teste de Darwinismo Neural (Fase 28)
Verifica a evolução e poda de Áreas Cerebrais baseada em eficácia.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus

def test_phase_28_darwinism():
    print("--- INICIANDO TESTE DA FASE 28: DARWINISMO NEURAL ---")
    
    orchestrator = CognitiveOrchestrator()
    area_name = "Prefrontal_Cortex"
    pulse_key = "prefrontal_pulses"
    
    # --- 1. Teste de Penalização ---
    print("\n[Teste 1] Falhas seguidas e queda de Score")
    
    # Forçamos falha no root
    orchestrator.root.tick = MagicMock(return_value=NodeStatus.FAILURE)
    # Simulamos que a área Pré-frontal estava ativa no tick
    orchestrator.context["areas_run_in_tick"] = [area_name]
    
    initial_score = orchestrator.blackboard.area_efficacy.get(area_name, 0.8)
    print(f"Score inicial da área {area_name}: {initial_score}")
    
    # Aplicamos 3 falhas
    for _ in range(3):
        orchestrator.context["areas_run_in_tick"] = [area_name]
        orchestrator.tick({"user_prompt": "Teste Falha"})
    
    low_score = orchestrator.blackboard.area_efficacy.get(area_name)
    print(f"Score após 3 falhas: {low_score}")
    assert low_score < initial_score
    print(f"✅ SUCESSO: Área {area_name} penalizada corretamente.")

    # --- 2. Teste de Poda Darwiniana (Rebalancing) ---
    print("\n[Teste 2] Poda de Pulsos via DynamicTuner")
    
    # Atualizamos o budget inicial para um valor alto para ver a queda
    orchestrator.blackboard.set(pulse_key, 4)
    orchestrator.blackboard.area_efficacy[area_name] = 0.4 # Score baixo
    
    print(f"Propulsão inicial: 4 pulsos. Score: 0.4")
    
    # No próximo tick, o DynamicTuner deve agir antes de qualquer área
    # O DynamicTuner roda como primeiro filho do root
    # Aqui vamos usar o tick real para ver o efeito no blackboard
    orchestrator.tick({"user_prompt": "Teste Rebalanceamento"})
    
    new_pulses = orchestrator.blackboard.get(pulse_key)
    print(f"Pulsos após Darwinismo: {new_pulses} (Esperado: <= 2)")
    
    # Como pulses * score -> 4 * 0.4 = 1.6 -> int(1.6) = 1
    assert new_pulses < 4
    print(f"✅ SUCESSO: Budget de pulsos podado de 4 para {new_pulses} devido a baixa eficácia!")

if __name__ == "__main__":
    try:
        test_phase_28_darwinism()
    except AssertionError as e:
        print(f"\n❌ FALHA NO TESTE: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ ERRO: {e}")
