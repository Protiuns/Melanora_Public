"""
🛠️ Melanora Script Executor (v1.0)
Busca e executa ferramentas locais (.py, .js, .bat, .ps1) espalhadas pela rede neural.
Permite que o Córtex Analítico delegue tarefas pesadas para scripts específicos.
"""

import os
import subprocess
import json
import sys
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Camadas para busca de ferramentas (Abstraídas pelo NeuralPrism)
from neural_prism import NeuralPrism

@cortex_function
def discover_local_tools(project_root: str) -> dict:
    """Varre a rede neural em busca de scripts executáveis usando o NeuralPrism."""
    root = Path(project_root)
    prism = NeuralPrism(str(root))
    tools = {}
    
    extensions = {".py": "Python", ".js": "NodeJS", ".bat": "Batch", ".ps1": "PowerShell"}
    active_paths = prism.get_active_scan_paths()
    
    for layer_path in active_paths:
        # Usar as políticas do prisma para limitar a busca
        layer_name = prism.get_layer_of(layer_path)
        
        for root_dir, dirs, files in os.walk(layer_path):
            # 1. Aplicar Filtro Global de Ignorância
            if prism.should_ignore(Path(root_dir)):
                dirs[:] = [] # Não descer em diretórios ignorados
                continue
            
            # 2. Filtrar subpastas ineficientes
            dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in extensions:
                    tool_path = Path(root_dir) / file
                    tool_id = tool_path.stem
                    tools[tool_id] = {
                        "path": str(tool_path.absolute()),
                        "type": extensions[ext],
                        "rel_path": str(tool_path.relative_to(root)),
                        "layer": layer_name
                    }
    
    log_event(f"Descobertas {len(tools)} ferramentas locais respeitando o NeuralPrism.")
    return {
        "count": len(tools),
        "tools": tools
    }

@cortex_function
def execute_local_tool(tool_path: str, args: list = None, timeout_s: int = 60) -> dict:
    """Executa uma ferramenta local e retorna o resultado."""
    path = Path(tool_path)
    if not path.exists():
        return {"status": "ERROR", "error": f"Tool not found: {tool_path}"}
    
    ext = path.suffix.lower()
    command = []
    
    if ext == ".py":
        command = [sys.executable, str(path)]
    elif ext == ".js":
        command = ["node", str(path)]
    elif ext == ".bat":
        command = [str(path)]
    elif ext == ".ps1":
        command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(path)]
    else:
        return {"status": "ERROR", "error": f"Unsupported extension: {ext}"}
    
    if args:
        command.extend([str(a) for a in args])
        
    log_event(f"Executando ferramenta: {path.name}")
    
    try:
        start_time = subprocess.time.time()
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            encoding="utf-8",
            errors="replace"
        )
        elapsed = subprocess.time.time() - start_time
        
        return {
            "status": "OK" if result.returncode == 0 else "FAILED",
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "elapsed_ms": round(elapsed * 1000, 1)
        }
    except subprocess.TimeoutExpired:
        log_event(f"Timeout na execução de {path.name}", "WARNING")
        return {"status": "TIMEOUT", "error": f"Execution exceeded {timeout_s}s"}
    except Exception as e:
        log_event(f"Erro ao executar {path.name}: {e}", "ERROR")
        return {"status": "ERROR", "error": str(e)}

@cortex_function
def list_available_runtimes() -> dict:
    """Verifica quais runtimes estão disponíveis no sistema."""
    runtimes = {
        "python": {"cmd": sys.executable, "status": "OK"},
        "node": {"cmd": "node --version", "status": "UNKNOWN"},
        "powershell": {"cmd": "powershell --version", "status": "UNKNOWN"}
    }
    
    for r in ["node", "powershell"]:
        try:
            subprocess.run([r.split()[0], "--version" if r == "node" else "-Command $PSVersionTable.PSVersion"], 
                           capture_output=True, timeout=2)
            runtimes[r]["status"] = "OK"
        except:
            runtimes[r]["status"] = "NOT_FOUND"
            
    return runtimes
