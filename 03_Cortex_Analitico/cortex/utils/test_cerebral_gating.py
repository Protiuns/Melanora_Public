"""
🧪 Teste de Gating Cerebral (Fase 22)
Verifica se áreas secundárias são desativadas sob carga alta.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

# Mock do logger para evitar travas
from cortex.system_2 import behavior_tree_manager as btm
btm.log_event = MagicMock()

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus

def test_load_based_gating():
    print("--- INICIANDO TESTE DE GATING CEREBRAL ---")
    
    orchestrator = CognitiveOrchestrator()
    
    # Caso 1: Carga Baixa (0%) - Tudo ativo
    print("\n[Cenário 1] Carga 10% (Baixa)")
    orchestrator.tick({"system_load": 10})
    
    limbic_active = orchestrator.blackboard.get("area_Limbic_System_active")
    motor_active = orchestrator.blackboard.get("area_Motor_Cortex_active")
    
    print(f"Limbic System: {'Ativo' if limbic_active else 'GATED'}")
    print(f"Motor Cortex: {'Ativo' if motor_active else 'GATED'}")
    
    assert limbic_active is True
    assert motor_active is True

    # Caso 2: Carga Alta (90%) - Gating ativado
    print("\n[Cenário 2] Carga 90% (Alta)")
    orchestrator.tick({"system_load": 90})
    
    limbic_active = orchestrator.blackboard.get("area_Limbic_System_active")
    motor_active = orchestrator.blackboard.get("area_Motor_Cortex_active")
    
    print(f"Limbic System: {'Ativo' if limbic_active else 'GATED'}")
    print(f"Motor Cortex: {'Ativo' if motor_active else 'GATED'}")
    
    assert limbic_active is False
    assert motor_active is False
    print("\n✅ SUCESSO: Gating dinâmico funcionando via Blackboard!")

if __name__ == "__main__":
    try:
        test_load_based_gating()
    except AssertionError as e:
        print(f"\n❌ FALHA NO TESTE: {e}")
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
