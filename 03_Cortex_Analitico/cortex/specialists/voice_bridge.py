"""
VoiceBridge v5.0 — Full Duplex Communication Bridge
===================================================
Orquestrador de ponte de voz em tempo real.
Gerencia entrada (Microfone), saída (Caixa de Som) e processamento neural (AEC/NS).
v5.0: TTS real via pyttsx3, paths absolutos, fallback STT com speech_recognition.
"""

import threading
import queue
import time
import logging
import json
import re
import os
import asyncio
import numpy as np
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional

from neural_bridge import log_event
from cortex.specialists.speech_cortex import speech_cortex
from cortex.specialists.dialogue_orchestrator import extract_unified_prompt

try:
    from cortex.utils.cortex_utils import cortex_function
except ImportError:
    def cortex_function(fn): return fn

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VoiceBridge")

# Path absoluto para o modelo Vosk
_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
_VOSK_MODEL_DIR = _CONFIG_DIR / "vosk-model"

try:
    import sounddevice as sd
    AUDIO_DEVICE_AVAILABLE = True
except ImportError:
    AUDIO_DEVICE_AVAILABLE = False

try:
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

try:
    import pygame
    from pygame import mixer
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

class VoskSTT:
    """Interface para o modelo Vosk (STT de baixa latência, streaming)."""
    def __init__(self, model_path: str = None):
        self.model_path = str(model_path or _VOSK_MODEL_DIR)
        self.recognizer = None
        if VOSK_AVAILABLE:
            try:
                if os.path.exists(self.model_path):
                    self.model = Model(self.model_path)
                    self.recognizer = KaldiRecognizer(self.model, 16000)
                    logger.info(f"✅ Vosk carregado: {self.model_path}")
                else:
                    logger.warning(f"⚠️ Modelo Vosk não encontrado em '{self.model_path}'.")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao carregar Vosk: {e}")
    
    def process_chunk(self, data: bytes) -> Optional[str]:
        """Processa chunk de áudio e retorna texto se houver uma frase completa."""
        if not self.recognizer:
            return None
        try:
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip()
                return text if text else None
        except:
            return None
        return None


class SpeechRecognitionSTT:
    """Fallback STT usando speech_recognition (Google/Whisper). Modo listen-and-transcribe."""
    def __init__(self, language="pt-BR"):
        self.language = language
        self.recognizer = None
        self.microphone = None
        if SR_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            try:
                self.microphone = sr.Microphone()
                logger.info("✅ SpeechRecognition STT pronto (fallback).")
            except Exception as e:
                logger.warning(f"⚠️ Mic não acessível para SR: {e}")
    
    def listen_and_transcribe(self) -> Optional[str]:
        """Escuta o microfone e retorna texto transcrito (blocking)."""
        if not self.recognizer or not self.microphone:
            return None
        try:
            with self.microphone as source:
                logger.info("🎤 Ouvindo...")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text.strip() if text else None
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            logger.warning(f"⚠️ Erro no STT: {e}")
            return None

