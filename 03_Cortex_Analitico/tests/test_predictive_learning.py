import logging
import sys
import os
import json
import time
from pathlib import Path

# Configurar logs para o teste
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Garantir que o diretorio root seja alcancado
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from neural_bridge import process_task, CORTEX_REGISTRY, read_json, write_json
from cortex.logic.predictive_observer import PredictiveObserver

CONFIG_DIR = Path(BASE_PATH) / "config"
MODEL_FILE = CONFIG_DIR / "expectation_model.json"

def mock_func(delay=0.01, fail=False):
    time.sleep(delay)
    if fail:
        raise Exception("Erro simulado")
    return {"status": "OK", "data": "test"}

def test_predictive_learning():
    print("="*60)
    print("TESTE DE APRENDIZADO PREDITIVO (FASE ALPHA)")
    print("="*60)
    
    # 0. Limpeza do ambiente
    if MODEL_FILE.exists():
        os.remove(MODEL_FILE)
    PredictiveObserver._model = {}
    
    # Registrar func de mock
    CORTEX_REGISTRY["test_mod"] = {"run": mock_func}
    
    # 1. Treinamento: Estabelecer expectativa de 10-20ms
    print("\n[STEP 1] Treinando sistema com tarefas previsiveis (5x)...")
    for i in range(5):
        task = {"id": f"T{i}", "module": "test_mod", "function": "run", "params": {"delay": 0.02}}
        res = process_task(task)
        print(f"  Tarefa {i}: {res['elapsed_ms']}ms | Surpresa: {res.get('surprise')}")

    # Verificar se o modelo foi salvo
    PredictiveObserver.load_model()
    exp = PredictiveObserver.get_expectation("test_mod", "run")
    print(f"\nExpectativa consolidada: {exp['avg_ms']}ms | Sucesso: {exp['success_rate']}")

    # 2. O Evento de Surpresa: Atraso massivo (Simular crash/lentidao)
    print("\n[STEP 2] Simulando evento SURPREENDENTE (Atraso de 500ms)...")
    task_surprise = {"id": "T_SURPRISE", "module": "test_mod", "function": "run", "params": {"delay": 0.5}}
    res_surprise = process_task(task_surprise)
    
    surprise_val = res_surprise.get("surprise", 0)
    print(f"  Resultado: {res_surprise['elapsed_ms']}ms | Surpresa: {surprise_val}")
    
    if surprise_val >= 1.5:
        print("[OK] Sistema detectou alta surpresa para anomalia de tempo.")
    else:
        print(f"[ERRO] Surpresa insuficiente: {surprise_val}")

    # 3. O Evento de Surpresa: Erro inesperado
    print("\n[STEP 3] Simulando evento SURPREENDENTE (Erro critico)...")
    task_fail = {"id": "T_FAIL", "module": "test_mod", "function": "run", "params": {"fail": True}}
    res_fail = process_task(task_fail)
    
    surprise_fail = res_fail.get("surprise", 0)
    print(f"  Status: {res_fail['status']} | Surpresa: {surprise_fail}")
    
    if surprise_fail >= 2.0:
        print("[OK] Sistema detectou alta surpresa para falha inesperada.")
    else:
        print(f"[ERRO] Surpresa insuficiente: {surprise_fail}")

if __name__ == "__main__":
    test_predictive_learning()
