"""
💾 Melanora Episodic Memory (v17.0 - Physiology)
Sistema de registro de experiências marcantes (Snapshots de Consciência).
Permite que o sistema aprenda com picos de stress ou estados de flow.
"""

import json
import time
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional

class EpisodicMemory:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.memory_file = self.base_dir / "logs" / "episodic_memory_fractal.json"
        # Estrutura: List de nós raiz. Cada nó tem "children" []
        self.episodes = self._load_memory()
        self.last_save = time.time()

    def _load_memory(self) -> List[Dict]:
        if self.memory_file.exists():
            try:
                return json.loads(self.memory_file.read_text(encoding="utf-8"))
            except:
                return []
        return []

    def save_episode(self, state_vector: List[float], metadata: Dict[str, Any], importance: float = 1.0):
        """
        Grava um snapshot usando estrutura fractal.
        Se muito importante (> 0.8), vira um nó raiz.
        Se similar a um nó existente, vira um filho (sub-ramo).
        """
        episode = {
            "id": f"ep_{int(time.time() * 1000)}",
            "timestamp": time.ctime(),
            "unixtime": time.time(),
            "vector": state_vector,
            "metadata": metadata,
            "importance": round(importance, 2),
            "children": []
        }
        
        # Lógica Fractal: Encontrar "Pai" por similaridade
        parent_found = False
        if importance < 0.8 and self.episodes:
            # Busca o nó raiz mais similar
            similar_roots = self.recall_similar(state_vector, top_n=1)
            if similar_roots:
                parent = similar_roots[0]
                # Se for minimamente similar (distância < 0.5)
                cur_v = np.array(state_vector)
                parent_v = np.array(parent["vector"])
                if np.linalg.norm(cur_v - parent_v) < 0.5:
                    parent.setdefault("children", []).append(episode)
                    parent_found = True

        if not parent_found:
            self.episodes.append(episode)
        
        # Limite de raízes (Manter o tronco principal limpo)
        if len(self.episodes) > 500:
            self.episodes.sort(key=lambda x: x["importance"], reverse=True)
            self.episodes = self.episodes[:500]

        # Salvar fisicamente a cada 5 minutos ou se for muito importante
        if time.time() - self.last_save > 300 or importance > 0.9:
            self.persist()

    def persist(self):
        try:
            self.memory_file.write_text(json.dumps(self.episodes, indent=2), encoding="utf-8")
            self.last_save = time.time()
        except Exception as e:
            print(f"❌ [MEMORY] Erro ao persistir episódios fractais: {e}")

    def recall_similar(self, current_vector: List[float], top_n: int = 3) -> List[Dict]:
        """Busca episódios passados (raízes) com similaridade vetorial."""
        if not self.episodes:
            return []
            
        cur = np.array(current_vector)
        matches = []
        
        # Busca recursiva simples (nível 1 apenas para performance)
        for ep in self.episodes:
            vec = np.array(ep["vector"])
            dist = np.linalg.norm(cur - vec)
            matches.append((dist, ep))
            
        matches.sort(key=lambda x: x[0])
        return [m[1] for m in matches[:top_n]]

    def get_stress_experience(self) -> float:
        """Retorna uma média do cortisol consolidado na memória (últimas raízes)."""
        if not self.episodes:
            return 0.2
        
        # Vetor[1] é Cortisol normalizado
        cortisols = [e["vector"][1] for e in self.episodes[-20:]]
        return sum(cortisols) / len(cortisols)

# Instância Global
episodic_memory = EpisodicMemory()

# Instância Global
episodic_memory = EpisodicMemory()
