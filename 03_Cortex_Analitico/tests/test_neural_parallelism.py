import json
import time
from pathlib import Path

CONFIG_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico/config")
QUEUE_FILE = CONFIG_DIR / "task_queue.json"
RESULTS_FILE = CONFIG_DIR / "results_buffer.json"

def inject_test_tasks():
    print("🧪 Injetando tarefas de teste (Paralelismo v4.1)...")
    tasks = [
        {"module": "semantic_memory", "function": "search", "params": {"query": "teste epic"}, "weight": 95, "tags": ["epic"]},
        {"module": "semantic_memory", "function": "search", "params": {"query": "teste fast"}, "weight": 20, "tags": ["fast"]},
        {"module": "semantic_memory", "function": "search", "params": {"query": "teste med"}, "weight": 50, "tags": ["medium"]}
    ]
    
    queue_data = {"queue": tasks}
    QUEUE_FILE.write_text(json.dumps(queue_data, indent=2), encoding="utf-8")
    print("✅ Tarefas injetadas. Aguardando processamento...")

if __name__ == "__main__":
    inject_test_tasks()
    
    # Monitorar resultados
    start = time.time()
    results_found = []
    while len(results_found) < 3 and time.time() - start < 30:
        if RESULTS_FILE.exists():
            data = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
            pending = data.get("pending", [])
            for res in pending:
                if res["task_id"] not in [r["task_id"] for r in results_found]:
                    results_found.append(res)
                    print(f"📦 Resultado recebido: {res['task_id']} (Status: {res['status']})")
        time.sleep(1)
    
    if len(results_found) == 3:
        print("\n✨ TESTE CONCLUÍDO COM SUCESSO! Todas as tarefas paralelas foram processadas.")
    else:
        print("\n❌ TESTE FALHOU ou TIMEOUT. Verifique os logs do Neural Bridge.")
