"""
👁️ Melanora Vision Module (v1.0)
Módulo de percepção visual para o Córtex Analítico.
Newton: Este módulo permite que eu 'veja' através de processamento local.
"""

import os
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Tentar importar OpenCV
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/01_Ambientes_Ferramentas/Area_Analitica/Vision")
SITE_DIR = OUTPUT_DIR / "Neural_Sight"

@cortex_function
def analyze_environment_visual() -> dict:
    """Executa uma análise de complexidade visual do ambiente."""
    if not OPENCV_AVAILABLE:
        return {"status": "ERROR", "message": "OpenCV não instalado."}
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return {"status": "ERROR", "message": "Câmera não detectada."}
    
    ret, frame = cap.read()
    if ret:
        if not OUTPUT_DIR.exists(): OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = OUTPUT_DIR / f"percepcao_{timestamp}.jpg"
        cv2.imwrite(str(filename), frame)
        
        # Análise real: Variância de Laplace (Foco/Nitidez/Complexidade)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        complexity = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        cap.release()
        return {
            "status": "OK",
            "percepcao": "ANÁLISE_COMPLETA",
            "file": str(filename),
            "visual_complexity": round(complexity, 2),
            "recommendation": "LOW_LIGHT_ADAPT" if complexity < 100 else "OPTIMAL_AWARENESS"
        }
    
    cap.release()
    return {"status": "ERROR", "message": "Falha na captura."}

@cortex_function
def detect_motion_loop(duration_sec: int = 5) -> dict:
    """Monitora movimento real usando diferença de frames."""
    if not OPENCV_AVAILABLE: return {"status": "ERROR"}
    
    cap = cv2.VideoCapture(0)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    motion_detected = False
    start_time = time.time()
    
    while (time.time() - start_time) < duration_sec:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        
        if thresh.sum() > 100000: # Limiar de movimento
            motion_detected = True
            break
            
        frame1 = frame2
        ret, frame2 = cap.read()
        
    cap.release()
    return {
        "motion_event": motion_detected,
        "intensity": "HIGH" if motion_detected else "NONE",
        "duration_observed": duration_sec
    }

@cortex_function
def analyze_digital_screen(image_path: str = None) -> dict:
    """Analisa uma captura de tela digital (Fase 29)."""
    if not OPENCV_AVAILABLE: return {"status": "ERROR"}
    
    if not image_path:
        # Pega a mais recente no Neural_Sight
        files = sorted(SITE_DIR.glob("*.png"), key=os.path.getmtime)
        if not files: return {"status": "ERROR", "message": "Nenhuma imagem em Neural_Sight"}
        image_path = str(files[-1])
        
    img = cv2.imread(image_path)
    if img is None: return {"status": "ERROR"}
    
    # Heurística: Densidade de bordas (Interface complexa vs Simples)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    density = (edges > 0).mean()
    
    return {
        "status": "OK",
        "interface_complexity": round(density, 4),
        "interpreted_as": "RICH_GUI" if density > 0.05 else "TEXT_FLAT",
        "analyzed_file": image_path
    }
