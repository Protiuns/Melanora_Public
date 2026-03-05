"""
🛠️ Teste de Priorização por Contexto (Fase 17)
Verifica se a Melanora escolhe tarefas leves quando o sistema está 'carregado'.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator
from neural_bridge import log_event

def test_context_prioritization():
    print("--- INICIANDO TESTE DE PRIORIZAÇÃO CONTEXTUAL ---")
    orchestrator = CognitiveOrchestrator()
    
    # Contexto 1: Sistema Ocioso (IDLE) -> Deve priorizar Consolidate_Knowledge (Prio 50)
    print("\n[CENA 1] Sistema Ocioso (Load 20%)")
    orchestrator.blackboard.set("system_load", 20)
    context_idle = {"user_prompt": "Update", "is_deep": True}
    res1 = orchestrator.tick(context_idle)
    
    # No tick, o PrioritySelector deve ter rodado o que tem maior peso.
    # Como usamos Selector, ele para no primeiro sucesso.
    # Consolidate (50) > Light (30) > Emotion (10)
    if "Consolidate_Knowledge" in res1["results"]:
        print("✅ SUCESSO: Priorizou tarefa PESADA no estado IDLE.")
    else:
        print("❌ FALHA: Não priorizou a tarefa pesada adequadamente.")

    # Contexto 2: Sistema Carregado (HIGH LOAD) -> Deve priorizar Light_Task (30) sobre Heavy (5)
    print("\n[CENA 2] Sistema Carregado (Load 80%)")
    orchestrator.blackboard.set("system_load", 80)
    orchestrator.context["results"] = {} # Limpa resultados
    res2 = orchestrator.tick(context_idle)
    
    # Agora: Light (30) > Emotion (10) > Consolidate (5)
    if "Update_Heartbeat" in res2["results"]:
        print("✅ SUCESSO: Priorizou tarefa LEVE no estado HIGH LOAD.")
    else:
        print("❌ FALHA: Continuou tentando tarefas pesadas sob carga.")

if __name__ == "__main__":
    test_context_prioritization()
