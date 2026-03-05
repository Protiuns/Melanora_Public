"""
👁️ Matemática Visual Periférica (Sistema 1a)
Extrai informações bidimensionais cruas da tela em altíssima velocidade.
Processamento de imagem focado em cores e formas, não em "semântica".
"""

try:
    import mss
    import cv2
    import numpy as np
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    mss = None
    cv2 = None
    np = None

import time
import json
import traceback
from cortex.utils.cortex_utils import cortex_function

class MathVisionCortex:
    def __init__(self, region=None):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Dependencies for MathVisionCortex are not available.")
        self.sct = mss.mss()
        self.region = region 
        
        self.color_ranges = {
            "green": (np.array([40, 50, 50]), np.array([80, 255, 255])),
            "red": (np.array([0, 150, 150]), np.array([10, 255, 255]))
        }
        
    def capture_frame(self):
        monitor = self.region if self.region else self.sct.monitors[0]
        sct_img = self.sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

    def analyze_scene(self, img) -> dict:
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        entities = []
        
        # 1. Procurar Verde (Cobra)
        lower_g, upper_g = self.color_ranges["green"]
        mask_g = cv2.inRange(hsv_img, lower_g, upper_g)
        contours_g, _ = cv2.findContours(mask_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours_g:
            area = cv2.contourArea(cnt)
            if area > 100:
                x, y, w, h = cv2.boundingRect(cnt)
                entities.append({
                    "type": "green_mass",
                    "bbox": [x, y, w, h],
                    "area": area
                })
                
        # 2. Procurar Vermelho (Maçã)
        lower_r, upper_r = self.color_ranges["red"]
        mask_r = cv2.inRange(hsv_img, lower_r, upper_r)
        contours_r, _ = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours_r:
            area = cv2.contourArea(cnt)
            if area > 50:
                x, y, w, h = cv2.boundingRect(cnt)
                entities.append({
                    "type": "red_mass",
                    "bbox": [x, y, w, h],
                    "area": area
                })

        return {"entities": entities, "resolution": [img.shape[1], img.shape[0]]}

    def perceive_continuously(self, callback, fps=15, duration_sec=10):
        start_time = time.time()
        frame_time = 1.0 / fps
        try:
            while time.time() - start_time < duration_sec:
                loop_start = time.time()
                img = self.capture_frame()
                scene_data = self.analyze_scene(img)
                if scene_data["entities"]:
                    callback(scene_data)
                elapsed = time.time() - loop_start
                if elapsed < frame_time:
                    time.sleep(frame_time - elapsed)
        except KeyboardInterrupt:
            pass

@cortex_function
def watch_gameplay(duration_sec: int = 10, target_fps: int = 5) -> dict:
    """Captura e analisa visualmente o gameplay por um período."""
    if not DEPENDENCIES_AVAILABLE:
        return {"error": "Dependencies not available"}
        
    captured_data = []
    try:
        vision = MathVisionCortex()
        start_time = time.time()
        while time.time() - start_time < duration_sec:
            img = vision.capture_frame()
            scene = vision.analyze_scene(img)
            captured_data.append(scene)
            time.sleep(1.0 / target_fps)
    except Exception as e:
        return {"error": str(e)}
        
    return {"status": "OK", "captured_frames": len(captured_data)}

if __name__ == "__main__":
    pass
