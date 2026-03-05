"""
🧪 Teste de Preservação de Estado Sináptico (Fase 23)
Verifica se uma área secundária (Motor) interrompida mantém seu progresso e respeita o Gating.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

# Mock do logger
from cortex.system_2 import behavior_tree_manager as btm
btm.log_event = MagicMock()

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus

def test_synaptic_resume_gated():
    print("--- INICIANDO TESTE DE PRESERVAÇÃO DE ESTADO (ÁREA GATED) ---")
    
    orchestrator = CognitiveOrchestrator()
    orchestrator.blackboard.set("motor_pulses", 5)
    orchestrator.blackboard.set("situational_id", "RESEARCH") # Pesquisa usa Motor_Cortex

    # Mock da ação no Motor Cortex (bt_consolidate)
    call_log = []
    def side_effect(context):
        call_log.append(1)
        if len(call_log) == 3:
            return NodeStatus.RUNNING
        return {"status": "SUCCESS"}
    
    # Em RESEARCH mode, o motor_cortex roda bt_consolidate
    orchestrator.bt_consolidate = MagicMock(side_effect=side_effect)
    orchestrator.bt_research = MagicMock(return_value={"status": "SUCCESS"})
    orchestrator.bt_finalize = MagicMock(return_value={"status": "SUCCESS"})

    # Recria a árvore para carregar os mocks
    orchestrator.root = orchestrator._build_tree()

    # CENÁRIO 1: Interrupção no pulso 3
    print("\n[Cenário 1] Executando 3 pulsos e forçando interrupção no Motor Cortex...")
    orchestrator.tick({"system_load": 10}) # Carga baixa, Motor ATIVO
    
    resume_val = orchestrator.blackboard.get("resume_Execution_Burst")
    print(f"DEBUG: Chamadas efetuadas: {len(call_log)}")
    print(f"DEBUG: Valor de resume (Execution_Burst): {resume_val}")
    
    assert len(call_log) == 3, f"Deveria ter chamado 3 vezes, chamou {len(call_log)}"
    assert resume_val == 2

    # CENÁRIO 2: Gating Ativo (Carga 90%)
    print("\n[Cenário 2] Carga 90% (Gating Motor ON). Área deve estar OFFLINE.")
    orchestrator.tick({"system_load": 90}) # Gating Motor ativo
    
    print(f"DEBUG: Chamadas totais após gating: {len(call_log)}")
    assert len(call_log) == 3, "ERRO: Área Motor rodou mesmo com Gating ativo!"

    # CENÁRIO 3: Retomada (Carga 10%)
    print("\n[Cenário 3] Carga 10% (Gating Motor OFF). Deve completar os 2 pulsos restantes.")
    orchestrator.bt_consolidate.side_effect = None
    orchestrator.bt_consolidate.return_value = {"status": "SUCCESS"}
    
    orchestrator.tick({"system_load": 10})
    
    # Total esperado: 3 (do primeiro tick) + 2 (do tick de retormada) = 5
    # Nota: mock_action.call_count contaria os side_effects + novas chamadas
    total_calls = len(call_log) + (orchestrator.bt_consolidate.call_count - 3)
    
    print(f"DEBUG: Chamadas totais final: {total_calls}")
    
    if total_calls == 5:
        print("\n✅ SUCESSO: O Motor Cortex retomou perfeitamente após o Gating!")
    else:
        print(f"\n❌ FALHA: Esperado 5 pulsos, executados {total_calls}")

if __name__ == "__main__":
    try:
        test_synaptic_resume_gated()
    except AssertionError as e:
        print(f"\n❌ FALHA NO TESTE (Assertion): {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ ERRO INESPERADO: {e}")
