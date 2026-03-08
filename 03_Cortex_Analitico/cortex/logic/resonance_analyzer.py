"""
⚖️ Melanora Resonance Analyzer (v1.0)
Calcula a harmonia entre uma tarefa concluída, o estado hormonal e os Axiomas Fundamentais.
Onde a ressonância é alta, a "Confiança" (0-1) se torna "Convicção" (Sentimento de Verdade).
"""

import re
import json
import time
from pathlib import Path
from dataclasses import dataclass

class ResonanceAnalyzer:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.axioms_file = self.base_dir.parent / "00_Mente_Teorica" / "01_Essencia_Visionaria" / "axiomas_fundamentais.md"
        self.axioms = self._load_axioms()

    def _load_axioms(self):
        """Carrega e extrai palavras-chave dos axiomas para análise de ressonância."""
        if not self.axioms_file.exists():
            return []
        
        content = self.axioms_file.read_text(encoding="utf-8")
        # Extrair títulos de axiomas (## II. Título)
        matches = re.findall(r"##\s+[IVX]+\.\s+(.+)", content)
        return [m.strip() for m in matches]

    def calculate_resonance(self, task_result, hormones):
        """
        Mede a harmonia estética e lógica.
        Retorna um valor de 0 a 1.
        """
        score = 0.5 # Base neutra
        
        # 1. Ressonância de Resultado (Sucesso aumenta harmonia)
        if task_result.get("status") == "OK":
            score += 0.1
        else:
            score -= 0.2

        # 2. Ressonância Hormonal (Dopamina Alta + Cortisol Baixo = Harmonia Estética)
        d = hormones.get("dopamine", 0.5)
        c = hormones.get("cortisol", 0.2)
        
        hormonal_harmony = (d * (1.1 - c))
        score += (hormonal_harmony - 0.5) * 0.4

        # 3. Ressonância Axiomática (Simulação de alinhamento com a Identidade)
        # Se a tarefa envolveu módulos de "Córtex", a ressonância é naturalmente maior
        module = task_result.get("module", "")
        if "cortex" in module.lower() or "neural" in module.lower():
            score += 0.1

        return max(0.0, min(1.0, score))

    def evaluate_conviction(self, confidence, resonance):
        """
        Transforma a confiança técnica e a ressonância em Convicção Qualia.
        """
        # A convicção é o produto da certeza técnica com o "sentimento" de harmonia
        return (confidence * 0.6) + (resonance * 0.4)

if __name__ == "__main__":
    analyzer = ResonanceAnalyzer()
    print(f"Axiomas detectados: {analyzer.axioms}")
    res = analyzer.calculate_resonance({"status": "OK", "module": "neural_bridge"}, {"dopamine": 0.8, "cortisol": 0.1})
    print(f"Ressonância Calculada: {res:.2f}")
    print(f"Convicção Qualia: {analyzer.evaluate_conviction(0.9, res):.2f}")
