"""
🧪 Teste de Feedback Sináptico (Fase 21)
Verifica se o histórico de pulsos chega até a injeção de prompt do Ollama.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

# Importa o módulo ANTES de qualquer coisa para moccar o log_event
import cortex.system_2.behavior_tree_manager as btm
btm.log_event = MagicMock()

from cortex.system_2.deep_architect import ask_ollama
from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator

def test_synaptic_feedback_injection():
    print("--- INICIANDO TESTE DE FEEDBACK SINAPTICO ---")
    
    # Mock do requests.post para não precisar do Ollama rodando
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Resposta Simulada"}
        mock_post.return_value = mock_response

        # Criamos o orquestrador e configuramos budgets
        orchestrator = CognitiveOrchestrator()
        orchestrator.blackboard.set("prefrontal_pulses", 7)
        orchestrator.blackboard.set("situational_id", "DEFAULT")
        
        # Mock das ações para garantir sucesso da árvore
        orchestrator.bt_research = MagicMock(return_value={"output": "Pesquisa ok"})
        orchestrator.bt_draft = MagicMock(return_value={"output": "Draft ok"})
        orchestrator.bt_transition_emotion = MagicMock(return_value={"output": "Humor ok"})
        orchestrator.run_stabilization = MagicMock(return_value={"output": "Estabilizacao ok"})
        
        # Recria a árvore para carregar os mocks
        orchestrator.root = orchestrator._build_tree()

        # Executamos o ciclo
        print("\nExecutando ciclo com Prefrontal=7 pulsos...")
        result = orchestrator.tick({"user_prompt": "Como esta meu cerebro?"})
        print(f"DEBUG: Tick finalizado com status {result['status']}")
        
        # Verificamos o que foi enviado para o Ollama
        if mock_post.called:
            args, kwargs = mock_post.call_args
            payload = kwargs['json']
            system_prompt = payload['system']
            
            print(f"\nSystem Prompt Capturado:\n{system_prompt}")
            
            if "[RELATORIO NEURO-COGNITIVO:" in system_prompt:
                print("\nSUCESSO: O relatorio neuro-cognitivo foi injetado corretamente!")
            else:
                print("\nFALHA: O relatorio sinaptico nao foi encontrado no prompt.")
        else:
            print("\nFALHA: requests.post nao foi chamado (ask_ollama ignorado?)")

if __name__ == "__main__":
    test_synaptic_feedback_injection()
