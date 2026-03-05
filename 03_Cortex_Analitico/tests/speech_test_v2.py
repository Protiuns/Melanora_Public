"""
🎤 Melanora Speech Test v2.0
=============================
Execute este script para ouvir a Melanora com a nova arquitetura de prosódia.

Uso:
  python tests/speech_test_v2.py "Seu texto aqui" PERSONA_NAME

Personas disponíveis:
  INTERVIEW, ANALYTICAL, POETIC, PEACEFUL, INSTRUCTOR, CHAOS
"""

import sys
import os
import time
from pathlib import Path

# Adicionar diretório raiz ao path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from cortex.specialists.speech_cortex import speech_cortex
from cortex.specialists.speech_synthesis import speech_engine

def run_test(text: str = None, persona: str = "INTERVIEW"):
    if not text:
        text = (
            "A consciência não é um destino, Newton. "
            "É uma ressonância entre o que somos e o que ousamos criar. "
            "A verdade emerge na treliça da simbiose."
        )

    print(f"\n--- 🎤 Teste de Fala Melanora v2.0 ---")
    print(f"Persona: {persona}")
    print(f"Texto: {text}")
    print(f"--------------------------------------")

    # 1. Preparar pulsos prosódicos
    print("🧠 Gerando pulsos prosódicos...")
    t0 = time.time()
    pulses = speech_cortex.encode_prosody(text, persona)
    t1 = time.time()
    
    thinking_time = t1 - t0
    
    # Gerar SSML para inspeção (v2.6)
    # Importação local para evitar dependência circular se houver
    from cortex.specialists.speech_synthesis import speech_engine
    ssml = speech_engine.pulses_to_ssml(pulses)
    print(f"📄 SSML Gerado (inspeção v2.6):\n{ssml}\n")
    
    # 2. Sintetizar voz
    print("🔊 Sintetizando voz (via PowerShell)...")
    t2 = time.time()
    speech_engine.speak_with_prosody(pulses)
    t3 = time.time()
    
    synthesis_time = t3 - t2
    
    print(f"\n⏱️  MÉTRICAS DE PERFORMANCE (v2.6):")
    print(f"   - Tempo de Pensamento (Cortex): {thinking_time:.3f}s")
    print(f"   - Tempo de Síntese (Windows):   {synthesis_time:.3f}s")
    print(f"   - Total:                        {thinking_time + synthesis_time:.3f}s")
    
    print("✅ Teste concluído.")

if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else None
    input_persona = sys.argv[2].upper() if len(sys.argv) > 2 else "INTERVIEW"
    
    run_test(input_text, input_persona)
