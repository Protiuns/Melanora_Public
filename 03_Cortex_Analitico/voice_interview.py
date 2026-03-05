"""
🎙️ Voice Interview — Entrevista por Voz com a Melanora
=======================================================
Script standalone para conversar com a Melanora por voz em tempo real.
Usa SpeechRecognition (Google) para STT e Edge-TTS (Azure Neural) para TTS.
Conecta ao Ollama local para gerar respostas.

Uso:
    python voice_interview.py              # Modo SpeechRecognition (Google STT)
    python voice_interview.py --vosk       # Modo Vosk (STT local/offline)
    python voice_interview.py --sr         # Forçar SpeechRecognition (mesmo se Vosk disponível)
"""

import sys
import time
import signal
import logging
import os
from pathlib import Path

# Activating ANSI colors for Windows Console
if os.name == 'nt':
    os.system('color')

# Logging limpo no terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("VoiceInterview")


# Cores ANSI
C_CYAN = '\033[96m'
C_MAGENTA = '\033[95m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_RESET = '\033[0m'
C_DIM = '\033[2m'

def print_banner():
    """Mostra banner de boas-vindas."""
    print(f"\n{C_CYAN}" + "━" * 60 + f"{C_RESET}")
    print(f"  🎙️  {C_MAGENTA}Melanora Voice Interview{C_RESET} v1.1")
    print(f"  {C_DIM}Neuro-semantic Voice Bridge{C_RESET}")
    print(f"{C_CYAN}" + "━" * 60 + f"{C_RESET}")


def check_ollama():
    """Verifica se o Ollama está rodando."""
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        if r.status_code == 200:
            models = [m['name'] for m in r.json().get('models', [])]
            print(f"  ✅ Ollama ativo — Modelos: {', '.join(models)}")
            return True
    except:
        pass
    print("  ❌ Ollama não detectado! Inicie o Ollama antes da entrevista.")
    print("     Comando: ollama serve")
    return False


def check_microphone():
    """Verifica acesso ao microfone."""
    try:
        import speech_recognition as sr
        mics = sr.Microphone.list_microphone_names()
        if mics:
            print(f"  ✅ Microfone detectado: {mics[0]}")
            return True
    except:
        pass
    print("  ❌ Nenhum microfone detectado!")
    return False


def check_tts():
    """Verifica TTS (Edge-TTS)."""
    try:
        import edge_tts
        print("  ✅ TTS Neural (Edge-TTS) disponível.")
        return True
    except Exception as e:
        print(f"  ❌ TTS indisponível: {e}")
        return False


def run_interview(use_vosk=False, force_sr=False):
    """Loop principal da entrevista por voz."""
    # Limpa a tela
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_banner()
    
    # Pré-checks
    print(f"\n  {C_CYAN}📋 Inicializando arranjo sináptico...{C_RESET}\n")
    mic_ok = check_microphone()
    tts_ok = check_tts()
    ollama_ok = check_ollama()
    
    if not (mic_ok and tts_ok and ollama_ok):
        print(f"\n  {C_RED}⛔ Corrija as falhas neurais antes de conectar o córtex.{C_RESET}")
        return
    
    print(f"\n  📡 {C_DIM}Motor Sensorial: {'Vosk (offline)' if use_vosk and not force_sr else 'Google (online)'}{C_RESET}")
    print(f"\n{C_CYAN}" + "─" * 60 + f"{C_RESET}")
    print(f"  {C_YELLOW}💡 Fale de forma livre. O Córtex responderá através do som.{C_RESET}")
    print(f"  {C_DIM}💡 Pressione Ctrl+C a qualquer momento para desconectar.{C_RESET}")
    print(f"{C_CYAN}" + "─" * 60 + f"{C_RESET}\n")
    
    # Importar e iniciar o VoiceBridge
    try:
        from cortex.specialists.voice_bridge import VoiceBridge
        bridge = VoiceBridge(use_sr_fallback=(not use_vosk or force_sr), llm_context="VOICE_INTERVIEW")
        
        # Handler para Ctrl+C
        def signal_handler(sig, frame):
            print(f"\n\n  {C_RED}🛑 Quebrando conexão neural...{C_RESET}")
            bridge.stop()
            time.sleep(1)
            print(f"  {C_MAGENTA}👋 Fim da transmissão.{C_RESET}\n")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Iniciar a ponte
        bridge.start()
        print(f"  {C_GREEN}🟢 Sinergia estabelecida. Pode falar!{C_RESET}\n")
        # Pequeno som de sino no terminal alertando que está pronta
        print('\a', end='') 
        
        # Manter o script rodando
        while bridge.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n\n  {C_RED}🛑 Quebrando conexão neural...{C_RESET}")
        bridge.stop()
        time.sleep(0.5)
        print(f"  {C_MAGENTA}👋 Fim da transmissão.{C_RESET}\n")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    use_vosk = "--vosk" in sys.argv
    force_sr = "--sr" in sys.argv
    run_interview(use_vosk=use_vosk, force_sr=force_sr)
