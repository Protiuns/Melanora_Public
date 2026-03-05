"""
Teste Simulado do Córtex Analítico focado em Matematica e Geometria.
Forjamos uma tarefa visual que aciona o Dilema, testando se a Ponte Neural
intercepta o problema e gera um "Analytical Insight" (Estatística e Regras Estritas).
"""

import sys
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from neural_bridge import direct_execute

# Uma "função vazia" de visão no Córtex só para ser injetada no teste
import cortex.heuristics.sensory_perception as sp
# Simular uma função falsa 'look_at_screen'
def look_at_screen(screen_data): return "Olhando..."
look_at_screen._cortex_function = True

# Registra a função temporária na ponte virtual
from neural_bridge import CORTEX_REGISTRY
CORTEX_REGISTRY["vision_test_module"] = {"look_at_screen": look_at_screen}

print("🧪 Iniciando Validação do Dilema Analítico...")

# Um cenário perigoso: Cobra perto do topo esquerdo. Ir para a esquerda ou cima bate na parede.
# Mas não tem maçã visível (Aciona dilema por falta de alvo heurístico).
dangerous_scene = {
    "resolution": [400, 400],
    "entities": [
        {"type": "green_mass", "bbox": [5, 5, 20, 20], "area": 400} 
    ]
}

print("1. Emulando uma Tarefa da Nuvem que pede para o módulo de 'vision' processar a tela...")
result = direct_execute(
    module="vision_test_module", 
    function="look_at_screen", 
    params={"screen_data": dangerous_scene}
)

print("\n--- RESULTADO DA PONTE NEURAL ---")
print(f"Status: {result['status']}")
print(f"Dilema Acionado? {result.get('dilemma')}")

insight = result.get("analytical_insight")
if insight:
    print("\n📊 INSIGHT ANALÍTICO LOCAL GERADO:")
    print(f"  Proporção de Massa: {insight['proportions'].get('occupied_ratio', 0) * 100:.2f}%")
    print("  Avaliação de Hard Rules (Se eu resolvesse mandar um input):")
    for act, eval_data in insight['action_evaluation'].items():
        bloqueado = not eval_data['allowed']
        print(f"    - {act}: {'❌ BLOQUEADO' if bloqueado else '✅ PERMITIDO'} (Risco Base: {eval_data['risk']})")
else:
    print("❌ Falha. Nenhum insight analítico foi anexado ao resultado da ponte.")
