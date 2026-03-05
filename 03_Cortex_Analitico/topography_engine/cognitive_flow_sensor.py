"""
📡 Melanora Topography Engine: Cognitive Flow Sensor (v0.1)
Protótipo inicial para medir a 'elevação' da carga cognitiva através da telemetria de edição.
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

# Caminhos
BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "03_Cortex_Analitico" / "config"
TOPOGRAPHY_STATE = BASE_DIR / "03_Cortex_Analitico" / "topography_engine" / "flow_state.json"

def calculate_edit_density(directory: Path, interval_hours: int = 24):
    """Calcula a densidade de edições recentes para estimar carga cognitiva."""
    now = time.time()
    cutoff = now - (interval_hours * 3600)
    
    edits = 0
    impact_score = 0
    affected_files = []
    
    # Ignorar pastas ruidosas
    ignore_dirs = {".git", "node_modules", "venv", "__pycache__", ".ollama", "bin"}
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            path = Path(root) / file
            try:
                mtime = path.stat().st_mtime
                if mtime > cutoff:
                    edits += 1
                    # Ponderação por tamanho/tipo (ex: .md é teoria, .js/py é técnica)
                    weight = 1.0
                    if path.suffix in ('.js', '.py', '.gd'): weight = 1.5
                    impact_score += weight
                    affected_files.append(str(path.relative_to(directory)))
            except: pass
            
    return {
        "timestamp": datetime.now().isoformat(),
        "interval_h": interval_hours,
        "edit_count": edits,
        "impact_score": round(impact_score, 2),
        "hot_spots": affected_files[:5], # Principais arquivos
        "topographic_status": "HIGH_ALTITUDE" if impact_score > 20 else "LOWLANDS"
    }

def update_topography():
    """Atualiza o estado persistente da topografia."""
    print("📡 Aferindo Topografia Humana...")
    report = calculate_edit_density(BASE_DIR)
    
    TOPOGRAPHY_STATE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOPOGRAPHY_STATE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"✅ Estado Topográfico: {report['topographic_status']} ({report['impact_score']})")

if __name__ == "__main__":
    update_topography()
