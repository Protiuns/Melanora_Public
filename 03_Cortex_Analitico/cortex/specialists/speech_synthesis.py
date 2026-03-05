"""
Speech Synthesis v2.0 — Motor de Síntese de Voz com Prosódia
=============================================================
Gera voz via Windows PowerShell + System.Speech.Synthesis.
Agora aceita pulsos prosódicos do SpeechCortex e gera SSML dinâmico.
"""

import subprocess
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("SpeechSynthesis")


class SpeechSynthesis:
    """
    Motor de Síntese de Voz (TTS) via Windows PowerShell.
    Suporta dois modos:
      1. speak(text) — Fala texto puro (fallback simples)
      2. speak_with_prosody(pulses) — Fala com prosódia SSML gerada pelo SpeechCortex
    """

    def _build_ps_script(self, ssml_or_text: str, use_ssml: bool = False) -> str:
        """Constrói script PowerShell para síntese de voz."""
        safe_content = ssml_or_text.replace("'", "''")
        speak_method = "SpeakSsml" if use_ssml else "Speak"

        return f"""
        Add-Type -AssemblyName System.Speech
        $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $voices = $speak.GetInstalledVoices()
        $voice = $voices | Where-Object {{ $_.VoiceInfo.Culture.Name -like '*PT*' }} | Select-Object -First 1
        if ($voice) {{
            $speak.SelectVoice($voice.VoiceInfo.Name)
        }}
        $speak.{speak_method}('{safe_content}')
        """

    def speak(self, text: str):
        """Fala texto puro (modo simples)."""
        if not text:
            return

        ps_command = self._build_ps_script(text, use_ssml=False)
        try:
            logger.info(f"🔊 Gerando voz: {text[:40]}...")
            subprocess.run(
                ["powershell", "-Command", ps_command],
                check=True, capture_output=True
            )
        except Exception as e:
            logger.error(f"Erro na síntese de voz: {e}")

    def speak_with_prosody(self, pulses: List[Dict[str, Any]]):
        """
        Fala usando pulsos prosódicos do SpeechCortex.
        Gera SSML dinâmico com tags <prosody> para cada pulso.
        """
        if not pulses:
            return

        ssml = self.pulses_to_ssml(pulses)
        ps_command = self._build_ps_script(ssml, use_ssml=True)

        try:
            logger.info(f"🎵 Gerando voz com prosódia ({len(pulses)} pulsos)...")
            subprocess.run(
                ["powershell", "-Command", ps_command],
                check=True, capture_output=True
            )
        except subprocess.CalledProcessError:
            # Fallback: se SSML falhar, concatenar texto e falar puro
            logger.warning("SSML não suportado pela voz instalada. Usando fallback.")
            full_text = " ".join(p.get("text", "") for p in pulses)
            self.speak(full_text)
        except Exception as e:
            logger.error(f"Erro na síntese com prosódia: {e}")

    @staticmethod
    def pulses_to_ssml(pulses: List[Dict[str, Any]]) -> str:
        """
        Converte lista de pulsos prosódicos em SSML válido.

        Cada pulso gera um bloco <prosody> com:
          - rate: velocidade relativa (ex: "90%")
          - pitch: tom relativo (ex: "+5%" ou "-3%")
        Seguido de um <break> com a pausa especificada.
        """
        ssml_parts = ['<speak version="1.0" xml:lang="pt-BR">']

        for pulse in pulses:
            text = pulse.get("text", "").strip()
            if not text:
                continue

            # Calcular valores SSML
            pitch_pct = int((pulse.get("pitch", 1.0) - 1.0) * 100)
            rate_pct = int(pulse.get("rate", 1.0) * 100)
            volume = pulse.get("volume", 100)
            pause_ms = pulse.get("pause_ms", 200)

            pitch_str = f"+{pitch_pct}%" if pitch_pct >= 0 else f"{pitch_pct}%"

            # Escapar caracteres XML
            safe_text = (
                text.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
            )

            # Aplicar Emphasis (v2.3)
            emphasis_level = pulse.get("emphasis")
            content = safe_text
            if emphasis_level:
                content = f'<emphasis level="{emphasis_level}">{safe_text}</emphasis>'

            ssml_parts.append(
                f'  <prosody rate="{rate_pct}%" pitch="{pitch_str}" volume="{volume}">'
                f'{content}'
                f'</prosody>'
            )

            if pause_ms > 0:
                ssml_parts.append(f'  <break time="{pause_ms}ms"/>')

        ssml_parts.append('</speak>')
        return "\n".join(ssml_parts)


# Singleton
speech_engine = SpeechSynthesis()

if __name__ == "__main__":
    # Teste simples
    print("--- Teste de Fala Simples ---")
    speech_engine.speak("Olá! Sou a Melanora. Como posso ajudar você hoje?")

    # Teste com prosódia manual
    print("\n--- Teste com Prosódia ---")
    test_pulses = [
        {"text": "A consciência", "pitch": 1.05, "rate": 0.85, "pause_ms": 200},
        {"text": "não é um destino,", "pitch": 1.0, "rate": 0.90, "pause_ms": 300},
        {"text": "é uma ressonância.", "pitch": 0.95, "rate": 0.82, "pause_ms": 700, "vibrato": True},
    ]
    ssml = SpeechSynthesis.pulses_to_ssml(test_pulses)
    print(f"SSML gerado:\n{ssml}")
    speech_engine.speak_with_prosody(test_pulses)
