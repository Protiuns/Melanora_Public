"""
🛠️ Teste de Autonomia Analítica (Fase 15)
Verifica se a Melanora consegue rodar um ciclo de Aprendizado Grounded por conta própria.
"""

import sys
from pathlib import Path

# Adiciona o diretório base ao path para importação
sys.path.append(str(Path(__file__).parent.parent.parent))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator
from neural_bridge import log_event

def test_autonomous_learning():
    print("--- INICIANDO TESTE DE APRENDIZADO AUTÔNOMO ---")
    orchestrator = CognitiveOrchestrator()
    
    # Simula um prompt que exige pensamento profundo e pesquisa
    context = {
        "user_prompt": "Quais são as regras de integridade do Newton no manual v1.0?",
        "is_deep": True
    }
    
    print(f"Executando tick da árvore para o prompt: '{context['user_prompt']}'")
    result = orchestrator.tick(context)
    
    print("\n--- RESULTADO DO CICLO ---")
    print(f"Status Final: {result['status']}")
    
    for phase, output in result['results'].items():
        print(f"\n[{phase}]:")
        if isinstance(output, dict):
            print(f"  Status: {output.get('status')}")
            if 'synced_count' in output:
                print(f"  Arquivos Sincronizados: {output['synced_count']}")
        else:
            print(f"  Preview: {str(output)[:100]}...")

    if "Knowledge_Consolidation_Phase" in result['results']:
        print("\n✅ SUCESSO: O nó de Consolidação foi executado autonomamente!")
    else:
        print("\n❌ FALHA: O nó de Consolidação não foi atingido.")

if __name__ == "__main__":
    test_autonomous_learning()
