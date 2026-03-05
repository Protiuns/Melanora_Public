import os
import re
import json
from datetime import datetime
from pathlib import Path

# Determinar a raiz do projeto (2 níveis acima de scripts/)
BASE_PATH = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_PATH / "03_Cortex_Analitico" / "config"
PREFERENCES_FILE = BASE_PATH / "03_Cortex_Analitico" / "memoria_vetorial" / "user_preferences.json"

def scan_progress_artifacts():
    """Analisa artefatos em busca de padroes de sucesso e falha."""
    preferences = {
        "positive": [
            "Genero Masculino (Mandatorio)",
            "Estrutura de Roteiro (McKee/Story)",
            "Brutalismo AAA (Simetria e Axialidade)",
            "Diplomacia Carnegie (Respeito e Foco no Diretor)"
        ],
        "negative": [
            "Lentidao em respostas de reflexo",
            "Complexidade desnecessaria em tarefas simples"
        ],
        "last_sync": str(datetime.now())
    }
    
    print("[AFL] Iniciando varredura de artefatos...")
    # Futuramente: Implementar busca real em .gemini/antigravity/artifacts/
    
    return preferences

def update_neural_database(prefs):
    """Salva as preferencias para que os agentes possam ler via System Prompt."""
    PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PREFERENCES_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=4, ensure_ascii=False)
    print(f"[AFL] Base de preferencias atualizada em: {PREFERENCES_FILE.name}")

if __name__ == "__main__":
    findings = scan_progress_artifacts()
    update_neural_database(findings)
    print("[AFL] Ciclo de aprendizado passivo concluido com sucesso.")
