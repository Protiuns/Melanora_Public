"""
🌊 Melanora Liquid Environment Manager
Centraliza a descoberta de caminhos e gestão de variáveis de ambiente.
NUNCA use caminhos absolutos; use este manager.
"""

import os
from pathlib import Path

class LiquidEnv:
    def __init__(self):
        self.root = self._find_root()
        
    def _find_root(self):
        """Descobre dinamicamente a raiz da Melanora."""
        current = Path(__file__).resolve()
        for parent in current.parents:
            # Se encontrar o arquivo mestre, esta é a raiz
            if (parent / "melanora.py").exists() or (parent / "README.md").exists():
                return parent
        # Fallback para o diretório de execução atual se não encontrar
        return Path(os.getcwd())

    @property
    def cortex(self):
        return self.root / "03_Cortex_Analitico"

    @property
    def config(self):
        return self.cortex / "config"

    @property
    def oficios(self):
        return self.root / "02_Oficios_Especialidades"

    @property
    def labs(self):
        return self.root / "04_Ambientes_Experimento"

    @property
    def python_bin(self):
        # Localiza o python portable
        return self.root / "01_Ambientes_Ferramentas" / "Python" / "bin" / "python.exe"

    def resolve(self, path_str):
        """Converte uma string de caminho relativo ou fixo antigo em um Path líquido."""
        # Se for um caminho absoluto antigo do Newton, limpa e torna relativo à raiz
        if "Newton" in path_str:
            parts = Path(path_str).parts
            if "Melanora" in parts:
                idx = parts.index("Melanora")
                relative = Path(*parts[idx+1:])
                return self.root / relative
        
        return self.root / path_str

# Singleton Instance
ENV = LiquidEnv()

if __name__ == "__main__":
    print(f"[ENV] Root detectado: {ENV.root}")
    print(f"[ENV] Python Bin: {ENV.python_bin}")
    print(f"[ENV] Cortex: {ENV.cortex}")
