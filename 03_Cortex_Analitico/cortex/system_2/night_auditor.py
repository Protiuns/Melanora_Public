import json
import os
import time
from pathlib import Path
from datetime import datetime

# Usaremos a integração existente com Ollama para gerar o resumo
try:
    from neural_bridge import direct_execute
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_DIR = BASE_DIR / "03_Cortex_Analitico" / "config"
PULSE_FILE = CONFIG_DIR / "user_pulse.json"
THEORETICAL_DIR = BASE_DIR / "00_Mente_Teorica" / "_Historico_Propostas"

def run_night_audit():
    """
    Script de lote: Lê a bagunça do pulse diário, deduz o significado,
    poda (pruning) o que for lixo repetitivo, e escreve um diário em markdown.
    """
    if not PULSE_FILE.exists():
        return {"status": "OK", "insight": "No pulse file found to audit."}
        
    try:
        with open(PULSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
        
    pulses = data.get("pulses", [])
    if len(pulses) == 0:
        return {"status": "OK", "insight": "No pulses to compress."}
        
    # Separar os dados valiosos do ruído (TDA/Vision vs Requests Vazios)
    valuable_pulses = []
    for p in pulses:
        route = p.get('endpoint', '')
        # Eliminar ping recorrente
        if "/api/state" in route or "/api/health" in route:
            continue
            
        valuable_pulses.append(p)
        
    if len(valuable_pulses) < 3:
        # Poda radical se for lixo
        with open(PULSE_FILE, "w", encoding="utf-8") as f:
            json.dump({"pulses": []}, f)
        return {"status": "OK", "insight": "Poda completada. Ruído irrelevante descartado."}

    # Gerar Resumo
    summary_text = "### Auditoria Sistêmica - Eventos Encontrados:\n"
    for idx, p in enumerate(valuable_pulses[-10:]): # Pega os 10 mais importantes pra não extrapolar
        stamp = datetime.fromtimestamp(p.get('timestamp', time.time())).strftime('%H:%M:%S')
        action = p.get('type') or p.get('method')
        desc = p.get('endpoint', '')
        summary_text += f"- **[{stamp}] {action}**: {desc}\n"
        
    # Aplicar a "Lei da Persistência de Relevância (L0)"
    if not THEORETICAL_DIR.exists():
        THEORETICAL_DIR.mkdir(parents=True, exist_ok=True)
        
    timestamp_filename = time.strftime("audit_%Y%m%d_%H%M%S.md")
    report_file = THEORETICAL_DIR / timestamp_filename
    
    with open(report_file, "w", encoding="utf-8") as rf:
        rf.write(f"# Auditoria Noturna: {timestamp_filename}\n")
        rf.write("> Este documento é uma cristalização gerada pelo Sistema 2 para reduzir entropia e manter a relevância histórica.\n\n")
        rf.write(summary_text)

    # Deletar os dados velhos (Memory Pruning)
    with open(PULSE_FILE, "w", encoding="utf-8") as f:
        json.dump({"pulses": []}, f)
        
    return {
        "status": "OK",
        "insight": "Poda e Sistematização concluídas com sucesso.",
        "pruned": len(pulses),
        "saved_to": str(report_file.name)
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(run_night_audit())
