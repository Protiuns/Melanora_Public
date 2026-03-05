"""
🛠️ Teste de Evolução de Comportamento (Fase 16)
Verifica Blackboards, Decoradores e Transições Emocionais.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator
from neural_bridge import log_event

def test_emotional_bt():
    print("--- INICIANDO TESTE DE EVOLUÇÃO COMPORTAMENTAL ---")
    orchestrator = CognitiveOrchestrator()
    
    # Ciclo 1: Melancolia (Default)
    context = {"user_prompt": "Como está o projeto?", "is_deep": True}
    print("\n[TICK 1] Esperado: Fluxo de Melancolia (Pesquisa + Consalidação)")
    res1 = orchestrator.tick(context)
    print(f"Humor Atual: {orchestrator.blackboard.get('emotion')}")
    print(f"Fases executadas: {list(res1['results'].keys())}")

    # Forçar transição (Ciclo 2, 3...)
    print("\n[TICK 2] Mantendo Melancolia...")
    orchestrator.tick(context)
    
    print("\n[TICK 3] Gatilho de Transição!")
    orchestrator.tick(context)
    print(f"Humor após Tick 3: {orchestrator.blackboard.get('emotion')}")
    
    # Ciclo 4: Euforia
    print("\n[TICK 4] Esperado: Fluxo de Euforia (Draft Rápido + Finalize)")
    orchestrator.context["results"] = {} # Limpa resultados para novo teste
    res4 = orchestrator.tick(context)
    print(f"Fases executadas na Euforia: {list(res4['results'].keys())}")

    if "Euphoric_Creative_Draft" in res4['results'] and orchestrator.blackboard.get('emotion') == 'euphoria':
        print("\n✅ SUCESSO: A árvore evoluiu e alternou humores autonomamente!")
    else:
        print("\n❌ FALHA: Transição emocional ou Decoradores falharam.")

if __name__ == "__main__":
    test_emotional_bt()
