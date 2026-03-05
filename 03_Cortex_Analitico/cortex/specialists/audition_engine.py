"""
🔊 Melanora Audition Engine (v1.0)
Gateway Auditivo Modular: Escutando o silêncio e o brilho dos sistemas.
"""

import os
import time
import json
import numpy as np
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event
from cortex.utils.audio_math import compute_fft, get_audio_metrics

# Interconexão Sensorial
try:
    from cortex.logic.synthesis_engine import process_sensory_pulse
    SYNTHESIS_AVAILABLE = True
except ImportError:
    SYNTHESIS_AVAILABLE = False

# Dependências Dinâmicas
try:
    import sounddevice as sd
    from scipy.io import wavfile
    AUDIO_AVAILABLE = True
except (ImportError, SystemError, Exception):
    # Newton: Se houver mismatch de NumPy/SciPy, desativamos o áudio mas mantemos a mente rodando.
    AUDIO_AVAILABLE = False

BASE_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora")
OUTPUT_DIR = BASE_DIR / "01_Ambientes_Ferramentas/Area_Analitica/Audition"

@cortex_function
def list_audio_sources() -> dict:
    """Lista todas as fontes de áudio (Input e Loopback) disponíveis."""
    if not AUDIO_AVAILABLE:
        return {"status": "ERROR", "message": "Sounddevice não instalado."}
    
    devices = sd.query_devices()
    return {"status": "OK", "devices": [str(d) for d in devices]}

@cortex_function
def capture_audio_sample(source: str = "MIC", duration_s: float = 2.0, sample_rate: int = 44100) -> dict:
    """
    Captura uma amostra de áudio de uma fonte modular.
    source: 'MIC' ou o index do dispositivo de Loopback.
    """
    if not AUDIO_AVAILABLE:
        return {"status": "ERROR", "message": "Audio Engine offline."}
    
    try:
        # Tentar capturar áudio
        # Nota: Capturar loopback no windows exige o device correto via WASAPI
        recording = sd.rec(int(duration_s * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        
        # Processamento básico
        recording = recording.flatten()
        metrics = get_audio_metrics(recording)
        spectral = compute_fft(recording, sample_rate)
        
        # Salvar arquivo temporário se necessário
        if not OUTPUT_DIR.exists(): OUTPUT_DIR.mkdir(parents=True)
        filename = OUTPUT_DIR / f"ear_{source.lower()}_{int(time.time())}.wav"
        # cast to int16 for wav
        wav_data = (recording * 32767).astype(np.int16)
        # scipy.io.wavfile.write(str(filename), sample_rate, wav_data)
        
        # Pulso Sensorial para Síntese
        if SYNTHESIS_AVAILABLE:
            process_sensory_pulse("AUDIO", {**metrics, "peak_freq": spectral["peak_freq"]})
        
        return {
            "status": "OK",
            "source": source,
            "metrics": metrics,
            "peak_freq": spectral["peak_freq"],
            "brilliance": spectral["peak_magnitude"] # Placeholder para brilho analítico
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@cortex_function
def register_sound_identity(environment_name: str, sound_data: dict) -> dict:
    """Registra uma identidade sonora no banco de dados descentralizado do ambiente."""
    env_path = BASE_DIR / "01_Ambientes_Ferramentas" / environment_name
    registry_path = env_path / "neural_registry" / "sounds"
    
    if not registry_path.exists():
        registry_path.mkdir(parents=True)
    
    sound_id = sound_data.get("id", f"sound_{int(time.time()*1000)}")
    file_path = registry_path / f"{sound_id}.json"
    
    sound_data["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    sound_data["type"] = "AUDITION_IDENTITY"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sound_data, f, indent=2, ensure_ascii=False)
    
    # Pulso Sensorial para Síntese (Solidificação)
    if SYNTHESIS_AVAILABLE:
        process_sensory_pulse("AUDIO", sound_data.get("characteristics", {}))
        
    log_event(f"Som identificado e registrado: {sound_id} em {environment_name}")
    return {"status": "OK", "id": sound_id, "path": str(file_path)}
