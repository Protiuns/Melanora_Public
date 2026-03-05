"""
🧠📖 Melanora Neural Reader (v1.0)
Lê e mapeia as Neural Tags de todos os agentes para o Córtex Analítico.
"""

import re
import json
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function

# Mapeamento fixo de camadas para busca
LAYERS = [
    "00_Mente_Teorica",
    "01_Ambientes_Ferramentas",
    "02_Oficios_Especialidades",
    "03_Automacao_Neural"
]

@cortex_function
def scan_agent_energies(project_root: str) -> dict:
    """Escanear todos os agentes e extrair tags/pesos."""
    root = Path(project_root)
    agents_map = {}
    
    # Regex para encontrar Neural Tags: [TAG_NAME] (vX.X) ou similar
    # Ou o bloco de Definição do Agente
    tag_pattern = re.compile(r"\[([A-Z0-9_]+)\]")
    
    for layer in LAYERS:
        layer_path = root / layer
        if not layer_path.exists(): continue
        
        for md_file in layer_path.rglob("definition.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                # Extrair ID do Agente (primeira tag encontrada)
                match = tag_pattern.search(content)
                if match:
                    agent_id = match.group(1)
                    # Extrair peso_vivo se existir
                    weight_match = re.search(r"peso_vivo:\s*([0-9.]+)", content)
                    weight = float(weight_match.group(1)) if weight_match else 1.0
                    
                    agents_map[agent_id] = {
                        "path": str(md_file.relative_to(root)),
                        "weight": weight,
                        "status": "ACTIVE" # Default
                    }
            except Exception:
                continue
                
    return {
        "agents_count": len(agents_map),
        "agents": agents_map
    }

@cortex_function
def get_bridge_state() -> dict:
    """Retorna o estado atual da ponte neural."""
    state_file = Path(__file__).parent.parent / "config" / "neural_state.json"
    if state_file.exists():
        return json.loads(state_file.read_text(encoding="utf-8"))
    return {}