class VoiceBridge:
    """
    Ponte Full-Duplex para interação por voz natural.
    Mantém fluxo contínuo de entrada e saída.
    """

    def __init__(self, speech_cortex=None, neural_inference=None, use_sr_fallback=False, llm_context="APP_CHAT"):
        self.running = False
        self.input_queue = queue.Queue(maxsize=100)
        self.output_queue = queue.Queue(maxsize=10)
        self.use_sr_fallback = use_sr_fallback
        self.llm_context = llm_context
        
        # Injeção de dependência ou Singleton fallback
        if not speech_cortex:
            try:
                from cortex.specialists.speech_cortex import speech_cortex as sc
                self.speech_cortex = sc
            except ImportError:
                self.speech_cortex = None
        else:
            self.speech_cortex = speech_cortex

        if not neural_inference:
            try:
                import cortex.specialists.neural_inference as ni
                self.neural_inference = ni
            except ImportError:
                self.neural_inference = None
        else:
            self.neural_inference = neural_inference
        
        # Threads
        self._mic_thread = None
        self._speaker_thread = None
        self._processing_thread = None

        # STT Engine — Vosk (streaming) ou SpeechRecognition (fallback)
        self.stt = VoskSTT()  # Usa path absoluto automaticamente
        self.sr_stt = None
        if (not self.stt.recognizer) or use_sr_fallback:
            self.sr_stt = SpeechRecognitionSTT()
            if self.sr_stt.recognizer:
                logger.info("🔄 Usando SpeechRecognition como STT (fallback).")

        # TTS Engine — Defer initialization to _speaker_loop to prevent COM Threading Deadlock
        self.tts_engine = None
        self.edge_tts_available = EDGE_TTS_AVAILABLE
        self.voice_name = "pt-BR-ThalitaNeural" # pt-BR-FranciscaNeural, pt-BR-AntonioNeural
        
        # Temp dir for audio
        self.audio_temp_dir = _CONFIG_DIR.parent / "tmp_audio"
        os.makedirs(self.audio_temp_dir, exist_ok=True)

        # Config de Áudio (Padrão STT: 16kHz, Mono, 16bit)
        self.sample_rate = 16000
        self.channels = 1
        self.block_size = 1600 # 100ms de áudio por bloco
        
        # AEC & Interruption State
        self.aec_enabled = True
        self.is_speaking = False
        self.simulation_mode = not AUDIO_DEVICE_AVAILABLE
        self.interruption_detected = threading.Event()
        self.last_played_chunk = None

        if self.simulation_mode:
            logger.info("🛠️ Modo SIMULAÇÃO ativado (Hardware ou bibliotecas ausentes).")

    def start(self):
        """Inicia a ponte de voz."""
        if self.running:
            return
        
        self.running = True
        logger.info("🎙️ VoiceBridge v5.0: Iniciando ponte Full-Duplex...")
        
        # Decidir qual loop de processamento usar
        use_sr = self.use_sr_fallback or (not self.stt.recognizer and self.sr_stt)
        
        self._speaker_thread = threading.Thread(target=self._speaker_loop, daemon=True)
        self._speaker_thread.start()
        
        if use_sr and self.sr_stt and self.sr_stt.recognizer:
            # Modo SpeechRecognition: não precisa de mic_loop separado
            logger.info("📡 Modo STT: SpeechRecognition (Google)")
            self._processing_thread = threading.Thread(target=self._processing_loop_sr, daemon=True)
            self._processing_thread.start()
        else:
            # Modo Vosk: mic_loop + processing_loop
            logger.info("📡 Modo STT: Vosk (streaming local)")
            self._mic_thread = threading.Thread(target=self._mic_loop, daemon=True)
            self._processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
            self._mic_thread.start()
            self._processing_thread.start()

    def stop(self):
        """Para a ponte de voz."""
        self.running = False
        logger.info("🛑 VoiceBridge v4.0: Encerrando ponte.")

    def _mic_loop(self):
        """Loop de captura do microfone com Noise Suppression."""
        logger.info("🎤 Microfone em standby.")
        
        def callback(indata, frames, time, status):
            if status:
                logger.warning(f"⚠️ Mic Status: {status}")
            processed = self._apply_noise_suppression(indata.tobytes())
            if self.aec_enabled and self.last_played_chunk:
                processed = self._apply_aec(processed, self.last_played_chunk)
            self.input_queue.put(processed)

        if not self.simulation_mode:
            try:
                with sd.InputStream(samplerate=self.sample_rate, 
                                   channels=self.channels, 
                                   dtype='int16', 
                                   blocksize=self.block_size,
                                   callback=callback):
                    while self.running:
                        sd.sleep(100)
            except Exception as e:
                logger.error(f"❌ Erro no Microfone Físico: {e}")
                self.simulation_mode = True

        if self.simulation_mode:
            while self.running:
                # Gera silêncio ou buffers vazios
                self.input_queue.put(b'\x00' * (self.block_size * 2))
                time.sleep(0.1)

    def _speaker_loop(self):
        """Loop de saída para a caixa de som — TTS Neural via Edge-TTS e Pygame."""
        
        if self.edge_tts_available:
            try:
                # Ocultar welcome do pygame
                os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
                mixer.init(frequency=24000) # Frequência padrão do edge-tts
                logger.info("🔊 TTS Mixer (Pygame) inicializado.")
            except Exception as e:
                logger.warning(f"⚠️ Falha ao inicializar pygame mixer: {e}")
        
        logger.info("🔊 Saída de som pronta.")
        
        while self.running:
            try:
                item = self.output_queue.get(timeout=1)
                
                if isinstance(item, str):
                    self.is_speaking = True
                    logger.info(f"🔊 Falando: '{item[:50]}...'")
                    
                    if self.edge_tts_available:
                        # 1. Gerar MP3 com edge-tts
                        mp3_path = os.path.join(self.audio_temp_dir, f"reply_{int(time.time())}.mp3")
                        communicate = edge_tts.Communicate(item, self.voice_name)
                        asyncio.run(communicate.save(mp3_path))
                        
                        # 2. Tocar com pygame
                        mixer.music.load(mp3_path)
                        mixer.music.play()
                        
                        # 3. Esperar terminar de tocar (com suporte a interrupção)
                        while mixer.music.get_busy() and self.running:
                            if self.interruption_detected.is_set():
                                logger.info("🛑 Interrupção humana! Cortando áudio.")
                                mixer.music.stop()
                                break
                            time.sleep(0.1)
                            
                        # Limpar arquivo
                        try:
                            os.remove(mp3_path)
                        except: pass
                    else:
                        logger.warning("⚠️ edge-tts não disponível. Pulando fala.")
                    
                    self.is_speaking = False
                    self.interruption_detected.clear()
                    
                elif isinstance(item, list):
                    # Edge-TTS não suporta pulsos da mesma forma que SSML/pyttsx3
                    # Então juntamos o texto dos pulsos inteiros se vier prosódia
                    self.is_speaking = True
                    full_text = " ".join([p.get('text', '') for p in item if p.get('text')])
                    if full_text and self.edge_tts_available:
                        logger.info(f"🔊 Falando (from pulses): '{full_text[:50]}...'")
                        mp3_path = os.path.join(self.audio_temp_dir, f"reply_pulse_{int(time.time())}.mp3")
                        communicate = edge_tts.Communicate(full_text, self.voice_name)
                        asyncio.run(communicate.save(mp3_path))
                        
                        mixer.music.load(mp3_path)
                        mixer.music.play()
                        while mixer.music.get_busy() and self.running:
                            if self.interruption_detected.is_set():
                                mixer.music.stop()
                                break
                            time.sleep(0.1)
                        try:
                            os.remove(mp3_path)
                        except: pass
                    
                    self.is_speaking = False
                    self.interruption_detected.clear()
            except queue.Empty:
                continue

    def _processing_loop(self):
        """Loop de processamento: STT -> Cortex -> TTS."""
        logger.info("🧠 Canal cognitivo da ponte ativo.")
        while self.running:
            try:
                raw_audio = self.input_queue.get(timeout=1)
                
                # Processar com STT (Streaming via Vosk)
                text = self.stt.process_chunk(raw_audio)
                
                if text:
                    logger.info(f"🎤 Percebido: '{text}'")
                    if self.is_speaking:
                        logger.info("🛑 Ignorando STT (eco da própria voz).")
                        continue
                    self._generate_and_speak(text)
            except queue.Empty:
                continue

    def _processing_loop_sr(self):
        """Loop de processamento alternativo usando SpeechRecognition (blocking listen)."""
        logger.info("🧠 Canal cognitivo da ponte ativo (modo SpeechRecognition).")
        while self.running:
            if self.is_speaking:
                time.sleep(0.2)
                continue
            text = self.sr_stt.listen_and_transcribe()
            if text:
                logger.info(f"🎤 Percebido: '{text}'")
                if self.is_speaking:
                    logger.info("🛑 Ignorando STT (eco da própria voz).")
                    continue
                self._generate_and_speak(text)

    def _generate_and_speak(self, text: str):
        """Passa o texto reconhecido para o Orquestrador de Diálogo e fala a resposta."""
        try:
            logger.info(f"🧠 Enviando ao Orquestrador de Diálogo (Contexto: {self.llm_context})...")
            
            # Chama o orquestrador multi-modal para incluir memória e histórico
            result = extract_unified_prompt(text, audio_metadata={"active": True}, llm_context_override=self.llm_context)
            
            if result.get("status") == "OK":
                ai_text = result["intent"].get("ai_response", "")
            else:
                ai_text = "[Sistema] Falha no orquestrador cognitivo."
                
            logger.info(f"💬 Resposta: '{ai_text[:50]}...'")
            response_text = ai_text # Assign ai_text to response_text for the TTS part
        except Exception as e:
            logger.error(f"❌ Erro ao chamar Orquestrador de Diálogo: {e}")
            response_text = "Desculpe, tive um problema para processar sua solicitação."
        
        # Tentar prosódia, senão falar texto direto
        if self.speech_cortex:
            try:
                pulses = self.speech_cortex.encode_prosody(response_text)
                self.output_queue.put(pulses)
            except Exception as e:
                logger.warning(f"⚠️ Prosódia falhou: {e}. Falando texto direto.")
                self.output_queue.put(response_text)
        else:
            self.output_queue.put(response_text)

    def _apply_aec(self, mic_input: bytes, ref_signal: bytes) -> bytes:
        """
        Aplica Acoustic Echo Cancellation (AEC).
        Subtrai o sinal de referência (voz da Melanora) da entrada do mic.
        """
        if not ref_signal:
            return mic_input
            
        try:
            # Converte para array numpy para processamento
            nic_arr = np.frombuffer(mic_input, dtype=np.int16).astype(np.float32)
            ref_arr = np.frombuffer(ref_signal, dtype=np.int16).astype(np.float32)
            
            # Garante mesmo tamanho para subtração simples (fallback recursivo)
            min_len = min(len(nic_arr), len(ref_arr))
            # AEC Adaptativo Simples (Spectral Subtraction)
            # Em sistemas reais, usaríamos LMS/NLMS. Aqui aplicamos uma redução de ganho no sinal de eco.
            nic_arr[:min_len] -= (ref_arr[:min_len] * 0.7) 
            
            return nic_arr.astype(np.int16).tobytes()
        except:
            return mic_input

    def _apply_noise_suppression(self, audio_data: bytes) -> bytes:
        """Aplica supressão de ruído baseada em portão de ruído (Noise Gate)."""
        try:
            arr = np.frombuffer(audio_data, dtype=np.int16)
            rms = np.sqrt(np.mean(arr.astype(np.float32)**2))
            
            # Se o volume for muito baixo, silenciar (Noise Gate)
            if rms < 300: # Threshold empírico para ruído de fundo
                return b'\x00' * len(audio_data)
            return audio_data
        except:
            return audio_data

# Singleton para controle via Bridge
_bridge_instance = None

@cortex_function
def activate_voice_bridge() -> dict:
    """Ativa a ponte de voz full-duplex."""
    global _bridge_instance
    if not _bridge_instance:
        _bridge_instance = VoiceBridge()
    
    _bridge_instance.start()
    return {"status": "OK", "message": "VoiceBridge Ativado"}

@cortex_function
def deactivate_voice_bridge() -> dict:
    """Desativa a ponte de voz full-duplex."""
    global _bridge_instance
    if _bridge_instance:
        _bridge_instance.stop()
    return {"status": "OK", "message": "VoiceBridge Desativado"}

if __name__ == "__main__":
    bridge = VoiceBridge()
    try:
        bridge.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        bridge.stop()
