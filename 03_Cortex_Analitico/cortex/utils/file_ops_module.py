"""
📂 Melanora File Ops Module (v1.0)
Operações rápidas de leitura e indexação para o Córtex Analítico.
"""

import os
import re
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function

@cortex_function
def fast_search_tags(directory: str, pattern: str) -> dict:
    """Busca rápida por tags em arquivos markdown."""
    base_path = Path(directory)
    results = {}
    
    if not base_path.exists():
        return {"error": f"Path {directory} not found"}

    prog = re.compile(pattern)
    
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding="utf-8")
                    matches = prog.findall(content)
                    if matches:
                        results[str(file_path.relative_to(base_path))] = list(set(matches))
                except Exception:
                    continue
                    
    return {
        "count": len(results),
        "matches": results
    }

@cortex_function
def get_recent_logs(log_path: str, lines: int = 50) -> list[str]:
    """Lê as últimas N linhas de um log."""
    path = Path(log_path)
    if not path.exists(): return []
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.readlines()
            return content[-lines:]
    except Exception:
        return []
