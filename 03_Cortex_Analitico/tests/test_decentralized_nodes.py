import logging
import sys
import os
import shutil
from pathlib import Path

# Garantir que o diretorio root do script seja alcancado
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cortex.utils.synaptic_core import SynapticCore, SYNAPSE_BASE_DIR

logging.basicConfig(level=logging.INFO, format="%(message)s")

def test_decentralized_summation():
    print("="*60)
    print("TESTE: SOMAÇÃO NEURAL DESCENTRALIZADA & PERSISTÊNCIA")
    print("="*60)
    
    # Limpeza inicial para o teste
    if SYNAPSE_BASE_DIR.exists():
        for f in SYNAPSE_BASE_DIR.glob("*.json"):
            try:
                os.remove(f)
            except Exception:
                pass
    SYNAPSE_BASE_DIR.mkdir(parents=True, exist_ok=True)

    node_id = "test_node_01"
    
    # 1. Primeira Carga (Deve persistir no disco)
    print(f"\n[STEP 1] Carregando {node_id} com 40.0...")
    SynapticCore.charge_and_check(node_id, 40.0)
    
    node_file = SYNAPSE_BASE_DIR / f"{node_id}.json"
    if node_file.exists():
        print(f"[OK] Arquivo de estado persistido: {node_file.name}")
    
    # 2. Simular reinicialização (Limpando do cache da memória)
    print("\n[STEP 2] Simulando Reinicialização do Sistema...")
    SynapticCore._nodes.clear() # Limpa o singleton em memória
    
    node = SynapticCore.get_node(node_id)
    print(f"Potencial recuperado do disco: {node.potential:.1f}")
    
    if abs(node.potential - 38.0) < 0.1: # 40 * (1 - 0.05) = 38
        print("[OK] Somação com decaimento persistida com sucesso.")
    else:
        print(f"[ERRO] Potencial incorreto: {node.potential}")

    # 3. Disparo Independente
    print(f"\n[STEP 3] Carregando {node_id} até o disparo (Threshold=100)...")
    fired = SynapticCore.charge_and_check(node_id, 70.0)
    
    if fired:
        print(f"[OK] Nodo {node_id} disparou!")
        print(f"Potencial residual: {SynapticCore.get_node(node_id).potential:.1f}")
    else:
        print(f"[ERRO] Nodo não disparou. Potencial: {SynapticCore.get_node(node_id).potential}")

    # 4. Resiliência: Criar um segundo nodo
    print("\n[STEP 4] Testando autonomia de múltiplos nodos...")
    node_id_2 = "test_node_02"
    SynapticCore.charge_and_check(node_id_2, 50.0)
    
    p1 = SynapticCore.get_node(node_id).potential
    p2 = SynapticCore.get_node(node_id_2).potential
    
    print(f"Node 1 Potential: {p1:.1f}")
    print(f"Node 2 Potential: {p2:.1f}")
    
    if p1 != p2:
        print("[OK] Nodos operam de forma independente e descentralizada.")

if __name__ == "__main__":
    test_decentralized_summation()
