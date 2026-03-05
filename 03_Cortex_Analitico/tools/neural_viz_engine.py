"""
🎨 Melanora Neural Visualization Engine (v1.0)
Gera diagramas de arquitetura (Mermaid) e resumos visuais.
Os resultados são salvos na Área Analítica do projeto.
"""

import json
from pathlib import Path
from datetime import datetime

# Caminhos
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/01_Ambientes_Ferramentas/Area_Analitica")

def generate_mermaid_map() -> str:
    """Gera um diagrama Mermaid baseado no Connectome e conexões abstratas."""
    # 1. Carregar Conexões Abstratas
    conn_file = CONFIG_DIR / "abstract_connections.json"
    connections = {}
    if conn_file.exists():
        try:
            connections = json.loads(conn_file.read_text(encoding="utf-8")).get("connections", {})
        except: pass

    # 2. Construir o Diagrama
    lines = ["graph TD", "    subgraph Córtex_Criativo", "        LLM[Criativo (LLM)]", "    end", "    subgraph Córtex_Analítico", "        Local[Analítico (Python)]", "    end"]
    
    # Adicionar conexões mapeadas
    for cid, info in connections.items():
        source = info["source"]
        target = info["target"]
        hits = info["hits"]
        # Estilizar baseado em hits (conexão forte)
        if hits > 50:
            lines.append(f"    {source} == \"{hits} pulses\" ==> {target}")
        else:
            lines.append(f"    {source} -- \"{hits}\" --> {target}")
            
    return "\n".join(lines)

def export_architecture_snapshot():
    """Exporta um arquivo Markdown com o diagrama e métricas atuais."""
    if not OUTPUT_DIR.exists(): OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = OUTPUT_DIR / f"snapshot_arquitetura_{timestamp}.md"
    
    mermaid = generate_mermaid_map()
    
    # Carregar métricas se existirem
    metrics = {}
    metrics_file = CONFIG_DIR / "neural_metrics.json"
    if metrics_file.exists():
        metrics = json.loads(metrics_file.read_text(encoding="utf-8")).get("stats", {})

    content = f"""# 🧠 Snapshot de Arquitetura - {datetime.now().strftime('%d/%m/%Y %H:%M')}

## 🗺️ Mapa de Conexões (Mermaid)
```mermaid
{mermaid}
```

## 📊 Métricas da Mente Física
- **Pulsos Totais**: {metrics.get('total_pulses', 0)}
- **Latência Média**: {metrics.get('avg_latency_ms', 0):.2f} ms
- **Taxa de Erro**: {metrics.get('error_rate', 0)*100:.1f}%

---
*Gerado automaticamente pelo Neural Viz Engine v1.0*
"""
    filename.write_text(content, encoding="utf-8")
    return str(filename)

if __name__ == "__main__":
    path = export_architecture_snapshot()
    print(f"✅ Snapshot exportado: {path}")
