import sys
from pathlib import Path

# Adicionar o caminho do projeto ao sys.path para importar os módulos
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

try:
    from cortex.logic.consolidation_engine import run_rest_cycle
    from cortex.specialists.dream_engine import generate_oneiric_snapshot
    from neural_bridge import log_event

    print("--- [SIMULAÇÃO FASE 15: IMAGINAÇÃO E TROPISMO] ---")
    
    # 1. Teste isolado do Motor Onírico
    print("\n[MOTOR ONÍRICO] Gerando primeiro sonho...")
    dream = generate_oneiric_snapshot()
    if dream["status"] == "DREAMING_SUCCESS":
        print(f"✔️ Sonho capturado: {dream['insight']['interpretation']}")
    else:
        print(f"⚠️ Alerta Onírico: {dream['message']}")

    # 2. Teste do Ciclo Integrado (Poda + Tropismo + Sonho)
    print("\n[CICLO DE DESCANSO] Executando rotina completa...")
    res = run_rest_cycle()
    
    print(f"✔️ Poda: {res['pruning']['removed']} conexões removidas.")
    print(f"✔️ Tropismo: {res['tropism'].get('new_links', 0)} novas conexões atraídas por Hubs.")
    print(f"✔️ Sonho: {res['dream'].get('status', 'ERROR')}")
    
    print("\n--- [SIMULAÇÃO CONCLUÍDA COM SUCESSO] ---")

except Exception as e:
    print(f"\n❌ ERRO NA SIMULAÇÃO: {str(e)}")
    import traceback
    traceback.print_exc()
