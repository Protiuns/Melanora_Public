"""
💎 Melanora Neural Prism (v1.0)
Camada de abstração para a arquitetura de camadas flexíveis.
Centraliza as políticas de varredura, ignorância e afinidade semântica.
Newton: Este é o 'filtro' que impede a superlotação e garante a fluidez operacional.
"""

import os
from pathlib import Path

# Definição Global de Ignorância (Bio-Filtro)
# Impede que pastas massivas de dependências entrem no processamento neural.
GLOBAL_IGNORE = {
    "node_modules", ".git", "__pycache__", "venv", ".venv", 
    "bin", "obj", "dist", "build", "_backups", ".godot"
}

# Políticas de Camada (Layer Policies)
# Define como cada camada deve ser 'percebida'.
LAYER_POLICIES = {
    "00_Mente_Teorica": {"scan": "shallow", "depth": 2},
    "01_Ambientes_Ferramentas": {"scan": "specific", "active_subfolders": ["Central_Pesquisa", "Area_Analitica", "Infra_Neural"]},
    "02_Oficios_Especialidades": {"scan": "deep", "depth": 3},
    "03_Cortex_Analitico": {"scan": "deep", "depth": 2},
    "04_Manifestacao_Projetos": {"scan": "shallow", "depth": 1}
}

class NeuralPrism:
    def __init__(self, project_root: str):
        self.root = Path(project_root)

    def get_active_scan_paths(self) -> list[Path]:
        """Retorna apenas os caminhos que devem ser varridos em busca de lógica/scripts."""
        active_paths = []
        
        # 1. Varredura dinâmica de camadas (00 a 05)
        for d in self.root.iterdir():
            if d.is_dir() and d.name[:2].isdigit():
                layer_name = d.name
                policy = LAYER_POLICIES.get(layer_name, {"scan": "shallow", "depth": 1})
                
                if policy["scan"] == "specific":
                    # Apenas subpastas ativas (Ex: evita node_modules na raiz do ambiente)
                    for sub in policy.get("active_subfolders", []):
                        sub_path = d / sub
                        if sub_path.exists():
                            active_paths.append(sub_path)
                else:
                    active_paths.append(d)
        
        return active_paths

    def should_ignore(self, path: Path) -> bool:
        """Verifica se um caminho deve ser ignorado pela rede neural."""
        parts = path.parts
        return any(p in GLOBAL_IGNORE for p in parts)

    def get_layer_of(self, path: Path) -> str:
        """Identifica a qual camada abstrata um caminho pertence."""
        try:
            rel = path.relative_to(self.root)
            return rel.parts[0] if rel.parts else "ROOT"
        except:
            return "EXTERNAL"

if __name__ == "__main__":
    prism = NeuralPrism("c:/Users/Newton/Meu Drive/1. Projetos/Melanora")
    print("Caminhos Ativos para Varredura:")
    for p in prism.get_active_scan_paths():
        print(f" - {p}")
