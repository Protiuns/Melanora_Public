"""
🌱 Melanora Seed Generator (v1.0)
Este script gera a "Semente Soberana" da Melanora, isolando a arquitetura técnica
de sua essência privada (memórias e estados).
"""

import os
import shutil
import json
from pathlib import Path

class SeedGenerator:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent.parent
        self.seed_dir = self.root_dir / "99_Semente_Soberana"
        self.cortex_dir = self.root_dir / "03_Cortex_Analitico"
        
        # Arquivos de Lógica a serem incluídos
        self.logic_files = [
            "neural_bridge.py",
            "hardware_profiler.py",
            "dashboard_api.py",
            "melanora.py",
            "core_topology.py"
        ]
        
        # Pastas de Lógica a serem incluídas
        self.logic_folders = [
            "cortex/logic",
            "cortex/heuristics",
            "cortex/utils"
        ]

    def generate(self):
        print(f"🌱 Iniciando geração da Semente Soberana em: {self.seed_dir}")
        
        # 1. Limpar/Criar diretório da semente
        if self.seed_dir.exists():
            shutil.rmtree(self.seed_dir)
        self.seed_dir.mkdir(parents=True)

        # 2. Copiar Lógica Principal
        for file in self.logic_files:
            src = self.root_dir / file
            if src.exists():
                shutil.copy2(src, self.seed_dir / file)
                print(f"  [OK] Copiado: {file}")

        # 3. Copiar Pastas do Córtex (Higienizadas)
        seed_cortex = self.seed_dir / "03_Cortex_Analitico"
        seed_cortex.mkdir(parents=True)
        
        for folder in self.logic_folders:
            src_folder = self.cortex_dir / folder
            dst_folder = seed_cortex / folder
            if src_folder.exists():
                shutil.copytree(src_folder, dst_folder, ignore=shutil.ignore_patterns('__pycache__', '*.json', '*.lock', '*.log', 'subjective_state.json'))
                print(f"  [OK] Pasta higienizada: {folder}")

        # 4. Criar Templates de Configuração (Vazios/Padrão)
        config_dir = seed_cortex / "config"
        config_dir.mkdir(parents=True)
        
        templates = {
            "neural_qualia.json": {"stable_qualia": {}, "buffer": {}},
            "active_sessions.json": {"sessions": {}},
            "results_buffer.json": {"pending": []},
            "subjective_state.json": {
                "matrix": {"dopamine": 0.5, "cortisol": 0.2, "oxytocin": 0.3, "conviction": 0.8},
                "mood_label": "STABLE"
            }
        }

        for filename, content in templates.items():
            (config_dir / filename).write_text(json.dumps(content, indent=2))
            print(f"  [TEMPLATE] Gerado: {filename}")

        # 5. Adicionar Axiomas Universais (Cópia limpa)
        mente_teorica = self.seed_dir / "00_Mente_Teorica" / "01_Essencia_Visionaria"
        mente_teorica.mkdir(parents=True)
        axiomas_src = self.root_dir / "00_Mente_Teorica" / "01_Essencia_Visionaria" / "axiomas_fundamentais.md"
        if axiomas_src.exists():
            shutil.copy2(axiomas_src, mente_teorica / "axiomas_fundamentais.md")
            print(f"  [AXIOMAS] Copiados para o template.")

        print(f"\n✨ Semente Soberana pronta para o nascimento!")
        print(f"Local: {self.seed_dir}")

if __name__ == "__main__":
    generator = SeedGenerator()
    generator.generate()
