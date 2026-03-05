"""
🔍 Melanora Topography Engine: Semantic Gap Analyzer (v0.1)
Identifica 'Buracos' (Gaps) e Arquivos Órfãos na rede de conhecimento da Melanora.
"""

import os
import re
from pathlib import Path

# Configurações
BASE_DIR = Path(__file__).parent.parent.parent
TARGET_DIRS = ["00_Mente_Teorica", "03_Cortex_Analitico"]

def find_links_in_file(file_path: Path):
    """Extrai links para outros arquivos (import em code, [link] em md)."""
    links = []
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Regex para Markdown [[link]] ou [link](path)
        md_links = re.findall(r'\[\[(.*?)\]\]|\]\((.*?)\)', content)
        for link in md_links:
            links.append(link[0] or link[1])
            
        # Regex para Python imports
        py_imports = re.findall(r'^import (.*?)$|^from (.*?) import', content, re.MULTILINE)
        for imp in py_imports:
            links.append(imp[0] or imp[1])
            
    except Exception as e:
        pass
    return links

def map_topology():
    print("🗺️ Iniciando Mapeamento Topológico...")
    
    file_map = {} # {rel_path: {"out": set(), "in": set()}}
    stem_to_path = {} # {stem: rel_path}
    all_files = []
    
    for d_name in TARGET_DIRS:
        d_path = BASE_DIR / d_name
        if not d_path.exists(): continue
        for root, _, files in os.walk(d_path):
            if "__pycache__" in root: continue
            for file in files:
                f_path = Path(root) / file
                rel_path = str(f_path.relative_to(BASE_DIR)).replace("\\", "/")
                all_files.append(rel_path)
                file_map[rel_path] = {"out": set(), "in": set()}
                stem_to_path[f_path.stem] = rel_path

    print(f"📂 {len(all_files)} arquivos mapeados. Analisando conexões...")

    # Analisar conexões
    for i, f in enumerate(all_files):
        if i % 10 == 0:
            print(f"⏳ Processando: {i}/{len(all_files)}...")
        
        links = find_links_in_file(BASE_DIR / f)
        for link in links:
            link_clean = link.replace("\\", "/").split('/')[-1].split('.')[0] # Pega apenas o 'nome' do arquivo
            
            # Busca rápida por stem
            if link_clean in stem_to_path:
                target = stem_to_path[link_clean]
                if target != f:
                    file_map[f]["out"].add(target)
                    file_map[target]["in"].add(f)

    # Identificar Buracos (Gaps)
    orphans = [f for f, data in file_map.items() if not data["in"] and f.endswith('.md')]
    undocumented = [f for f, data in file_map.items() if not data["out"] and f.endswith('.py')]
    
    print("\n\n⚠️ RELATÓRIO DE GAPS TOPOGRÁFICOS:")
    print("====================================")
    print(f"📄 Arquivos Órfãos (Sem conexões de entrada): {len(orphans)}")
    for o in orphans[:10]: print(f"  - {o}")
    
    print(f"\n💻 Código 'Mudo' (Sem links para teoria/documentação): {len(undocumented)}")
    for u in undocumented[:10]: print(f"  - {u}")

if __name__ == "__main__":
    map_topology()
