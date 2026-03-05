"""
🧪 Teste de Arcos Reflexos Motores (Fase 29)
Verifica a integração entre a Behavior Tree e o Córtex Motor Local.
"""

import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus, MotorReflex

def test_phase_29_bt_integration():
    print("--- INICIANDO TESTE DA FASE 29: INTEGRAÇÃO BT-MOTOR ---")
    
    # Patching no nível da classe para garantir o binding correto
    with patch.object(CognitiveOrchestrator, 'bt_research', return_value={"status": NodeStatus.SUCCESS, "output": "Research OK"}), \
         patch.object(CognitiveOrchestrator, 'bt_draft', return_value={"status": NodeStatus.SUCCESS, "output": "Draft OK"}), \
         patch.object(CognitiveOrchestrator, 'bt_finalize', return_value={"status": NodeStatus.SUCCESS, "output": "Final OK"}), \
         patch("requests.post") as mock_post:
        
        # Configura o mock do post para retorno de sucesso
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "file": "neural_sight/test.png"}
        mock_post.return_value = mock_response
        
        orchestrator = CognitiveOrchestrator()
        print("\n[Teste 1] Disparo de Reflexo Digital_Sight via Orquestrador")
        orchestrator.tick({"user_prompt": "Teste Reflexo"})
        
        print(f"DEBUG: Results: {orchestrator.context['results']}")
        
        # Verifica se o endpoint correto foi chamado
        found_call = False
        for call in mock_post.call_args_list:
            if "reflex/digital_sight" in call[0][0]:
                found_call = True
                break
        
        assert found_call
        print("✅ SUCESSO: Behavior Tree disparou o reflexo motor corretamente.")

def test_phase_29_api_logic():
    print("\n--- TESTANDO LÓGICA DA API DO CÓRTEX MOTOR ---")
    from cortex.Cortex_Motor_Local.motor_cortex_api import app
    
    # Usando o test_client do Flask para testar os novos endpoints sem subir o servidor
    with app.test_client() as client:
        # Teste do Screen Snapshot (Digital Sight)
        # Nota: Pode falhar em ambientes sem display, então focamos na rota existir
        print("[Teste 2] Verificando existência de endpoints de reflexo...")
        
        # Testamos o status
        res = client.get('/')
        assert res.status_code == 200
        assert b"Local Motor Cortex" in res.data
        
        # Testamos a estrutura do reflexo de arquivo (sem mover arquivos reais)
        res = client.post('/reflex/file_dispatch', json={})
        # Deve retornar 400 por falta de params, provando que a rota existe e valida
        assert res.status_code == 400
        print("✅ SUCESSO: Endpoints de reflexo registrados e validando parâmetros.")

if __name__ == "__main__":
    try:
        # mock de log_event para não poluir
        with patch("neural_bridge.log_event"):
            test_phase_29_bt_integration()
            # test_phase_29_api_logic() # Pode ter problemas de import dependendo da estrutura de pastas
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ ERRO: {e}")
