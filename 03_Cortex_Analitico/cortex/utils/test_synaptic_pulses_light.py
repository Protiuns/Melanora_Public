"""
🧪 Teste Leve de Pulsos Sinápticos (Fase 20)
Verifica se as áreas cerebrais respeitam o bueget de pulsos sem chamadas externas.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, Action, Sequence, CerebralAreaBurst, NodeStatus

def test_pulse_logic():
    print("--- INICIANDO TESTE DE PULSOS SINÁPTICOS (LIGHT) ---")
    orchestrator = CognitiveOrchestrator()
    
    # Mock de contagem de execuções
    execution_stats = {"prefrontal": 0}

    def mock_prefrontal_action(ctx):
        execution_stats["prefrontal"] += 1
        return True

    # Rebuild de uma árvore de teste minimalista
    test_tree = Sequence("Test_Pulse_Tree")
    prefrontal_mock = Action("Mock_Prefrontal", mock_prefrontal_action)
    test_tree.add_child(CerebralAreaBurst("Burst_Area", prefrontal_mock, "test_pulses"))

    # Cena 1: 5 Pulsos
    print("\n[CENA 1] Configurando 5 Pulsos")
    orchestrator.blackboard.set("test_pulses", 5)
    execution_stats["prefrontal"] = 0
    test_tree.tick(orchestrator.context)
    
    print(f"Execuções detectadas: {execution_stats['prefrontal']}")
    if execution_stats["prefrontal"] == 5:
        print("✅ SUCESSO: Budget de 5 pulsos respeitado.")
    else:
        print(f"❌ FALHA: Esperado 5, obtido {execution_stats['prefrontal']}")

    # Cena 2: 2 Pulsos
    print("\n[CENA 2] Configurando 2 Pulsos")
    orchestrator.blackboard.set("test_pulses", 2)
    execution_stats["prefrontal"] = 0
    test_tree.tick(orchestrator.context)
    
    print(f"Execuções detectadas: {execution_stats['prefrontal']}")
    if execution_stats["prefrontal"] == 2:
        print("✅ SUCESSO: Budget de 2 pulsos respeitado.")
    else:
        print(f"❌ FALHA: Esperado 2, obtido {execution_stats['prefrontal']}")

if __name__ == "__main__":
    test_pulse_logic()
