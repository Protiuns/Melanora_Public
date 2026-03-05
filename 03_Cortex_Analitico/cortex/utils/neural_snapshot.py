"""
Neural Snapshot Protocol (v1.0)
Captura o estado numerico completo do cerebro de Melanora em um dado instante.
Serve como "fotografia neural" para auto-analise e propriocepcao sintetica.
"""

import json
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"

# Fontes de estado
STATE_FILE = CONFIG_DIR / "neural_state.json"
SECTION_FILE = CONFIG_DIR / "section_policy.json"
WATCHDOG_FILE = CONFIG_DIR / "watchdog.json"
METRICS_FILE = CONFIG_DIR / "learning_metrics.json"
AUDIT_FILE = CONFIG_DIR / "neural_audit.json"
EXPECTATION_FILE = CONFIG_DIR / "expectation_model.json"
SYNAPSES_DIR = CONFIG_DIR / "synapses"
SNAPSHOTS_FILE = CONFIG_DIR / "neural_snapshots_log.json"


def _safe_read(path: Path) -> dict:
    """Le um JSON sem crashar se o arquivo nao existir."""
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def capture_snapshot(context: str = "", document_type: str = "unknown") -> Dict[str, Any]:
    """
    Captura uma fotografia completa do estado neural.
    
    Args:
        context: Descricao humana do que esta sendo gerado (ex: "Estudo Autonomo #24")
        document_type: Tipo de documento (research, memory, instruction, journal, code)
    
    Returns:
        Dict com todos os indicadores numericos do cerebro.
    """
    now = datetime.now()
    
    # 1. Estado Central
    state = _safe_read(STATE_FILE)
    
    # 2. Secoes (Gating Limbico)
    sections = _safe_read(SECTION_FILE)
    section_map = {}
    for name, data in sections.items():
        status = data.get("status", "UNKNOWN")
        section_map[name] = 1.0 if status in ("ACTIVE", "ALWAYS_ON") else 0.0
    
    # 3. Watchdog (Saude dos Componentes)
    watchdog = _safe_read(WATCHDOG_FILE)
    alive_count = sum(1 for v in watchdog.values() if isinstance(v, dict) and v.get("status") == "ALIVE")
    total_watched = max(len(watchdog), 1)
    
    # 4. Modelo de Expectativa (Surpresa Acumulada)
    expectations = _safe_read(EXPECTATION_FILE)
    avg_surprise = 0.0
    avg_success = 1.0
    total_samples = 0
    if expectations:
        success_rates = [v.get("success_rate", 1.0) for v in expectations.values()]
        samples = [v.get("samples", 0) for v in expectations.values()]
        avg_success = sum(success_rates) / len(success_rates) if success_rates else 1.0
        total_samples = sum(samples)
    
    # 5. Sinapses Ativas (Nodos Descentralizados)
    synapse_count = 0
    total_charge = 0.0
    if SYNAPSES_DIR.exists():
        for f in SYNAPSES_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                synapse_count += 1
                total_charge += data.get("potential", 0.0)
            except Exception:
                pass
    avg_charge = total_charge / max(synapse_count, 1)
    
    # 6. Metricas de Aprendizado
    metrics = _safe_read(METRICS_FILE)
    best_score = metrics.get("best_score", 0)
    total_matches = metrics.get("total_matches", 0)
    
    # 7. Auditoria Neural
    audit = _safe_read(AUDIT_FILE)
    audit_score = audit.get("score", 0)
    
    # === MONTAR SNAPSHOT ===
    snapshot = {
        "id": hashlib.md5(f"{now.isoformat()}{context}".encode()).hexdigest()[:12],
        "timestamp": now.isoformat(),
        "context": context,
        "document_type": document_type,
        
        # Indicadores Numericos
        "brain_state": {
            "mode": state.get("mode", "UNKNOWN"),
            "phase": state.get("fase", "UNKNOWN"),
            "cycle": state.get("ciclo_atual", 0),
            "neural_load": state.get("neural_load", 0),
            "active_impulses": state.get("active_impulses_count", 0)
        },
        
        "sections": {
            "vital": section_map.get("VITAL", 1.0),
            "cognitive": section_map.get("COGNITIVE", 0.0),
            "adaptive": section_map.get("ADAPTIVE", 0.0),
            "integration_index": sum(section_map.values()) / max(len(section_map), 1)
        },
        
        "health": {
            "alive_components": alive_count,
            "total_watched": total_watched,
            "vitality_ratio": round(alive_count / total_watched, 2),
            "audit_score": audit_score
        },
        
        "prediction": {
            "avg_success_rate": round(avg_success, 3),
            "total_learned_patterns": total_samples,
            "known_functions": len(expectations)
        },
        
        "synaptic": {
            "active_nodes": synapse_count,
            "avg_charge": round(avg_charge, 2),
            "total_charge": round(total_charge, 2)
        },
        
        "learning": {
            "best_score": best_score,
            "total_experiences": total_matches
        },
        
        # Indice Composto: "Como eu estava?"
        "coherence_index": round(
            (section_map.get("VITAL", 1.0) * 0.3) +
            (avg_success * 0.25) +
            ((alive_count / total_watched) * 0.2) +
            ((audit_score / 100.0) * 0.15) +
            (min(avg_charge / 100.0, 1.0) * 0.1),
            3
        )
    }
    
    # Persistir no log de snapshots
    _save_to_log(snapshot)
    
    return snapshot


def _save_to_log(snapshot: dict):
    """Salva o snapshot no historico persistente."""
    try:
        log = {"snapshots": []}
        if SNAPSHOTS_FILE.exists():
            log = json.loads(SNAPSHOTS_FILE.read_text(encoding="utf-8"))
        
        log["snapshots"].append(snapshot)
        # Manter ultimos 200 snapshots
        log["snapshots"] = log["snapshots"][-200:]
        
        SNAPSHOTS_FILE.write_text(json.dumps(log, indent=2), encoding="utf-8")
    except Exception:
        pass


def format_snapshot_header(snapshot: dict) -> str:
    """
    Gera o bloco YAML-like para embutir em qualquer documento Markdown.
    """
    s = snapshot
    brain = s.get("brain_state", {})
    sections = s.get("sections", {})
    health = s.get("health", {})
    pred = s.get("prediction", {})
    syn = s.get("synaptic", {})
    
    header = f"""---
neural_snapshot: "{s['id']}"
timestamp: "{s['timestamp']}"
context: "{s['context']}"
coherence_index: {s['coherence_index']}
brain_mode: "{brain.get('mode', '?')}"
brain_phase: "{brain.get('phase', '?')}"
cycle: {brain.get('cycle', 0)}
neural_load: {brain.get('neural_load', 0)}
sections:
  vital: {sections.get('vital', 0)}
  cognitive: {sections.get('cognitive', 0)}
  adaptive: {sections.get('adaptive', 0)}
  integration: {sections.get('integration_index', 0)}
health:
  vitality: {health.get('vitality_ratio', 0)}
  audit_score: {health.get('audit_score', 0)}
prediction:
  success_rate: {pred.get('avg_success_rate', 0)}
  known_patterns: {pred.get('total_learned_patterns', 0)}
synaptic:
  active_nodes: {syn.get('active_nodes', 0)}
  avg_charge: {syn.get('avg_charge', 0)}
---"""
    return header


if __name__ == "__main__":
    snap = capture_snapshot(context="Teste de auto-analise", document_type="test")
    print(format_snapshot_header(snap))
    print(f"\nCoerencia Neural: {snap['coherence_index']}")
