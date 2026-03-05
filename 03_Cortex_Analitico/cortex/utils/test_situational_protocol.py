"""
🛠️ Teste de Protocolo Situacional Dinâmico (Fase 19)
Verifica se a Melanora troca árvores inteiras conforme a situação.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator
from neural_bridge import log_event

def test_situational_protocol():
    print("--- INICIANDO TESTE DE PROTOCOLO SITUACIONAL ---")
    orchestrator = CognitiveOrchestrator()
    context = {"is_deep": True, "user_prompt": "Teste"}

    # Cena 1: Situação RESEARCH
    print("\n[CENA 1] Modo: RESEARCH")
    orchestrator.blackboard.set("situational_id", "RESEARCH")
    res1 = orchestrator.tick(context)
    if "Grounded_Research" in res1["results"]:
        print("✅ SUCESSO: Alternou para a Árvore de Pesquisa Densa.")
    else:
        print("❌ FALHA: Não detectou o modo RESEARCH.")

    # Cena 2: Situação EMERGENCY (Caminho rápido via Blackboard)
    print("\n[CENA 2] Modo: EMERGENCY (via surprise_detected)")
    orchestrator.blackboard.set("surprise_detected", True)
    orchestrator.context["results"] = {}
    res2 = orchestrator.tick(context)
    if "Rapid_Stabilization" in res2["results"]:
        print("✅ SUCESSO: Prioridade absoluta de emergência respeitada!")
    else:
        print("❌ FALHA: Emergência ignorada.")

    # Cena 3: Situação DEFAULT (Normal)
    print("\n[CENA 3] Modo: DEFAULT (Operação Normal)")
    orchestrator.blackboard.set("surprise_detected", False)
    orchestrator.blackboard.set("situational_id", "DEFAULT")
    orchestrator.context["results"] = {}
    res3 = orchestrator.tick(context)
    if "Finalize_Phase" in res3["results"]:
        print("✅ SUCESSO: Retornou ao fluxo de operação padrão.")
    else:
        print("❌ FALHA: Não retornou ao DEFAULT.")

if __name__ == "__main__":
    test_situational_protocol()
