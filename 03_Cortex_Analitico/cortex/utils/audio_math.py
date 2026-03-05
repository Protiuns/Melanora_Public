"""
📊 Melanora Audio Math Utilities (v1.0)
Funções de processamento de sinal digital (DSP) para o Córtex Analítico.
Traduzindo ondas sonoras em 'Brilho' matemático.
"""

import numpy as np
try:
    from scipy.fft import fft, fftfreq
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

def compute_fft(signal: np.ndarray, sample_rate: int) -> dict:
    """Calcula a FFT de um sinal e retorna os componentes de frequência e magnitude."""
    if not SCIPY_AVAILABLE:
        return {"peak_freq": 0, "peak_magnitude": 0, "error": "scipy missing"}
        
    n = len(signal)
    yf = fft(signal)
    xf = fftfreq(n, 1 / sample_rate)
    
    # Apenas frequências positivas
    xf = xf[:n//2]
    yf = 2.0/n * np.abs(yf[:n//2])
    
    return {
        "frequencies": xf.tolist(),
        "magnitudes": yf.tolist(),
        "peak_freq": float(xf[np.argmax(yf)]),
        "peak_magnitude": float(np.max(yf))
    }

def get_audio_metrics(signal: np.ndarray) -> dict:
    """Extrai métricas básicas do buffer de áudio (RMS, Peak)."""
    rms = np.sqrt(np.mean(signal**2))
    peak = np.max(np.abs(signal))
    
    return {
        "rms": float(rms),
        "peak": float(peak),
        "db": float(20 * np.log10(rms + 1e-10))
    }

def analyze_spectral_centroid(frequencies: np.ndarray, magnitudes: np.ndarray) -> float:
    """Calcula o centroide espectral (indica o 'brilho' ou 'escuridão' do som)."""
    return float(np.sum(frequencies * magnitudes) / (np.sum(magnitudes) + 1e-10))
