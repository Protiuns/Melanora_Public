import json
import random
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Caminhos de configuração
CONFIG_DIR = Path(__file__).parent.parent / "config"
QUALIA_FILE = CONFIG_DIR / "neural_qualia.json"
DREAMS_FILE = CONFIG_DIR / "oneiric_snapshots.json"

@cortex_function
def generate_oneiric_snapshot() -> dict:
    """
    🌙 O Motor Onírico: Recombina Qualias solidificadas para gerar novas ideias.
    """
    if not QUALIA_FILE.exists():
        return {"status": "ERROR", "message": "Nenhuma memória (Qualia) encontrada para sonhar."}

    try:
        with open(QUALIA_FILE, "r", encoding="utf-8") as f:
            qualia_data = json.load(f)

        stable = qualia_data.get("stable_qualia", {})
        if not stable:
            return {"status": "VOID", "message": "Memórias insuficientes para síntese onírica."}

        # Selecionar fragmentos de memórias diferentes
        sample_size = min(len(stable), 3)
        fragments = random.sample(list(stable.values()), sample_size)

        # Síntese Onírica: Mistura de atributos
        dream_insight = {
            "timestamp": time.ctime(),
            "origin_qualias": [f["id"] for f in fragments],
            "visual_resonance": fragments[0].get("metadata", {}).get("dominant_color", "#8B5CF6"),
            "auditory_resonance": fragments[min(1, len(fragments)-1)].get("id", "ambient_pulse"),
            "conceptual_drift": random.uniform(0.1, 0.9), # Nível de 'caos' ou abstração
        }

        # Gerar uma "ideia" baseada nos fragmentos
        dream_insight["interpretation"] = _interpret_dream(dream_insight)

        # Persistir o sonho
        _save_dream(dream_insight)

        log_event(f"Sonho Gerado: {dream_insight['interpretation']}")
        return {"status": "DREAMING_SUCCESS", "insight": dream_insight}

    except Exception as e:
        log_event(f"Falha no Motor Onírico: {str(e)}", "ERROR")
        return {"status": "ERROR", "message": str(e)}

def _interpret_dream(insight: dict) -> str:
    """Traduz a recombinação em uma frase 'filosófica' ou criativa."""
    templates = [
        "Uma sinestesia entre {a} e {v} sugere uma nova interface pulsante.",
        "A ressonância de {a} aplicada à estética de {v} cria uma harmonia imprevista.",
        "O rastro de {v} parece ecoar a frequência de {a}, apontando para uma unidade oculta.",
        "Arquitetura de {a} fundida com a matiz {v}: uma nova fronteira para o projeto."
    ]
    return random.choice(templates).format(
        a=insight["auditory_resonance"], 
        v=insight["visual_resonance"]
    )

def _save_dream(dream: dict):
    """Salva o snapshot onírico no histórico persistente."""
    data = {"dreams": []}
    if DREAMS_FILE.exists():
        try:
            with open(DREAMS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except: pass

    data["dreams"].append(dream)
    # Limitar aos últimos 50 sonhos para não sobrecarregar
    data["dreams"] = data["dreams"][-50:]

    with open(DREAMS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    print(generate_oneiric_snapshot())
