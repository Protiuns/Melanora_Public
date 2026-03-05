"""
Teste Integrado: Visão OpenCV + Semântica + Córtex Motor
Abre o jogo Snake criado e tenta jogá-lo usando visão e teclado virtuais no Windows.
"""

import webbrowser
import os
import time
import sys

try:
    from cortex.perception.math_vision import MathVisionCortex
    from cortex.heuristics.local_semantic_engine import run_semantic_reflex
except ImportError as e:
    print(f"Erro de importação. Bibliotecas faltantes? {e}")
    sys.exit(1)

html_path = r"c:\Users\Newton\Meu Drive\1. Projetos\Melanora\04_Manifestacao_Projetos\Jogos_Simples\snake_lab.html"
print(f"🎮 Abrindo {html_path} no seu navegador padrão...")
webbrowser.open(f"file:///{html_path.replace('\\', '/')}")

print("⏳ Você tem 5 segundos para maximizar o navegador, clicar em PLAY (o botão verde normal) e manter o jogo em foco!")
for i in range(5, 0, -1):
    print(i)
    time.sleep(1)

# Callback que junta a percepção da tela com o reflexo e atua fisicamente
def vision_callback(scene_data):
    reflex = run_semantic_reflex(scene_data)
    if reflex.get("action") == "press_key":
        print(f"⚡ [REFLEXO MOTOR]: {reflex['key']} | Motivo: {reflex['reasoning']}")

print("\n👁️ Iniciando Córtex Visual e Motor por 20 segundos...")
# Tenta pegar a tela inteira. Para testes otimizados seria bom pegar só a bounding box do jogo, mas isso serve de laboratório.
vision = MathVisionCortex() 

try:
    vision.perceive_continuously(vision_callback, fps=15, duration_sec=20)
except Exception as e:
    print(f"Erro durante a percepção: {e}")

print("✅ Teste finalizado. O Córtex Neural entrou em repouso.")
