import sys
import os
import time
from unittest.mock import MagicMock, patch

# Adiciona o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus

def test_phase_33_circuitry_metrics():
    print("--- INICIANDO TESTE DA FASE 33: MÉTRICAS DE CIRCUITRIA NEURAL ---")
    
    # Mock das funções de LLM para evitar chamadas reais
    with patch("cortex.system_2.deep_architect.ask_ollama", return_value="Resposta Mock"):
        orchestrator = CognitiveOrchestrator()
        
        # Simula alguns ciclos para acumular métricas
        print("\n[Carga] Simulando 5 ciclos de processamento...")
        for i in range(5):
            # Injeta contextos diferentes para variar a 'Voltagem' (V)
            load = 20 + (i * 10)
            orchestrator.tick({"user_prompt": f"Teste Ciclo {i}", "system_load": load})
            
        # Verifica se as métricas foram populadas no Blackboard
        bb = orchestrator.blackboard
        print("\n[Métricas] Auditando Componentes (V, I, R):")
        
        for node_name, metrics in bb.node_metrics.items():
            v, r, i = metrics["V"], metrics["R"], metrics["I"]
            print(f" -> Nodo: {node_name:20} | V: {v:3} | I: {i:3} | R: {r:6.2f}ms")
            
        assert len(bb.node_metrics) > 0, "Nenhuma métrica foi coletada!"
        
        # Testa gatilho de fusão (simulado)
        # Criamos um nodo artificial com R baixo e V baixo
        bb.node_metrics["Low_Energy_Node"] = {"V": 0.5, "R": 2, "I": 20}
        
        print("\n[Análise] Verificando logs de recomendação (Fissão/Fusão)...")
        # O tick final deve processar essas métricas e logar as recomendações
        orchestrator.tick({"user_prompt": "Análise Final"})

    print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")

if __name__ == "__main__":
    test_phase_33_circuitry_metrics()
