import sys
import os
from unittest.mock import MagicMock, patch

# Adiciona o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, Composite, Decorator, Action, Condition

def count_nodes(node):
    count = 1
    if isinstance(node, Composite):
        for child in node.children:
            count += count_nodes(child)
    elif isinstance(node, Decorator):
        count += count_nodes(node.child)
    return count

def test_jump_to_100_audit():
    print("--- AUDITORIA DO CONECTOMA: O SALTO PARA 100 ---")
    
    with patch("cortex.system_2.deep_architect.ask_ollama", return_value="Audit Success"):
        orchestrator = CognitiveOrchestrator()
        
        # 1. Auditoria de Árvore
        total_bt_nodes = count_nodes(orchestrator.root)
        print(f"\n[BT] Total de Nodos na Árvore de Comportamento: {total_bt_nodes}")
        
        # 2. Auditoria de Funções/Métodos (Neurônios Funcionais)
        # Contamos métodos da classe que começam com 'bt_' ou 'motor_' ou 'limbic_'
        functional_methods = [m for m in dir(orchestrator) if m.startswith(('bt_', 'motor_', 'limbic_'))]
        total_methods = len(functional_methods)
        print(f"[Core] Total de Arcos Reflexos/Lógica (Métodos): {total_methods}")
        
        total_connectome = total_bt_nodes + total_methods
        print(f"\n[Resultado] Complexidade Total Segmentada: {total_connectome}")
        
        if total_connectome >= 100:
            print("\n✅ SUCESSO: Atingimos a meta de 100+ Neurônios Funcionais!")
        else:
            print(f"\n⚠️ AVISO: Faltam {100 - total_connectome} unidades para a meta.")

        # 3. Teste de Estabilidade
        print("\n[Estabilidade] Executando 3 ciclos de pulso completo...")
        try:
            for i in range(3):
                res = orchestrator.tick({"user_prompt": f"Teste de Estabilidade {i}", "system_load": 20})
                print(f" -> Ciclo {i} status: {res['status']}")
            print("✅ Estabilidade verificada!")
        except Exception as e:
            print(f"❌ Falha na estabilidade: {e}")
            sys.exit(1)

if __name__ == "__main__":
    test_jump_to_100_audit()
