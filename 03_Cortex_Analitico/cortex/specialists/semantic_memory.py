"""
🧠 Melanora Semantic Memory (v1.0)
Motor de Memória Semântica Local e Indexação de Conceitos.
Utiliza indexação vetorial simplificada (TF-IDF/Keyword Mapping) para recuperação contextual.
"""

import os
import json
import time
import math
import re
from pathlib import Path
from collections import Counter

try:
    from cortex.utils.cortex_utils import cortex_function
except ImportError:
    def cortex_function(func):
        func._cortex_function = True
        return func

class SemanticMemory:
    def __init__(self, storage_path=None):
        base_dir = Path(__file__).parent.parent.parent
        self.storage_path = Path(storage_path) if storage_path else base_dir / "memoria_vetorial" / "semantic_index.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.index = self._load_index()

    def _load_index(self):
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "documents" in data:
                        return data
            except:
                pass
        return {"documents": [], "vocabulary": {}}

    def _save_index(self):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def _tokenize(self, text):
        # Limpeza e tokenização aprimorada
        text = text.lower()
        # Remove URLs e caminhos de arquivo para evitar ruído
        text = re.sub(r'http\S+|file://\S+', '', text)
        # Tokenização: palavras com 3+ caracteres, ignorando números isolados
        tokens = re.findall(r'\b[a-z]{3,}\b', text)
        
        # Stopwords expandidas
        stopwords = {
            'que', 'para', 'uma', 'com', 'dos', 'das', 'pelo', 'pela', 'num', 'numa',
            'the', 'and', 'for', 'this', 'that', 'with', 'from', 'have', 'been'
        }
        return [t for t in tokens if t not in stopwords]

    @cortex_function
    def add_document(self, text, metadata=None):
        """Indexa um novo documento na memória semântica."""
        tokens = self._tokenize(text)
        if not tokens: return None
        
        doc_id = len(self.index["documents"])
        doc_entry = {
            "id": doc_id,
            "text": text[:1000] + "..." if len(text) > 1000 else text, # Preview maior
            "full_path": metadata.get("path") if metadata else None,
            "tokens": tokens,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        self.index["documents"].append(doc_entry)
        self._save_index()
        return doc_id

    @cortex_function
    def search(self, query, top_k=5):
        """Busca documentos relevantes baseada em sobreposição semântica."""
        query_tokens = set(self._tokenize(query))
        if not query_tokens: return []
        
        results = []
        for doc in self.index["documents"]:
            doc_tokens = Counter(doc["tokens"])
            score = 0
            # BM25-like scoring simplificado (relevância por raridade de termo não implementada ainda, usando frequência bruta)
            for q_token in query_tokens:
                if q_token in doc_tokens:
                    score += doc_tokens[q_token]
            
            if score > 0:
                # Normalizar pelo tamanho do documento (evitar viés para docs longos)
                norm_score = score / math.log(len(doc["tokens"]) + 1)
                results.append({
                    "id": doc["id"],
                    "path": doc.get("full_path"),
                    "text": doc["text"],
                    "metadata": doc["metadata"],
                    "score": round(norm_score, 2)
                })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    @cortex_function
    def query_context(self, query, top_k=3):
        """Retorna um bloco de texto consolidado para contextualização da LLM."""
        hits = self.search(query, top_k=top_k)
        if not hits:
            return "Nenhuma memória relevante encontrada."
        
        context_blocks = []
        for hit in hits:
            block = f"--- ORIGEM: {hit['path']} (Score: {hit['score']}) ---\n{hit['text']}\n"
            context_blocks.append(block)
        
        return "\n".join(context_blocks)

    @cortex_function
    def index_workspace(self, base_dir=None, targets=None):
        """Varre o workspace em busca de documentos importantes, filtrando por Tags Neurais."""
        if not base_dir:
            base_dir = Path(__file__).parent.parent.parent.parent
        else:
            base_dir = Path(base_dir)
            
        patterns = ["*.md", "*.txt", "definition.md", "manifest.md"]
        count = 0
        
        # Load active neural tags for contextual filtering
        active_tags = ["engineering", "science", "gamedev"]
        state_path = base_dir / "03_Cortex_Analitico" / "config" / "neural_state.json"
        if state_path.exists():
            try:
                with open(state_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    active_tags = state.get("active_tags", active_tags)
            except Exception: pass
            
        # Define the taxonomy mapping
        tag_map = {
            "gamedev": ["Godot_Nexus_2", "Studio_Nexus"],
            "engineering": ["03_Cortex_Analitico", "Python", "Node", "Melanora_App"],
            "science": ["Central_Pesquisa", "00_Mente_Teorica", "Atelie_Artigos"]
        }
        
        if not targets:
            targets = [
                "00_Mente_Teorica",
                "01_Ambientes_Ferramentas",
                "02_Oficios_Especialidades",
                "03_Cortex_Analitico",
                "05_Evolucao_Sintonizacao"
            ]

        for target in targets:
            target_path = base_dir / target
            if not target_path.exists(): continue
            
            for pattern in patterns:
                try:
                    for file_path in target_path.rglob(pattern):
                        path_str = str(file_path)
                        
                        # Apply Neural Tags filter
                        skip_due_to_tags = False
                        for tag, folders in tag_map.items():
                            if tag not in active_tags:
                                if any(folder in path_str for folder in folders):
                                    skip_due_to_tags = True
                                    break
                                    
                        if skip_due_to_tags:
                            continue

                        if any(b in path_str.lower() for b in [".git", "__pycache__", "node_modules", "logs", "temp", "archive"]):
                            continue
                        
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                            
                            self.add_document(content, metadata={
                                "path": str(file_path.relative_to(base_dir)),
                                "type": file_path.suffix[1:]
                            })
                            count += 1
                        except:
                            pass
                except:
                    pass
        
        return {"indexed_files": count}

def get_semantic_engine():
    return SemanticMemory()

if __name__ == "__main__":
    memory = SemanticMemory()
    print("🧠 Memória Semântica Pronta.")

