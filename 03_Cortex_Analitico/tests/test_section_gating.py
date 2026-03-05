import logging
import sys
import os
import json
from pathlib import Path

# Garantir que o diretorio root do script seja alcancado
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cortex.logic.area_manager import AreaManager
from neural_bridge import process_task

logging.basicConfig(level=logging.INFO, format="%(message)s")

def test_section_gating():
    print("="*60)
    print("TESTE DE GATING LÍMBICO (SECTIONING)")
    print("="*60)
    
    AreaManager.load_configs()
    
    # 1. Teste de modulo VITAL (Deve estar sempre ativo)
    print("\n[STEP 1] Testando modulo VITAL (metrics_counter)...")
    allowed = AreaManager.is_allowed("metrics_counter")
    print(f"metrics_counter permitido: {allowed}")
    if not allowed:
        print("[ERRO] metrics_counter deveria estar sempre ativo.")
    
    # 2. Teste de modulo COGNITIVE (Inicialmente Ativo)
    print("\n[STEP 2] Testando modulo COGNITIVE (vision_module) - Inicialmente ACTIVE...")
    allowed = AreaManager.is_allowed("vision_module")
    print(f"vision_module permitido: {allowed}")
    
    # 3. Desativar COGNITIVE e testar
    print("\n[STEP 3] Desativando secao COGNITIVE...")
    AreaManager.set_section_status("COGNITIVE", "INACTIVE")
    
    allowed = AreaManager.is_allowed("vision_module")
    print(f"vision_module permitido apos desativacao: {allowed}")
    
    if not allowed:
        print("[OK] Gating bloqueou o modulo corretamente.")
    else:
        print("[ERRO] Gating falhou em bloquear o modulo.")
    
    # 4. Testar via process_task (Neural Bridge Integration)
    print("\n[STEP 4] Testando integracao com Neural Bridge (process_task)...")
    task = {
        "id": "TEST_GATED",
        "module": "vision_module",
        "function": "analyze_environment_visual",
        "params": {}
    }
    
    result = process_task(task)
    print(f"Status do resultado: {result['status']}")
    
    if result["status"] == "SECTION_GATED":
        print("[OK] Neural Bridge respeitou o bloqueio de secao.")
    else:
        print(f"[ERRO] Neural Bridge nao bloqueou a tarefa. Status: {result['status']}")

    # Resetar para o estado original para nao quebrar o sistema
    print("\n[RESET] Reativando secoes...")
    AreaManager.set_section_status("COGNITIVE", "ACTIVE")

if __name__ == "__main__":
    test_section_gating()
