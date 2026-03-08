"""
🔄 Melanora Consolidation Engine (v1.0)
Motor de descanso e reforço sináptico do Córtex Analítico.
Executa Poda Sináptica (Pruning) e Consolidação de Memória (LTP/LTD).
"""

import os
import json
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Interconexões de Lógica
try:
    from cortex.logic.synthesis_engine import load_qualia
    QUALIA_AVAILABLE = True
except ImportError:
    QUALIA_AVAILABLE = False

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
CONNECTOME_FILE = CONFIG_DIR / "abstract_connections.json"

@cortex_function
def run_rest_cycle(depth: str = "LIGHT") -> dict:
    """Executa todas as rotinas do ciclo de descanso (Consolidação)."""
    log_event("Iniciando Ciclo de Descanso e Consolidação...")
    
    # 1. Poda Sináptica (Limpeza)
    pruning_res = synaptic_pruning(hits_threshold=10)
    
    # 2. Consolidação de Qualia
    qualia_res = consolidate_sensory_qualia()
    
    # 3. Tropismo Sináptico (Atração de Hubs) - NOVO
    tropism_res = apply_synaptic_tropism()
    
    # 4. Síntese Onírica (Sonho) - NOVO
    try:
        from cortex.specialists.dream_engine import generate_oneiric_snapshot
        dream_res = generate_oneiric_snapshot()
    except ImportError:
        dream_res = {"status": "OFFLINE"}
    
    results = {
        "pruning": pruning_res,
        "qualia_consolidation": qualia_res,
        "tropism": tropism_res,
        "dream": dream_res,
        "integrity": network_integrity_check(),
        "timestamp": time.ctime()
    }
    
    log_event(f"Ciclo concluído. Hubs Ativos: {tropism_res.get('hubs_found', 0)}. Sonho gerado.")
    return results

def synaptic_pruning(hits_threshold: int = 10) -> dict:
    """Consolida memórias e remove conexões fracas/redundantes."""
    if not CONNECTOME_FILE.exists():
        return {"removed": 0, "status": "NO_FILE"}
    
    try:
        with open(CONNECTOME_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        original_count = len(data.get("connections", {}))
        # REM-style Pruning: se Hits < threshold, remove.
        new_conns = {}
        for k, v in data["connections"].items():
            if v["hits"] >= hits_threshold:
                new_conns[k] = v
            # Throttling para não travar CPU
            time.sleep(0.01)
        
        data["connections"] = new_conns
        with open(CONNECTOME_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
        return {
            "original": original_count,
            "current": len(new_conns),
            "removed": original_count - len(new_conns)
        }
    except Exception as e:
        return {"error": str(e)}

def network_integrity_check() -> dict:
    """Verifica se as camadas e diretórios mapeados ainda existem fisicamente."""
    state_file = CONFIG_DIR / "neural_state.json"
    if not state_file.exists(): return {"status": "NO_STATE"}
    
    # Verificação física de caminhos críticos
    critical_paths = [
        BASE_DIR / "cortex",
        BASE_DIR / "config",
        BASE_DIR / "dashboard"
    ]
    
    missing = [str(p) for p in critical_paths if not p.exists()]
    
    if missing:
        log_event(f"Falha de integridade física: {len(missing)} pastas ausentes.", "CRITICAL")
        return {"status": "CORRUPTED", "missing": missing}
        
    return {"status": "INTEGRITY_VERIFIED", "health": 1.0}

@cortex_function
def calculate_long_term_reinforcement(agent_id: str, success: bool):
    """Reforço de Longo Prazo (LTP) ou Depressão (LTD) baseado em uso real."""
    # Lógica para alterar o peso_vivo no definition.md do agente
    # Newton: O lado analítico 'escava' o peso vivo do criativo.
    pass

def consolidate_sensory_qualia() -> dict:
    """Reforça padrões sensoriais que atingiram estabilidade."""
    if not QUALIA_AVAILABLE: return {"status": "OFFLINE"}
    
    qualia = load_qualia()
    stable = qualia.get("stable_qualia", {})
    
    # Simula reforço sináptico baseado em qualia estável
    for q_id, data in stable.items():
        if data["hits"] > 5:
            log_event(f"Consolidando Qualia: {q_id} (Hits: {data['hits']})")
            
    return {"status": "OK", "stable_count": len(stable)}

def apply_synaptic_tropism(hit_threshold: int = 50) -> dict:
    """
    🧲 Tropismo Sináptico: Neurônios ativos (Hubs) atraem novas conexões.
    """
    if not CONNECTOME_FILE.exists():
        return {"status": "NO_FILE", "hubs_found": 0}

    try:
        with open(CONNECTOME_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        connections = data.get("connections", {})
        hub_candidates = {}

        # Identificar Hubs baseados em Hits
        for conn_id, conn in connections.items():
            source = conn["source"]
            target = conn["target"]
            hub_candidates[source] = hub_candidates.get(source, 0) + conn["hits"]
            hub_candidates[target] = hub_candidates.get(target, 0) + conn["hits"]

        hubs = [node for node, hits in hub_candidates.items() if hits >= hit_threshold]
        
        if not hubs:
            return {"status": "STABLE", "hubs_found": 0}

        new_tropic_links = 0
        # Tentar atrair conexões entre Hubs e nós aleatórios (Simulando Axonal Guidance)
        all_nodes = list(hub_candidates.keys())
        for hub in hubs:
            # Selecionar um nó potencial que ainda não está fortemente conectado ao Hub
            potential_target = random.choice(all_nodes)
            if potential_target != hub:
                conn_id = f"{hub}->{potential_target}"
                if conn_id not in connections:
                    # Criar 'Link Trópico' (Conexão atraída pela gravidade neural)
                    connections[conn_id] = {
                        "source": hub,
                        "target": potential_target,
                        "hits": 1, 
                        "total_intensity": 0.1,
                        "first_seen": time.ctime(),
                        "last_seen": time.ctime(),
                        "type": "TROPIC_BOND" # Marcador de crescimento orgânico
                    }
                    new_tropic_links += 1
                    time.sleep(0.01) # Throttling orgânico

        if new_tropic_links > 0:
            data["connections"] = connections
            with open(CONNECTOME_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            log_event(f"Tropismo: Hubs atraíram {new_tropic_links} novas conexões sinápticas.")

        return {
            "status": "GROWTH_DETECTED",
            "hubs_found": len(hubs),
            "new_links": new_tropic_links
        }

    except Exception as e:
        log_event(f"Erro no Tropismo: {str(e)}", "ERROR")
        return {"error": str(e)}

import random
