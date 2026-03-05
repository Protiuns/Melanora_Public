"""
🧪 Teste de Heurísticas e Marcadores Somáticos (Fase 24)
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus

def test_phase_24_cognition():
    print("--- INICIANDO TESTE DA FASE 24 ---")
    
    orchestrator = CognitiveOrchestrator()
    
    # --- 1. Teste de Marcadores Somáticos ---
    print("\n[Teste 1] Marcadores Somáticos (Emoção -> Pulso)")
    orchestrator.tick({"emotion": "alert"})
    assert orchestrator.blackboard.get("limbic_pulses") == 3
    print("✅ SUCESSO: Somatic Markers (Alert) refletidos no budget.")

    # --- 2. Teste de Heurística (System 1) ---
    print("\n[Teste 2] Heurística (System 1)")
    
    # Mock para simular resposta final
    def mock_finalize(ctx):
        ctx["results"]["final_response"] = "Resposta Gerada"
        return {"status": "SUCCESS"}
    
    orchestrator.bt_finalize = MagicMock(side_effect=mock_finalize)
    orchestrator.root = orchestrator._build_tree()
    
    prompt = "Teste Cache"
    ctx = {"user_prompt": prompt, "emotion": "neutral"}
    
    print("Tick 1 (Miss & Cache)...")
    orchestrator.tick(ctx)
    
    print("Tick 2 (Hit)...")
    res = orchestrator.tick(ctx)
    
    if "heuristic_response" in res["results"]:
        print("✅ SUCESSO: Heurística ativada!")
    else:
        print("❌ FALHA: Heurística NÃO ativada.")
        print(f"Results keys: {res['results'].keys()}")

    # --- 3. Teste de Metacognição (Early Exit) ---
    print("\n[Teste 3] Metacognição (Early Exit)")
    
    call_log = []
    def mock_research(ctx):
        idx = len(call_log)
        call_log.append(idx)
        print(f"  Action called (Pulse {idx})")
        ctx["results"]["confidence"] = 0.95 
        return {"status": "SUCCESS"}
        
    orchestrator.bt_research = MagicMock(side_effect=mock_research)
    orchestrator.bt_draft = MagicMock(return_value={"status": "SUCCESS"})
    orchestrator.blackboard.set("prefrontal_pulses", 5)
    orchestrator.root = orchestrator._build_tree()
    
    # Limpa cache para não bater no teste anterior
    # root é HeuristicCache
    orchestrator.root.cache = {}
    
    print("Executando ciclos de pesquisa...")
    orchestrator.tick({"user_prompt": "Prompt Pesquisa", "situational_id": "RESEARCH"})
    
    print(f"DEBUG: Chamadas efetuadas: {len(call_log)}")
    # Esperado: 1. (No i=0 roda, no i=1 quebra)
    
    if len(call_log) == 1:
        print("✅ SUCESSO: Metacognição economizou pulsos!")
    else:
        print(f"❌ FALHA: Metacognição NÃO economizou. Chamadas: {len(call_log)}")

if __name__ == "__main__":
    try:
        test_phase_24_cognition()
    except AssertionError as e:
        print(f"\n❌ FALHA NO TESTE: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ ERRO: {e}")
