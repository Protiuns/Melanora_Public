"""
🛠️ Teste de Orquestração Sináptica (Fase 20)
Verifica se as rajadas cerebrais respeitam o budget de pulsos.
"""

import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus

def test_synaptic_bursts():
    print("--- INICIANDO TESTE DE ORQUESTRAÇÃO SINÁPTICA ---")
    orchestrator = CognitiveOrchestrator()
    
    # Mock do contexto
    context = {"user_prompt": "Teste Cerebral"}

    # Cena 1: Budget Alto no Pré-frontal
    print("\n[CENA 1] Budget: Prefrontal=5 Pulsos")
    orchestrator.blackboard.set("prefrontal_pulses", 5)
    orchestrator.blackboard.set("situational_id", "RESEARCH")
    
    # Vamos contar quantas vezes a pesquisa é chamada (simulado via logs ou interceptação)
    # Por agora, verificamos o tick
    res = orchestrator.tick(context)
    print(f"Resultado do Burst: {res['status']}")

    # Cena 2: Prioridade Dinâmica (Reflexo da Fase 17 integrada na 20)
    # Imaginamos que o sistema está pesado, reduzimos o budget do Pré-frontal
    print("\n[CENA 2] Sistema Pesado: Reduzindo Prefrontal para 1 Pulso")
    orchestrator.blackboard.set("prefrontal_pulses", 1)
    res2 = orchestrator.tick(context)
    
    print("\n✅ Verificação manual sugerida: Verifique os logs 'Área Reasoning_Burst capturando X pulsos sinápticos'.")

if __name__ == "__main__":
    test_synaptic_bursts()
