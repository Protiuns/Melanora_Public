"""
🧪 Teste de Sintonização Matemática Dinâmica (Fase 26)
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus

def test_phase_26_dynamic_tuning():
    print("--- INICIANDO TESTE DA FASE 26 ---")
    
    orchestrator = CognitiveOrchestrator()
    
    # --- 1. Teste de Ajuste de Pulso (Numerical Counter) ---
    print("\n[Teste 1] Ajuste de Pulso via Numerical Counter")
    
    # Simulamos um histórico de sucesso alto (1, 1, 1) -> deve sugerir 1 pulso
    orchestrator.blackboard.set("success_history", [1, 1, 1])
    
    print("Executando tick com histórico de sucesso...")
    orchestrator.tick({"user_prompt": "Teste Math"})
    
    pulses = orchestrator.blackboard.get("prefrontal_pulses")
    print(f"DEBUG: Prefrontal Pulses após Tuning: {pulses} (Esperado: 1)")
    assert pulses == 1
    print("✅ SUCESSO: Budget de pulsos reduzido por alta eficiência!")

    # --- 2. Teste de Ajuste de Abstração (Dimensional Scaler) ---
    print("\n[Teste 2] Ajuste de Abstração via Dimensional Scaler")
    
    # Simulamos carga alta (90%) -> deve recomendar dimensão 1D (abstraction_level = 1)
    orchestrator.blackboard.set("system_load", 90)
    orchestrator.blackboard.set("success_history", [0, 0, 0]) # Reseta para forçar mais pulsos se não fosse a carga
    
    print("Executando tick com carga alta...")
    orchestrator.tick({"user_prompt": "Teste Carga"})
    
    level = orchestrator.blackboard.get("abstraction_level")
    print(f"DEBUG: Abstraction Level após Tuning: {level} (Esperado: 1 para 1D)")
    assert level == 1
    print("✅ SUCESSO: Abstração reduzida para economizar recursos em carga alta!")

if __name__ == "__main__":
    try:
        test_phase_26_dynamic_tuning()
    except AssertionError as e:
        print(f"\n❌ FALHA NO TESTE: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ ERRO: {e}")
