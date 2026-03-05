import json
import math
from pathlib import Path

# Configurações de diretório
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_DIR = BASE_DIR / "03_Cortex_Analitico" / "config"
CONNECTOME_FILE = CONFIG_DIR / "connectome_graph.json"

def perform_topological_analysis():
    """Lê o conectoma e aplica Leis Proporcionais (L0) gerando insight analítico."""
    if not CONNECTOME_FILE.exists():
        return {"status": "ERROR", "message": "Connectome offline."}

    try:
        with open(CONNECTOME_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

    nodes = data.get("nodes", [])
    links = data.get("links", [])

    num_nodes = len(nodes)
    num_links = len(links)

    if num_nodes == 0:
        return {"status": "OK", "metrics": {}, "insight": "Sistema vazio. Nenhuma matriz para calcular."}

    # 1. Contar links por nó
    link_counts = {node["id"]: 0 for node in nodes}
    for link in links:
        source = link.get("source")
        target = link.get("target")
        if isinstance(source, dict): source = source.get("id")
        if isinstance(target, dict): target = target.get("id")
        
        if source in link_counts: link_counts[source] += 1
        if target in link_counts: link_counts[target] += 1

    # 2. Nós Isolados (0 links)
    isolated_nodes = [node_id for node_id, count in link_counts.items() if count == 0]

    # 3. Densidade Sináptica
    # max possible links in undirected graph: n(n-1)/2
    max_possible_links = (num_nodes * (num_nodes - 1)) / 2 if num_nodes > 1 else 1
    density = num_links / max_possible_links

    # 4. Avaliação Axiomática (Integração L0)
    phi_status = "ESTÁVEL"
    density_str = f"{density:.4f}"
    
    insight_msg = "Análise Topológica concluída com base na Lei das Proporções (L0). "
    if len(isolated_nodes) > 0:
        insight_msg += f"ALERTA: Detectamos {len(isolated_nodes)} arquivos isolados (buracos semânticos) no projeto. Recomendo integrá-los para evitar perda de conhecimento (Ex: {isolated_nodes[0]}). "
        phi_status = "FRAGMENTADO (Atenção)"
    elif density < 0.05:
        insight_msg += "A rede está funcional, mas muito esparsa. Alta dependência linear."
        phi_status = "ESPARSO"
    else:
        insight_msg += "Conectividade robusta. Densidade sináptica saudável."
        phi_status = "INTEGRADO (Saudável)"

    # Formatar o retorno
    return {
        "status": "OK",
        "metrics": {
            "total_nodes": num_nodes,
            "total_links": num_links,
            "isolated_count": len(isolated_nodes),
            "density": density_str,
            "phi_status": phi_status,
            "isolated_examples": isolated_nodes[:3]
        },
        "insight": insight_msg
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(perform_topological_analysis())
