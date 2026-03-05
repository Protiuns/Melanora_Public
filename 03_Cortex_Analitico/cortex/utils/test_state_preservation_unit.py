"""
🧪 Teste Unitário de Preservação de Estado (Fase 23)
Foca apenas nos nós AreaGate + CerebralAreaBurst + Action.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import (
    NodeStatus, Action, CerebralAreaBurst, AreaGate, Blackboard
)

def test_unit_resume():
    print("--- INICIANDO TESTE UNITÁRIO DE PRESERVAÇÃO ---")
    
    bb = Blackboard()
    context = {"blackboard": bb, "results": {}}
    
    # 1. Configuração dos Nós
    call_log = []
    def mock_action_func(ctx):
        call_log.append(1)
        if len(call_log) == 3:
            return NodeStatus.RUNNING # Interrompe no 3º pulso
        return {"status": "SUCCESS"}
    
    action = Action("TestAction", mock_action_func)
    burst = CerebralAreaBurst("TestBurst", action, "pulses")
    gate = AreaGate("TestArea", burst)
    
    bb.set("pulses", 5)
    bb.set("area_TestArea_active", True)

    # CENÁRIO 1: Interrupção (Tick 1)
    print("\n[Cenário 1] Tick 1: Deve parar no 3º pulso (RUNNING)")
    status = gate.tick(context)
    
    print(f"Status Final: {status}")
    print(f"Chamadas totais: {len(call_log)}")
    
    assert status == NodeStatus.RUNNING
    assert len(call_log) == 3
    assert bb.get("resume_TestBurst") == 2 # Índice do 3º pulso

    # CENÁRIO 2: Gating (Tick 2)
    print("\n[Cenário 2] Tick 2: Gating Ativo. Deve bloquear.")
    bb.set("area_TestArea_active", False)
    status = gate.tick(context)
    
    print(f"Status Final: {status}")
    print(f"Chamadas totais: {len(call_log)}") # Não deve aumentar
    assert status == NodeStatus.FAILURE
    assert len(call_log) == 3

    # CENÁRIO 3: Retomada (Tick 3)
    print("\n[Cenário 3] Tick 3: Gating OFF. Deve retomar e completar.")
    bb.set("area_TestArea_active", True)
    status = gate.tick(context)
    
    print(f"Status Final: {status}")
    print(f"Chamadas totais: {len(call_log)}")
    
    # Pulso 3 parou. Ao retomar, ele RE-EXECUTA o pulso 3 (que agora retorna SUCCESS).
    # Então ele faz: Pulso 3 (re-run), Pulso 4, Pulso 5.
    # Total calls: 3 (tick 1) + 3 (tick 3) = 6.
    
    assert status == NodeStatus.SUCCESS
    assert len(call_log) == 6 # 3 originais + 3 da retomada
    assert bb.get("resume_TestBurst") == 0 # Resetado
    print("\n✅ SUCESSO UNITÁRIO: Gating e Resume (com re-entrega) funcionando!")

if __name__ == "__main__":
    try:
        test_unit_resume()
    except AssertionError as e:
        print(f"\n❌ FALHA NO TESTE: {e}")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
