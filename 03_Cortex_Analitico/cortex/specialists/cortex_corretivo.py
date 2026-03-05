import os
import json
import time
from pathlib import Path

# Tentamos importar os módulos de comunicação com a LLM para gerar os sumários semantic
try:
    from cortex.specialists.neural_inference import ask_ollama
except ImportError:
    # Fallback se ask_ollama não existir diretamente lá
    def ask_ollama(prompt, model="llama3", system="Você é o Córtex Corretivo."):
        import requests
        try:
            res = requests.post("http://localhost:11434/api/generate", json={
                "model": model, "prompt": prompt, "system": system, "stream": False
            }, timeout=30)
            return res.json().get("response", "[Simulação de Sumário Gerado]")
        except:
            return "[Motor de Inferência Offline: Sumário Auto-Gerado por Heurística Padrão]"

# Usar decorator se existir
try:
    from cortex.utils.cortex_utils import cortex_function
except ImportError:
    def cortex_function(f): return f


def load_knowledge_graph():
    """Carrega o grafo neural principal."""
    graph_path = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico/config/knowledge_graph.json")
    if not graph_path.exists():
        return {"nodes": [], "edges": []}
    with open(graph_path, "r", encoding="utf-8") as f:
        return json.load(f)

def identify_isolated_nodes(graph_data):
    """Retorna os IDs de todos os nós que possuem 0 arestas apontando ou saindo deles."""
    nodes = {n.get("id") for n in graph_data.get("nodes", []) if n.get("id")}
    connected = set()
    for e in graph_data.get("edges", []):
        connected.add(e.get("source"))
        connected.add(e.get("target"))
    
    isolated = list(nodes - connected)
    return isolated

def analyze_directory_contents(folder_path):
    """Extrai uma pequena amostra do que existe na pasta para a IA ler."""
    path = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora") / folder_path
    if not path.is_dir():
        return "Not a valid directory."
        
    contents = []
    # Olha apenas para a raiz imediata pra não ser muito lento
    for item in list(path.iterdir())[:15]:
        size = "DIR" if item.is_dir() else f"{item.stat().st_size} bytes"
        contents.append(f"- {item.name} ({size})")
        
    return "\n".join(contents)

@cortex_function
def scan_semantic_holes():
    """
    🧹 CÓRTEX CORRETIVO: Varre a base do Connectome em busca de arquivos isolados.
    Se encontrar uma pasta morta, lê o conteúdo e gera um '_semantic_index.md' usando LLM
    para que o Indexador principal crie as ligações neurais no futuro.
    """
    print("🔎 [Córtex Corretivo] Iniciando escaneamento de Buracos Semânticos...")
    graph = load_knowledge_graph()
    isolated_nodes = identify_isolated_nodes(graph)
    
    if not isolated_nodes:
        print("✅ Nenhum buraco semântico detectado. A mente está coesa.")
        return {"status": "OK", "holes_fixed": 0}
        
    print(f"⚠️ {len(isolated_nodes)} nós isolados detectados no projeto. Iniciando integração...")
    
    nodes_processed = 0
    base_dir = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora")
    
    for i, node_id in enumerate(isolated_nodes):
        # Vamos tratar principalmente pastas órfãs identificadas pelo connectome_engine
        # que geralmente tem ID relativo, se for "logs", então resolve_path é base / "logs"
        fixed_path = base_dir / node_id

        if fixed_path.is_dir():
            index_file = fixed_path / "_semantic_index.md"
            if not index_file.exists():
                print(f"  🧠 Reconectando módulo isolado: {node_id}")
                dir_structure = analyze_directory_contents(node_id)
                
                prompt = (
                    f"A pasta '{node_id}' acabou de ser escanneada na Melanora e não tem conexões semânticas.\n"
                    f"Aqui está uma lista do que tem dentro dela:\n{dir_structure}\n\n"
                    f"Escreva um arquivo markdown EXTREMAMENTE CURTO (máximo 4 linhas) que sirva como um indexador. "
                    f"Diga que isso é um 'Arquivo gerado automaticamente pelo Córtex Corretivo para reconexão semântica'. "
                    f"Explique de forma técnica do que se trata essa pasta baseado nos seus arquivos."
                )
                
                # Gera o sumário pela IA ou Mock
                try:
                    ai_summary = ask_ollama(prompt, system="Você é a Mente Sintetizadora da Melanora. Analise a arquitetura.")
                except Exception as e:
                    ai_summary = f"[Motor Cognitivo Offline. Possível pasta de backup/arquivos]\nErro na geração: {e}"
                
                # Salva o arquivo de ponte
                with open(index_file, "w", encoding="utf-8") as out:
                    out.write(ai_summary)
                
                nodes_processed += 1
                time.sleep(1) # Breath
                
    return {
        "status": "OK",
        "holes_fixed": nodes_processed,
        "total_isolated_found": len(isolated_nodes)
    }

if __name__ == "__main__":
    res = scan_semantic_holes()
    print("Resultado:", res)
