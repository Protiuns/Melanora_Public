import time
import json
from pathlib import Path

STATE_FILE = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico/config/neural_state.json")

def test_heartbeat():
    print("🧪 Verificando Heartbeat Neural (Ciclos Contínuos)...")
    
    if not STATE_FILE.exists():
        print("❌ Erro: neural_state.json não encontrado.")
        return

    def get_cycle():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("ciclo_atual", 0)
        except:
            return 0

    c1 = get_cycle()
    print(f"Ciclo inicial: {c1}")
    time.sleep(1)
    c2 = get_cycle()
    print(f"Ciclo após 1s: {c2}")

    if c2 > c1:
        print(f"✅ Heartbeat Ativo! Incremento de {c2 - c1} ciclos.")
    else:
        print("❌ Falha: O contador de ciclos está estagnado. (O bridge está rodando?)")

if __name__ == "__main__":
    test_heartbeat()
