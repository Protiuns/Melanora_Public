"""
🌱 Melanora Plasticity Engine (v1.0)
Monitora a criação de novas regiões neurais (diretórios) e ferramentas.
Permite que o Córtex Analítico se adapte nativamente à evolução da rede.
"""

import os
import time
import json
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Camadas para monitoramento (Abstraído pelo NeuralPrism)
from neural_prism import NeuralPrism

@cortex_function
def scan_for_new_regions(project_root: str, known_regions: list = None) -> dict:
    """Detecta novas pastas na rede neural usando o NeuralPrism."""
    root = Path(project_root)
    prism = NeuralPrism(str(root))
    found = []
    known = set(known_regions or [])
    
    active_paths = prism.get_active_scan_paths()
    
    for layer_path in active_paths:
        if not layer_path.exists(): continue
        layer_name = prism.get_layer_of(layer_path)
        
        for d in layer_path.iterdir():
            if d.is_dir() and not d.name.startswith((".", "_")):
                # Ignorar se o prisma mandar ignorar
                if prism.should_ignore(d):
                    continue
                    
                rel_path = str(d.relative_to(root))
                if rel_path not in known:
                    found.append({
                        "name": d.name,
                        "path": rel_path,
                        "layer": layer_name,
                        "created_at": time.ctime(os.path.getctime(d))
                    })
    
    if found:
        log_event(f"Detectadas {len(found)} novas regiões neurais!")
    
    return {
        "new_count": len(found),
        "new_regions": found
    }

@cortex_function
def check_for_orphan_scripts(project_root: str) -> list:
    """Busca scripts (.py, .js) que não estão em pastas 'oficiais' de agentes."""
    root = Path(project_root)
    orphans = []
    
    # Busca scripts na raiz das camadas
    for layer in LAYERS:
        layer_path = root / layer
        if not layer_path.exists(): continue
        
        for f in layer_path.glob("*"):
            if f.is_file() and f.suffix in [".py", ".js", ".bat"]:
                orphans.append(str(f.relative_to(root)))
                
    return orphans

if __name__ == "__main__":
    # Teste local
    print(scan_for_new_regions("c:/Users/Newton/Meu Drive/1. Projetos/Melanora"))
