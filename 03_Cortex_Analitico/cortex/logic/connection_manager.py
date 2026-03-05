"""
🔗 Melanora Connection Manager (v1.0)
Mapeia e monitora conexões abstratas entre regiões neurais.
Identifica "gargalos" e sugere a criação de novos agentes.
"""

import json
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Arquivo persistente para o mapa de conexões
CONNECTIONS_FILE = Path(__file__).parent.parent / "config" / "abstract_connections.json"

@cortex_function
def record_interaction(source: str, target: str, intensity: float = 1.0) -> dict:
    """Registra uma interação entre duas regiões neurais."""
    if not CONNECTIONS_FILE.exists():
        data = {"connections": {}, "last_refactor_suggestion": None}
    else:
        try:
            data = json.loads(CONNECTIONS_FILE.read_text(encoding="utf-8"))
        except:
            data = {"connections": {}, "last_refactor_suggestion": None}
            
    conn_id = f"{source}->{target}"
    
    conn = data["connections"].get(conn_id, {
        "source": source,
        "target": target,
        "hits": 0,
        "total_intensity": 0.0,
        "first_seen": time.ctime(),
        "last_seen": None
    })
    
    conn["hits"] += 1
    conn["total_intensity"] += intensity
    conn["last_seen"] = time.ctime()
    
    data["connections"][conn_id] = conn
    
    # Salvar
    CONNECTIONS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    
    # Verificar se precisa sugerir refatoração (Se hits > 50 e intensidade alta)
    if conn["hits"] > 50 and (conn["total_intensity"] / conn["hits"]) > 0.7:
        log_event(f"ALERTA: Conexão abstrata sobrecarregada: {conn_id}. Sugestão de Refatoração!", "WARNING")
        return {"status": "OVERLOAD", "suggestion": f"Criar agente mediador para {conn_id}"}
        
    return {"status": "RECORDED", "current_hits": conn["hits"]}

@cortex_function
def get_abstract_map() -> dict:
    """Retorna o mapa completo de conexões abstratas."""
    if not CONNECTIONS_FILE.exists():
        return {"connections": {}}
    return json.loads(CONNECTIONS_FILE.read_text(encoding="utf-8"))

@cortex_function
def clear_weak_connections(threshold_hits: int = 5):
    """Remove conexões com poucos hits para limpar o mapa."""
    if not CONNECTIONS_FILE.exists(): return
    data = json.loads(CONNECTIONS_FILE.read_text(encoding="utf-8"))
    
    new_conns = {k: v for k, v in data["connections"].items() if v["hits"] >= threshold_hits}
    data["connections"] = new_conns
    
    CONNECTIONS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"removed": len(data["connections"]) - len(new_conns)}
