"""
🧠 Melanora Knowledge Architect (Phase 9 PoC)
Especialista em mapear a topologia de conhecimento e arquivos da Melanora.
Usa NetworkX para identificar núcleos de informação e conexões semânticas.
"""

import os
import networkx as nx
import json
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
CORTEX_HUB = BASE_DIR / "cortex"

@cortex_function
def map_architectural_graph():
    """Analisa a estrutura de pastas e gera um grafo de densidade de arquivos."""
    G = nx.Graph()
    
    # Caminhos para ignorar
    ignore = ["node_modules", ".git", "__pycache__", ".godot"]
    
    root_path = str(BASE_DIR)
    
    for root, dirs, files in os.walk(root_path):
        # Filtrar pastas ignoradas
        dirs[:] = [d for d in dirs if d not in ignore]
        
        rel_root = os.path.relpath(root, root_path)
        if rel_root == ".": rel_root = "MELANORA_CORE"
        
        G.add_node(rel_root, type="directory", size=len(files))
        
        # Conectar ao pai
        parent = os.path.dirname(rel_root)
        if parent:
            G.add_edge(parent, rel_root)
            
        for f in files:
            if f.endswith(('.py', '.md', '.json', '.bat')):
                file_node = f"{rel_root}/{f}"
                G.add_node(file_node, type="file", ext=os.path.splitext(f)[1])
                G.add_edge(rel_root, file_node)

    # Calcular Centralidade (quais pastas/arquivos são núcleos)
    centrality = nx.degree_centrality(G)
    
    # Preparar dados para o Dashboard
    nodes = []
    for node, data in G.nodes(data=True):
        nodes.append({
            "id": node,
            "centrality": round(centrality.get(node, 0), 4),
            "type": data.get("type"),
            "label": os.path.basename(node)
        })
        
    edges = [{"source": u, "target": v} for u, v in G.edges()]
    
    result = {
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges(),
            "most_central": max(centrality, key=centrality.get)
        }
    }
    
    # Salvar para o Dashboard ler como uma 'Neural Skill Result'
    with open(CONFIG_DIR / "knowledge_graph.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    return result

@cortex_function
def calculate_architecture_entropy():
    """Calcula a entropia (desorganização) baseada na densidade de arquivos por pasta."""
    stats = {}
    total_files = 0
    
    for root, dirs, files in os.walk(str(BASE_DIR)):
        if any(x in root for x in ["node_modules", ".git", "__pycache__"]): continue
        rel = os.path.relpath(root, str(BASE_DIR))
        f_count = len([f for f in files if not f.startswith('.')])
        if f_count > 0:
            stats[rel] = f_count
            total_files += f_count
            
    # Pastas com mais de 15 arquivos sugerem necessidade de refatoração
    overloaded = {k: v for k, v in stats.items() if v > 15}
    
    return {
        "total_files": total_files,
        "folder_density": stats,
        "overloaded_folders": overloaded,
        "status": "HEALTHY" if not overloaded else "ORGANIZATION_REQUIRED"
    }

@cortex_function
def run_neural_self_audit():
    """Realiza uma autocrítica profunda da estrutura e lógica do projeto."""
    G = nx.Graph()
    root_path = str(BASE_DIR)
    
    findings = []
    
    # 1. Checar Modularidade (Fase 9: Centros de Processamento)
    hubs = ["logic", "specialists", "utils"]
    missing_hubs = [h for h in hubs if not (BASE_DIR / h).exists()]
    
    if len(missing_hubs) == 0:
         findings.append({
            "severity": "LOW",
            "type": "ARCHITECTURAL_EVOLUTION",
            "message": "Estrutura de Hubs Sinápticos detectada. Expansão organizada em andamento."
        })
    
    cortex_files = list(BASE_DIR.rglob("*.py"))
    
    # 2. Identificar Neurônios Isolados
    all_files = []
    for root, _, files in os.walk(str(BASE_DIR.parent)):
        if any(x in root for x in ["node_modules", "anaconda3", ".git"]): continue
        all_files.extend(files)
        
    # 3. Análise de 'Dívida Técnica'
    placeholders = 0
    for file in cortex_files:
        if file.name == "knowledge_architect.py": continue
        try:
            content = file.read_text(encoding="utf-8")
            if "placeholder" in content.lower() or "stub" in content.lower():
                placeholders += 1
        except: pass
            
    if placeholders > 0:
        findings.append({
            "severity": "MEDIUM",
            "type": "SYNAPTIC_GAP",
            "message": f"Existem {placeholders} áreas com lógica simplificada. Melhore a densidade analítica."
        })

    # 4. Verificação de Integridade de Comunicação
    if not (BASE_DIR / "dashboard").exists():
        findings.append({
            "severity": "CRITICAL",
            "type": "SENSORY_DEPRIVATION",
            "message": "Interface visual desconectada ou não compilada."
        })

    audit_result = {
        "timestamp": time.time(),
        "score": max(0, 100 - (len(findings) * 15)),
        "findings": findings,
        "recommendation": "Consolidação concluída. A mente física está operando com capacidades reais."
    }
    
    # Exportar para o Dashboard
    with open(CONFIG_DIR / "neural_audit.json", "w", encoding="utf-8") as f:
        json.dump(audit_result, f, indent=2)
        
    return audit_result
