"""
💓 Melanora Synaptic Wave Engine (v1.0)
Motor de ondas sinápticas de alta frequência para o Córtex Analítico.
Simula o fluxo de energia e o PICO de ativação em milissegundos.
"""

import time
import json
import math
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

STATE_FILE = Path(__file__).parent.parent / "config" / "neural_state.json"

@cortex_function
def process_wave_step(impulse, global_energy=0.5) -> dict:
    """
    Processa um único passo (onda) de um impulso neural.
    Retorna o estado atualizado do impulso.
    """
    if impulse.status == "PENDING":
        impulse.status = "PROCESSING"
        log_event(f"🌊 Ativando impulso {impulse.id}: {impulse.source_module}. {impulse.target_function}")

    # Simula o consumo de ciclos
    impulse.remaining_waves -= 1
    
    # Efeito colateral: rastro de calor/energia baseado no peso original
    heat = (impulse.original_weight / 100.0) * global_energy
    
    if impulse.remaining_waves <= 0:
        impulse.status = "COMPLETED"
        return {"completed": True, "heat_generated": heat}
    
    return {"completed": False, "heat_generated": heat}

@cortex_function
def run_synaptic_burst(agents_energies: dict, duration_ms: int = 1000) -> dict:
    """
    Simula uma explosão sináptica de alta frequência em uma sub-rede de agentes.
    
    agents_energies: { "AGENT_NAME": energy_level }
    duration_ms: tempo total da simulação
    """
    start_time = time.time()
    end_time = start_time + (duration_ms / 1000.0)
    
    # Parâmetros de simulação (Inspirados no v4.1 do modelo)
    # Frequência base: ~100 Hz (10ms por onda)
    wave_interval = 0.01 
    waves_count = 0
    total_momentum = 0.0
    
    # Snapshots de ativação
    history = []
    
    current_energies = agents_energies.copy()
    
    while time.time() < end_time:
        # Ciclo E -> C (Exploração -> Convergência) simplificado
        for agent, energy in current_energies.items():
            # Ruído sináptico natural (Exploração)
            noise = (math.sin(time.time() * 10) * 0.05)
            
            # Convergência (Atração para o PICO)
            if energy > 0.7:
                current_energies[agent] += (1.0 - energy) * 0.1 # Crystallization
            else:
                current_energies[agent] += noise
                
            # Clipping
            current_energies[agent] = max(0.0, min(1.0, current_energies[agent]))
            
        # Calcular Momentum Médio
        avg_energy = sum(current_energies.values()) / len(current_energies) if current_energies else 0
        total_momentum += avg_energy
        
        waves_count += 1
        time.sleep(wave_interval)
        
        # Registrar snapshot a cada 10 ondas
        if waves_count % 10 == 0:
            history.append({
                "wave": waves_count,
                "avg_energy": round(avg_energy, 3),
                "timestamp": round(time.time() - start_time, 3)
            })
            
    elapsed = time.time() - start_time
    
    result = {
        "status": "CONCLUDED",
        "duration_actual_ms": round(elapsed * 1000, 1),
        "waves_processed": waves_count,
        "frequency_actual_hz": round(waves_count / elapsed, 1),
        "final_momentum": round(total_momentum / waves_count, 3) if waves_count > 0 else 0,
        "history": history
    }
    
    log_event(f"Burst sináptico concluído: {waves_count} ondas a {result['frequency_actual_hz']} Hz")
    return result

@cortex_function
def update_brain_heartbeat():
    """Atualiza o batimento cardíaco (timestamp) no estado neural."""
    try:
        if STATE_FILE.exists():
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            state["timestamp"] = time.time()
            state["fase"] = "HEARTBEAT"
            STATE_FILE.write_text(json.dumps(state, indent=2))
            return True
    except Exception:
        pass
    return False
