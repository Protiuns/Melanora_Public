"""
🧪 Teste de Eficácia Analítica (Fase 27)
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus

def test_phase_27_tracker():
    print("--- INICIANDO TESTE DA FASE 27 ---")
    
    orchestrator = CognitiveOrchestrator()
    tool_id = "nt_numerical_counter"
    
    # --- 1. Teste de Aumento de Eficácia ---
    print("\n[Teste 1] Evolução Positiva de Eficácia")
    
    # Mock do root para garantir sucesso
    orchestrator.root.tick = MagicMock(return_value=NodeStatus.SUCCESS)
    # Força o uso da ferramenta no contexto (simulando DynamicTuner)
    orchestrator.context["tools_run_in_tick"] = [tool_id]
    
    initial_score = orchestrator.blackboard.tool_efficacy.get(tool_id, 0.5)
    print(f"Score inicial: {initial_score}")
    
    orchestrator.tick({"user_prompt": "Teste Sucesso"})
    
    new_score = orchestrator.blackboard.tool_efficacy.get(tool_id)
    print(f"Score após sucesso: {new_score}")
    assert new_score > initial_score
    print("✅ SUCESSO: Eficácia aumentou após sucesso da tarefa.")

    # --- 2. Teste de Degradação e Gating ---
    print("\n[Teste 2] Degradação e Remoção Dinâmica (Gating)")
    
    # Mock para garantir falha
    orchestrator.root.tick = MagicMock(return_value=NodeStatus.FAILURE)
    
    print("Forçando falhas para derrubar o score...")
    for i in range(5):
        orchestrator.context["tools_run_in_tick"] = [tool_id]
        orchestrator.tick({"user_prompt": f"Falha {i}"})
    
    final_score = orchestrator.blackboard.tool_efficacy.get(tool_id)
    print(f"Score final após falhas: {final_score}")
    
    # Agora testamos se o DynamicTuner realmente pula a ferramenta
    # Precisamos usar o root real ou um que contenha o DynamicTuner
    orchestrator = CognitiveOrchestrator() # Novo para resetar mocks mas mantemos o score baixo via BB se quisermos, 
    # ou apenas forçamos o score no BB deste novo.
    orchestrator.blackboard.tool_efficacy[tool_id] = 0.1
    
    # Mock do run_neural_tool_scan para ver se é chamado
    with patch("cortex.specialists.neural_tool_manager.run_neural_tool_scan") as mock_scan:
        orchestrator.tick({"user_prompt": "Teste Gating"})
        
        # O Numerical Counter não deve ter sido chamado
        calls = [c[0][0] for c in mock_scan.call_args_list]
        print(f"Ferramentas chamadas: {calls}")
        assert tool_id not in calls
    
    print("✅ SUCESSO: Ferramenta ineficaz foi ignorada pelo DynamicTuner!")

from unittest.mock import patch

if __name__ == "__main__":
    try:
        test_phase_27_tracker()
    except AssertionError as e:
        print(f"\n❌ FALHA NO TESTE: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ ERRO: {e}")
