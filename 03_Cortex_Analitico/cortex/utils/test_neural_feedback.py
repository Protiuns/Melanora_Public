"""
🛠️ Teste de Feedback Neural (Fase 18)
Verifica se as respostas do LLM "sentem" o contexto da Behavior Tree.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator
from neural_bridge import log_event

def test_neural_feedback():
    print("--- INICIANDO TESTE DE FEEDBACK NEURAL ---")
    orchestrator = CognitiveOrchestrator()
    
    # Simula o pedido
    context = {"user_prompt": "Explique o sistema de arquivos.", "is_deep": True}

    print("\n[CENA 1] Melancolia + Load Baixo")
    orchestrator.blackboard.set("emotion", "melancholy")
    orchestrator.blackboard.set("system_load", 10)
    
    # Mock para ver o que chega no Ollama
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {"response": "Resposta Analítica"}
        orchestrator.tick(context)
        
        args, kwargs = mock_post.call_args
        sent_system = kwargs['json']['system']
        print(f"System Prompt enviado: {sent_system}")
        
        if "analítico, profundo e cauteloso" in sent_system and "MELANCHOLY" in sent_system:
            print("✅ SUCESSO: Contexto de Melancolia injetado corretamente!")
        else:
            print("❌ FALHA: Prompt de melancolia não detectado.")

    print("\n[CENA 2] Euforia + Load Alto")
    orchestrator.blackboard.set("emotion", "euphoria")
    orchestrator.blackboard.set("system_load", 90)
    orchestrator.context["results"] = {}

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {"response": "Resposta Rápida"}
        orchestrator.tick(context)
        
        args, kwargs = mock_post.call_args
        sent_system = kwargs['json']['system']
        print(f"System Prompt enviado: {sent_system}")
        
        if "criativo, rápido e expansivo" in sent_system and "extremamente conciso" in sent_system:
            print("✅ SUCESSO: Contexto de Euforia e Carga Alta injetados!")
        else:
            print("❌ FALHA: Prompt de euforia/carga não detectado.")

if __name__ == "__main__":
    test_neural_feedback()
