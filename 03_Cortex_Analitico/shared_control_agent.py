import mss
import numpy as np
import cv2
import pydirectinput
import time
import json
import os
from datetime import datetime

class SharedControlAgent:
    def __init__(self, region=None):
        self.sct = mss.mss()
        # Default region: Center of screen (approx 400x400)
        if region is None:
            monitor = self.sct.monitors[1]
            width, height = 400, 400
            self.region = {
                "top": (monitor["height"] - height) // 2,
                "left": (monitor["width"] - width) // 2,
                "width": width,
                "height": height
            }
        else:
            self.region = region
            
        self.active = False
        self.last_capture_time = 0
        self.fps_log = []
        self.focus_region = None # For guided training

    def start_sync(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Neural_Sync: STARTING_SHARED_CONTROL_SESSION")
        self.active = True
        self.perception_loop()

    def stop_sync(self):
        self.active = False
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Neural_Sync: SHARED_CONTROL_STOPPED")

    def set_focus(self, top, left, width, height):
        """Sets a specific focus area for guided training."""
        self.focus_region = {"top": top, "left": left, "width": width, "height": height}
        print(f"Neural_Focus: Region set to {self.focus_region}")

    def clear_focus(self):
        self.focus_region = None
        print("Neural_Focus: Cleared. Returning to Global Window.")

    def perception_loop(self):
        wander_cycles = 0
        while self.active:
            start_time = time.time()
            
            # 1. Capture Perception (Screen or Focus Region)
            capture_area = self.focus_region if self.focus_region else self.region
            screenshot = self.sct.grab(capture_area)
            img = np.array(screenshot)
            
            # 2. Process Patterns (Shared Agency Context)
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            avg_color = [float(c) for c in np.mean(frame, axis=(0, 1))]
            
            # 3. Sensory Pulses (Fase 12 & 13)
            try:
                from neural_bridge import direct_execute
                
                # Pulso de Visão
                direct_execute("perception_engine", "process_sensory_pulse", {
                    "source_type": "VISION",
                    "features": {"avg_color": avg_color, "focus": "GUI_ELEMENT"}
                })
                
                # 4. Neural Motor Autonomy (Fase 12+)
                if self.active:
                    # Tentar jogar se houver detecção
                    snake_state = direct_execute("gaming_specialist", "detect_snake_state", {"frame_bgr": frame})
                    if snake_state.get("result", {}).get("active"):
                        move = direct_execute("gaming_specialist", "decide_snake_move", {"state": snake_state["result"]})
                        if move.get("result"):
                            direct_execute("gaming_specialist", "execute_game_command", {"command": move["result"]})
                            wander_cycles = 0 # Reinicia wander se estiver jogando
                    
                    # 5. Wander/Discovery Mode (Fase 13)
                    elif not self.focus_region or wander_cycles > 50:
                        wander_cycles += 1
                        if wander_cycles % 10 == 0: # A cada ~1s tenta descobrir
                            discovery = direct_execute("heuristic_discovery", "analyze_screen_salience", {"frame_bgr": frame})
                            regions = discovery.get("result", {}).get("top_regions", [])
                            
                            # Se encontrar uma região promissora, focar nela temporariamente para testar se é o jogo
                            if regions:
                                best = regions[0]
                                if not self.focus_region:
                                    print(f"[AUTONOMY] Heurística detectou região saliente. Focando em {best['x']}, {best['y']}")
                                    self.set_focus(best['y'], best['x'], best['w'], best['h'])
                                    wander_cycles = 0
            except Exception as e:
                pass

            # 6. Performance Tracking
            end_time = time.time()
            dt = end_time - start_time
            if dt > 0:
                fps = 1.0 / dt
                self.fps_log.append(fps)
                if len(self.fps_log) > 60: self.fps_log.pop(0)
            
            if len(self.fps_log) % 10 == 0:
                avg_fps = sum(self.fps_log) / len(self.fps_log) if self.fps_log else 0
                mode_label = "FOCUS" if self.focus_region else "GLOBAL"
                print(f"Neural_Window: {mode_label} | FPS: {avg_fps:.1f} | Avg_Color: {avg_color}")

if __name__ == "__main__":
    # Test Run
    agent = SharedControlAgent()
    try:
        print("Starting 50-frame Shared Control Test...")
        agent.active = True
        for _ in range(50):
            agent.perception_loop()
        agent.stop_sync()
            
    except KeyboardInterrupt:
        agent.stop_sync()
