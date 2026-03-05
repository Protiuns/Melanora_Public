import json
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Caminhos de configuração
CONFIG_DIR = Path(__file__).parent.parent / "config"
PULSE_FILE = CONFIG_DIR / "user_pulse.json"
STATE_FILE = CONFIG_DIR / "neural_state.json"

@cortex_function
def analyze_user_flow() -> dict:
    """
    🧠 Analisa o rítmo de interação do usuário para detectar estados de Flow ou Caos.
    """
    if not PULSE_FILE.exists():
        return {"status": "INITIALIZING", "mode": "STASIS"}

    try:
        with open(PULSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        pulses = data.get("pulses", [])
        if len(pulses) < 3:
            return {"status": "COLLECTING_DATA", "mode": "STASIS"}

        # Calcular intervalos entre os últimos pulsos
        timestamps = [p["timestamp"] for p in pulses[-10:]]
        intervals = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        
        avg_interval = sum(intervals) / len(intervals)
        last_pulse_age = time.time() - timestamps[-1]

        # Classificação de Estado
        mode = "NORMAL"
        if last_pulse_age > 300: # 5 minutos de silêncio
            mode = "STASIS"
        elif avg_interval < 2.5: # Interações muito rápidas
            mode = "CHAOS"
        elif avg_interval < 20.0: # Rítmo constante de trabalho
            mode = "FLOW"

        # Atualizar o Estado Neural
        _update_symbiotic_mode(mode, avg_interval)

        return {
            "status": "ANALYZED",
            "mode": mode,
            "avg_interval_s": round(avg_interval, 2),
            "last_pulse_age_s": round(last_pulse_age, 2)
        }

    except Exception as e:
        log_event(f"Erro na Análise de Simbiose: {str(e)}", "ERROR")
        return {"status": "ERROR", "message": str(e)}

def _update_symbiotic_mode(mode: str, interval: float):
    """Reflete o estado de simbiose no neural_state.json."""
    if not STATE_FILE.exists(): return
    
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

        if state.get("symbiotic_mode") != mode:
            state["symbiotic_mode"] = mode
            state["last_mode_change"] = time.ctime()
            
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
            
            log_event(f"SIMBIOSE: Entrando em modo {mode} (Intervalo Médio: {interval:.1f}s)")
    except: pass

if __name__ == "__main__":
    print(analyze_user_flow())
