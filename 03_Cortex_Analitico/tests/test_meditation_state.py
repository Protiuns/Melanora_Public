import json
import time
from pathlib import Path

# Paths
BASE_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico")
STATE_FILE = BASE_DIR / "config" / "neural_state.json"

def trigger_meditation():
    print("🧪 Teste: Solicitando Meditação ao Monk Agent...")
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {}
    
    state["is_meditating"] = True
    state["meditation_cycles_remaining"] = 30 # Ciclos rápidos
    
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    print("✅ Estado alterado para is_meditating=True. Verifique os logs do bridge.")

if __name__ == "__main__":
    trigger_meditation()
