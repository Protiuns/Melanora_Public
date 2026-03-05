import json
import os
import ast
import math
import numpy as np
from pathlib import Path
from datetime import datetime

# Neural Bridge imports (assuming they are available in the path)
# Analytical Executor Level 3
try:
    from cortex.utils.cortex_utils import cortex_function
    from cortex.logic.dynamic_math_engine import DynamicComplexityEngine, ProximityReinforcer
except ImportError:
    def cortex_function(f): return f
    # Fallback to avoid crashes if imports fail
    class DynamicComplexityEngine:
        @staticmethod
        def get_logic_string(n): return f"lambda x: x + {n}"
        @staticmethod
        def get_complexity_level(n): return "LINEAR"
        @staticmethod
        def run_prediction(c, d): return sum(d)/len(d) if d else 0
    class ProximityReinforcer:
        def apply(self, a, n, c): return {}

BASE_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora")
REGISTRY_FILE = BASE_DIR / "03_Cortex_Analitico/config/neural_tools_registry.json"

def _load_registry():
    if not REGISTRY_FILE.exists():
        return {"tools": []}
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_registry(data):
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def is_logic_safe(logic_str):
    """🛡️ Analisador AST para garantir que código dinâmico não seja malicioso."""
    try:
        tree = ast.parse(logic_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr.startswith('_'):
                return False
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                return False
        return True
    except:
        return False

class NeuralTool:
    def __init__(self, id, name, axiom_hooks):
        self.id = id
        self.name = name
        self.axiom_hooks = axiom_hooks

    def scan(self, inputs):
        raise NotImplementedError

class RelationalSymmetryTool(NeuralTool):
    def __init__(self):
        super().__init__("nt_relational_symmetry", "Relational Symmetry", ["Topologia Toroidal", "Harmonia"])
    
    def scan(self, inputs):
        correlations = []
        for i, input_a in enumerate(inputs):
            for input_b in inputs[i+1:]:
                tags_a = set(input_a.get('tags', []))
                tags_b = set(input_b.get('tags', []))
                common = tags_a.intersection(tags_b)
                if common:
                    score = len(common) / max(len(tags_a), len(tags_b), 1)
                    correlations.append({
                        "id_a": input_a.get('id'),
                        "id_b": input_b.get('id'),
                        "shared_tags": list(common),
                        "symmetry_score": score
                    })
        return correlations

class DynamicPredictiveTool(NeuralTool):
    def __init__(self):
        super().__init__("nt_dynamic_prediction", "Dynamic Prediction", ["Energia Distribuída", "Metacognição Permanente"])
        self.reinforcer = ProximityReinforcer()
        
    def scan(self, inputs):
        results = []
        for inp in inputs:
            active_id = inp.get("id")
            data_vector = inp.get("metrics", {}).get("history", [0.1, 0.2, 0.15])
            val = data_vector[-1] if data_vector else 0.0
            
            logic_str = inp.get("dynamic_logic_ready")
            if logic_str:
                try:
                    # Garantir que temos math e numpy no env (importados globalmente)
                    safe_env = {"math": math, "np": np}
                    func = eval(logic_str, {"__builtins__": None}, safe_env)
                    prediction = func(val)
                except Exception as e:
                    # Se falhar, use o fallback clássico do motor
                    from cortex.logic.dynamic_math_engine import DynamicComplexityEngine
                    n_conns = len(inp.get("tags", []))
                    complexity = DynamicComplexityEngine.get_complexity_level(n_conns)
                    prediction = DynamicComplexityEngine.run_prediction(complexity, data_vector)
            else:
                n_conns = len(inp.get("tags", []))
                complexity = DynamicComplexityEngine.get_complexity_level(n_conns)
                prediction = DynamicComplexityEngine.run_prediction(complexity, data_vector)
            
            updates = self.reinforcer.apply(active_id, inp.get("neighbors", []), {})
            results.append({
                "target_id": active_id,
                "predicted_value": round(float(prediction), 4),
                "reinforcement_updates": updates
            })
        return results

class TopologicalManifoldTool(NeuralTool):
    """Analisa a 'forma' geométrica do contexto e sugere conectividade (Fase 26)."""
    def __init__(self):
        super().__init__("nt_topological_manifold", "Topological Manifold", ["Topologia", "Estrutura"])

    def scan(self, inputs):
        # Mapeia a densidade de tags para sugerir se o caminho deve ser 'Curto' ou 'Longo'
        results = []
        for inp in inputs:
            tags = inp.get("tags", [])
            density = len(tags) / 10.0 # Heurística simples
            results.append({
                "id": inp.get("id"),
                "structural_density": density,
                "suggested_path": "DIRECT" if density < 0.3 else "COMPLEX"
            })
        return results

class DimensionalScalerTool(NeuralTool):
    """Ajusta a profundidade do processamento (1D a N-D) (Fase 26)."""
    def __init__(self):
        super().__init__("nt_dimensional_scaler", "Dimensional Scaler", ["Abstração", "Escala"])

    def scan(self, inputs):
        results = []
        for inp in inputs:
            load = inp.get("load", 0)
            # Se a carga é alta, reduz dimensão para economizar
            dimension = "1D" if load > 80 else "3D" if load > 40 else "N-D"
            results.append({
                "id": inp.get("id"),
                "recommended_dimension": dimension,
                "abstraction_level": 1 if dimension == "1D" else 3 if dimension == "3D" else 10
            })
        return results

class TemporalFlowTool(NeuralTool):
    """Gerencia o tempo e a entropia dos pulsos sinápticos (Fase 26)."""
    def __init__(self):
        super().__init__("nt_temporal_flow", "Temporal Flow", ["Tempo", "Ritmo"])

    def scan(self, inputs):
        # Mede a latência ou 'drift' para sugerir pausas (GABA) ou aceleração
        results = []
        for inp in inputs:
            drift = inp.get("drift", 0.1)
            results.append({
                "id": inp.get("id"),
                "tempo_adjustment": "STABILIZE" if drift > 0.5 else "FLOW",
                "entropy_injection": round(drift * 0.2, 3)
            })
        return results

class NumericalCounterTool(NeuralTool):
    """Estatística de sucesso e ajuste de budgets (Fase 26)."""
    def __init__(self):
        super().__init__("nt_numerical_counter", "Numerical Counter", ["Contagem", "Estatística"])

    def scan(self, inputs):
        results = []
        for inp in inputs:
            history = inp.get("success_history", [1, 1, 0])
            success_rate = sum(history) / len(history) if history else 0.5
            results.append({
                "id": inp.get("id"),
                "success_rate": success_rate,
                "suggested_pulses": 1 if success_rate > 0.8 else 3 if success_rate < 0.4 else 2
            })
        return results

@cortex_function
def manage_neural_tool(action="list", tool_id=None, config=None):
    registry = _load_registry()
    if action == "list": return registry
    if action == "create":
        registry["tools"].append(config)
        _save_registry(registry)
        return {"status": "CREATED", "id": config["id"]}
    if action == "update":
        for i, tool in enumerate(registry["tools"]):
            if tool["id"] == tool_id:
                registry["tools"][i].update(config)
                _save_registry(registry)
                return {"status": "UPDATED", "id": tool_id}
    if action == "delete":
        registry["tools"] = [t for t in registry["tools"] if t["id"] != tool_id]
        _save_registry(registry)
        return {"status": "DELETED", "id": tool_id}
    return {"error": "Ação inválida."}

@cortex_function
def run_neural_tool_scan(tool_id="nt_relational_symmetry", sample_data=None):
    registry = _load_registry()
    tool_config = next((t for t in registry["tools"] if t["id"] == tool_id), None)
    if not tool_config: return {"error": f"Tool ID '{tool_id}' not found."}
    
    tool_map = {
        "RelationalSymmetryTool": RelationalSymmetryTool, 
        "DynamicPredictiveTool": DynamicPredictiveTool,
        "TopologicalManifoldTool": TopologicalManifoldTool,
        "DimensionalScalerTool": DimensionalScalerTool,
        "TemporalFlowTool": TemporalFlowTool,
        "NumericalCounterTool": NumericalCounterTool
    }
    class_name = tool_config.get("class", "RelationalSymmetryTool")
    tool = tool_map.get(class_name, RelationalSymmetryTool)()
    
    # Injeção para ferramentas dinâmicas
    if class_name == "DynamicPredictiveTool" and sample_data:
        for item in sample_data:
            n = len(item.get("tags", []))
            logic = DynamicComplexityEngine.get_logic_string(n)
            # Sanitização AST obrigatória
            if is_logic_safe(logic):
                item["dynamic_logic_ready"] = logic
                print(f"DEBUG: Manager - Injected logic for {item.get('id')}: {logic}")
            else:
                print(f"⚠️ Lógica insegura detectada para N={n}")

    if not sample_data:
        sample_data = [{"id": "NODE_MOCK", "tags": ["spiral"], "metrics": {"history": [0.1, 0.2]}}]
        
    results_list = tool.scan(sample_data)
    for res in results_list:
        res["timestamp"] = datetime.now().isoformat()
        res["axiom_resonanse"] = tool_config["axiom_hooks"]
        
    return {"status": "SUCCESS", "tool": tool_config["name"], "results": results_list}

if __name__ == "__main__":
    print(run_neural_tool_scan("nt_relational_symmetry"))
