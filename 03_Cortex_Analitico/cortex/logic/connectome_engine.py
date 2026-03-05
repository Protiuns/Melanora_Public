"""
🧬 Melanora Connectome Engine v1.0
Constroi o grafo semântico do projeto mapeando Agentes e Ambientes.
"""

import os
import json
import re
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent

def extract_metadata(file_path):
    """Extrai tags e descrição de um arquivo markdown."""
    tags = []
    cluster = "general"
    try:
        content = file_path.read_text(encoding="utf-8")
        # Procura por - **tags:** `tag1, tag2`
        tag_match = re.search(r"\*\*tags:\*\* `([^`]+)`", content)
        if tag_match:
            tags = [t.strip() for t in tag_match.group(1).split(',')]
            
        # Procura por - **cluster:** `cluster_name`
        cluster_match = re.search(r"\*\*cluster:\*\* `([^`]+)`", content)
        if cluster_match:
            cluster = cluster_match.group(1).strip()
            
    except Exception:
        pass
    return tags, cluster

def build_connectome():
    """Escaneia o projeto e constrói o JSON do Connectome com métricas TDA."""
    nodes = []
    links = []
    
    # 1. Mapear Ambientes (Contextual)
    env_path = PROJECT_ROOT / "01_Ambientes_Ferramentas"
    if env_path.exists():
        for item in env_path.iterdir():
            if item.is_dir() and not item.name.startswith(('.', '_')):
                def_file = item / "definition.md"
                tags_file = item / "neural_tags.md"
                
                tags, cluster_tag = [], "contextual"
                if def_file.exists(): tags, _ = extract_metadata(def_file)
                if not tags and tags_file.exists(): tags, _ = extract_metadata(tags_file)
                
                nodes.append({
                    "id": item.name,
                    "label": item.name.replace('_', ' '),
                    "group": "environment",
                    "area": "CONTEXTUAL",
                    "tags": tags,
                    "path": str(item)
                })

                # 1.1 Mapear PIDs (Objetos Percebidos) neste ambiente
                pid_path = item / "neural_registry" / "objects"
                if pid_path.exists():
                    for pid_file in pid_path.glob("*.json"):
                        try:
                            with open(pid_file, "r", encoding="utf-8") as f:
                                pid_data = json.load(f)
                            nodes.append({
                                "id": pid_data.get("id", pid_file.stem),
                                "label": pid_data.get("type", "PID"),
                                "group": "pid",
                                "area": "CONTEXTUAL",
                                "tags": pid_data.get("characteristics", {}).get("primary_colors", []) + ["perceived"],
                                "path": str(pid_file)
                            })
                        except: pass

    # 2. Mapear Agentes (Analytical/Strategic)
    agent_path = PROJECT_ROOT / "02_Oficios_Especialidades"
    if agent_path.exists():
        for item in agent_path.iterdir():
            if item.is_dir() and not item.name.startswith(('.', '_')):
                def_file = item / "definition.md"
                tags, _ = extract_metadata(def_file) if def_file.exists() else ([], "analytical")
                
                nodes.append({
                    "id": item.name,
                    "label": item.name.replace('_', ' '),
                    "group": "agent",
                    "area": "ANALYTICAL",
                    "tags": tags,
                    "path": str(item)
                })

    # 3. Gerar Links por Tags em comum
    links_count = {}
    for i, node_a in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            node_b = nodes[j]
            common_tags = set(node_a["tags"] or []) & set(node_b["tags"] or [])
            if common_tags:
                links.append({
                    "source": node_a["id"],
                    "target": node_b["id"],
                    "value": len(common_tags) * 0.5,
                    "tags": list(common_tags)
                })
                # Contabilizar para centralidade
                links_count[node_a["id"]] = links_count.get(node_a["id"], 0) + 1
                links_count[node_b["id"]] = links_count.get(node_b["id"], 0) + 1
                
    # 4. Cálculo de Métricas TDA Nativas
    max_links = max(links_count.values()) if links_count else 1
    for node in nodes:
        # Centralidade de Grau (Normalizada)
        node["centrality"] = round(links_count.get(node["id"], 0) / max_links, 2)
        
        # Detecção de Cluster (Simplificada por tag majoritária)
        if node["tags"]:
            node["cluster_id"] = hash(node["tags"][0]) % 12 # 12 cores possíveis no HUD
        else:
            node["cluster_id"] = 0

    # 5. Cálculo de Phi (Φ) - Densidade de Integração
    n = len(nodes)
    l = len(links)
    phi = round((2 * l) / (n * (n - 1)), 3) if n > 1 else 0

    return {
        "nodes": nodes,
        "links": links,
        "summary": {
            "environments": len([n for n in nodes if n["group"] == "environment"]),
            "agents": len([n for n in nodes if n["group"] == "agent"]),
            "pids": len([n for n in nodes if n["group"] == "pid"]),
            "total_links": len(links),
            "phi": phi,
            "timestamp": time.ctime()
        }
    }

if __name__ == "__main__":
    graph = build_connectome()
    output_path = BASE_DIR / "config" / "connectome_graph.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"Connectome Graph gerado em {output_path} (Phi: {graph['summary']['phi']})")
