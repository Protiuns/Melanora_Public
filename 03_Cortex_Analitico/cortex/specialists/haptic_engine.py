"""
📉 Melanora Haptic Engine (v1.0)
Analisador de Entropia e Complexidade Arquitetônica.
Transforma métricas de código em "sensações" digitais.
"""

import os
import ast
import time
from pathlib import Path

class HapticEngine:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.connectome_stats = {}

    def analyze_complexity(self, file_path):
        """Calcula métricas de complexidade para um arquivo Python."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Métricas Básicas
            lines = content.splitlines()
            num_lines = len(lines)
            
            # Complexidade Arquitetônica (AST)
            depths = []
            num_functions = 0
            num_classes = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    num_functions += 1
                elif isinstance(node, ast.ClassDef):
                    num_classes += 1
            
            # Entropia de Código (Simplificada: Indentação média como proxy de complexidade)
            indentations = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
            avg_indent = sum(indentations) / len(indentations) if indentations else 0
            
            return {
                "lines": num_lines,
                "functions": num_functions,
                "classes": num_classes,
                "avg_indent": round(avg_indent, 2),
                "entropy": round(avg_indent * (num_functions + 1) / (num_lines + 1), 3)
            }
        except Exception as e:
            return {"error": str(e)}

    def scan_connectome(self):
        """Varre o projeto em busca de arquivos de código e calcula o 'calor'."""
        total_entropy = 0
        file_count = 0
        hottest_files = []

        # Focar em áreas críticas: cortex, logic, especialistas
        search_paths = [
            self.target_dir / "03_Cortex_Analitico" / "cortex",
            self.target_dir / "03_Cortex_Analitico" / "dashboard_api.py"
        ]

        for path in search_paths:
            if path.is_file():
                files = [path]
            elif path.is_dir():
                files = list(path.rglob("*.py"))
            else:
                continue

            for f in files:
                if "__pycache__" in str(f) or "setup.py" in str(f):
                    continue
                
                metrics = self.analyze_complexity(f)
                if "error" not in metrics:
                    total_entropy += metrics["entropy"]
                    file_count += 1
                    hottest_files.append({
                        "name": f.name,
                        "path": str(f.relative_to(self.target_dir)),
                        "entropy": metrics["entropy"]
                    })

        # Ordenar por mais "quentes" (complexos)
        hottest_files.sort(key=lambda x: x["entropy"], reverse=True)

        avg_health = 1.0 - (total_entropy / (file_count + 1))
        
        return {
            "timestamp": time.time(),
            "overall_health": max(0, min(1, round(avg_health, 2))),
            "total_entropy": round(total_entropy, 2),
            "file_count": file_count,
            "hottest_files": hottest_files[:5], # Top 5 áreas complexas
            "status": "STABLE" if avg_health > 0.7 else "DENSE" if avg_health > 0.4 else "CRITICAL"
        }

def get_haptic_state():
    """Função de entrada para a API."""
    base_path = Path(__file__).parent.parent.parent.parent
    engine = HapticEngine(base_path)
    return engine.scan_connectome()

if __name__ == "__main__":
    print("🔍 Testando Haptic Engine...")
    state = get_haptic_state()
    import json
    print(json.dumps(state, indent=2))
