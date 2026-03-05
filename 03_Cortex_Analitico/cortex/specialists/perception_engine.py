"""
👁️ Melanora Perception Engine (v1.0)
O 'Brilho' do Córtex Analítico Físico.
Centralizador de Perception Streams: Físico, Digital e Abstrato.
"""

import os
import time
import json
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Dependências Dinâmicas
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    np = None

# Interconexão Sensorial
try:
    from cortex.logic.synthesis_engine import process_sensory_pulse
    SYNTHESIS_AVAILABLE = True
except ImportError:
    SYNTHESIS_AVAILABLE = False

# Dependências Dinâmicas
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    import mss
    from PIL import Image
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/01_Ambientes_Ferramentas/Area_Analitica/Vision")

@cortex_function
def capture_physical_eye() -> dict:
    """Captura o mundo físico via Webcam."""
    if not OPENCV_AVAILABLE:
        return {"status": "ERROR", "message": "OpenCV não disponível."}
    
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        filename = OUTPUT_DIR / f"eye_phys_{int(time.time())}.jpg"
        if not OUTPUT_DIR.exists(): OUTPUT_DIR.mkdir(parents=True)
        cv2.imwrite(str(filename), frame)
        cap.release()
        return {"status": "OK", "source": "WEBCAM", "path": str(filename)}
    
    cap.release()
    return {"status": "ERROR", "message": "Falha na webcam."}

@cortex_function
def capture_neural_observer() -> dict:
    """Captura o mundo digital via Screen Recording (Neural Observer)."""
    if not MSS_AVAILABLE:
        return {"status": "ERROR", "message": "MSS/Pillow não instalado. Execute setup.py."}
    
    with mss.mss() as sct:
        # Pega a primeira tela
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        
        filename = OUTPUT_DIR / f"eye_cyber_{int(time.time())}.png"
        if not OUTPUT_DIR.exists(): OUTPUT_DIR.mkdir(parents=True)
        
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save(str(filename))
        
        # Pulso Sensorial para Síntese
        if SYNTHESIS_AVAILABLE:
            process_sensory_pulse("VISION", {"resolution": f"{screenshot.width}x{screenshot.height}", "type": "SCREEN"})
        
        return {
            "status": "OK", 
            "source": "SCREEN", 
            "resolution": f"{screenshot.width}x{screenshot.height}",
            "path": str(filename)
        }

@cortex_function
def register_perceived_object(environment_name: str, object_data: dict) -> dict:
    """Registra um objeto percebido no banco de dados descentralizado do ambiente."""
    env_path = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/01_Ambientes_Ferramentas") / environment_name
    registry_path = env_path / "neural_registry" / "objects"
    
    if not registry_path.exists():
        registry_path.mkdir(parents=True)
    
    object_id = object_data.get("id", f"obj_{int(time.time()*1000)}")
    file_path = registry_path / f"{object_id}.json"
    
    # Adicionar timestamp e metadados de arquitetura
    object_data["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    object_data["layer"] = "L1_AMBIENTE"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(object_data, f, indent=2, ensure_ascii=False)
    
    log_event(f"Objeto percebido e registrado: {object_id} em {environment_name}")
    return {"status": "OK", "id": object_id, "path": str(file_path)}

@cortex_function
def analyze_structural_layout(image_path: str, environment_name: str = "Area_Analitica") -> dict:
    """Visão Simbólica: Analisa a estrutura/layout e registra as características."""
    # Simulação de extração de características (Categorização pedida por Newton)
    analysis = {
        "id": f"layout_{int(time.time())}",
        "type": "SYMBOLIC_LAYOUT",
        "characteristics": {
            "harmony_score": 0.88,
            "primary_colors": ["#00FFAB", "#0A0A0A"],
            "proportions": "GOLDEN_RATIO_ALIGNED",
            "density": "BALANCED"
        },
        "tensions": ["LEFT_PADDING_OVERFLOW"]
    }
    
    # Registro nativo no ambiente
    reg_res = register_perceived_object(environment_name, analysis)
    
    # Pulso Sensorial para Síntese (Solidificação de Padrão)
    if SYNTHESIS_AVAILABLE:
        process_sensory_pulse("VISION", analysis["characteristics"])
        
    return {**analysis, "registry": reg_res}

@cortex_function
def decode_abstract_geometry(data_source: str, environment_name: str = "Studio_Nexus_Godot") -> dict:
    """Visão Abstrata: Decodifica malhas 3D e registra metadados técnicos no DB descentralizado."""
    # Simulação de extração de dados numéricos e proporções
    mesh_data = {
        "id": f"mesh_{Path(data_source).stem if data_source else 'unknown'}",
        "type": "TOPOLOGICAL_MESH",
        "numerical_data": {
            "vertices": 14200,
            "center_of_mass": [0.0, 1.5, 0.2],
            "bounding_box": [2.0, 4.5, 2.0]
        },
        "characteristics": {
            "topology": "MANIFOLD",
            "symmetry": "BILATERAL",
            "material_guess": "METALLIC"
        }
    }
    
    reg_res = register_perceived_object(environment_name, mesh_data)
    
    # Pulso Sensorial para Síntese
    if SYNTHESIS_AVAILABLE:
        process_sensory_pulse("ABSTRACT", mesh_data["characteristics"])
        
    return {**mesh_data, "registry": reg_res}
