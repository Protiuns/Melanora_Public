"""
🏛️ Melanora Standalone Gaming Autonomy Test
Bypasses the Neural Bridge to run the perception-action loop directly.
"""
import sys
import os
import time
import numpy as np
import cv2
import mss
import pydirectinput
from pathlib import Path

# Add project root to path
BASE_DIR = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico")
sys.path.append(str(BASE_DIR))

# Mock cortex_function to avoid imports
def cortex_function(func): 
    func._cortex_function = True
    return func

try:
    from cortex.specialists.gaming_specialist import detect_snake_state, decide_snake_move, execute_game_command, check_game_over, restart_game
    from cortex.specialists.heuristic_discovery import analyze_screen_salience
    from cortex.specialists.synesthesia_bridge import map_spatial_to_qualia, generate_sensory_harmony
    from learning_metrics import record_match
    print("[MIND] Especialistas carregados para Treinamento.")
except Exception as e:
    print(f"[CRITICAL] Erro ao carregar especialistas: {e}")
    sys.exit(1)

def focus_browser():
    """Tenta trazer o navegador para frente."""
    import subprocess
    ps_cmd = """
    $wshell = New-Object -ComObject WScript.Shell;
    $edge = Get-Process | Where-Object {$_.ProcessName -eq "msedge" -or $_.ProcessName -eq "chrome" -or $_.ProcessName -eq "firefox"};
    if ($edge) {
        $wshell.AppActivate($edge[0].Id);
        Write-Output "Browser focused";
    }
    """
    subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)

def run_training_session(max_matches=20, target_score=40):
    sct = mss.mss()
    monitor = sct.monitors[1] 
    
    print(f"[TRAINING] Iniciando Sessao de Treinamento: {max_matches} partidas | Alvo: {target_score}")
    focus_browser()
    time.sleep(2)
    
    match_count = 0
    best_score = 0
    focus_region = None
    
    while match_count < max_matches:
        match_count += 1
        print(f"\n[GAME] --- PARTIDA {match_count} / {max_matches} ---")
        
        score = 0
        last_food = None
        last_move = None
        match_start = time.time()
        resonance_sum = 0
        cycles = 0
        idle_count = 0
        
        # Pressionar algo para começar se necessário
        pydirectinput.press("enter")
        time.sleep(1)
        
        while True:
            # 1. Percepção
            capture_area = focus_region if focus_region else monitor
            screenshot = sct.grab(capture_area)
            frame = np.array(screenshot)
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # 2. Verificar Game Over (Apenas se já tiver começado a jogar)
            if cycles > 10 and check_game_over(frame_bgr):
                print("💀 Game Over detectado.")
                break
            
            # 3. Estado do Jogo
            state = detect_snake_state(frame_bgr)
            
            if state.get("active"):
                idle_count = 0
                # Tracking de Score
                current_food = state["food"]
                if last_food and current_food != last_food:
                    score += 1
                    print(f"[SCORE] Maca consumida! Score Atual: {score}")
                last_food = current_food
                
                # Sinestesia
                qualia_pkg = map_spatial_to_qualia(state)
                q = qualia_pkg.get("qualias", {})
                resonance_sum += q.get("neural_resonance", 0.1)
                cycles += 1
                
                # Decisão e Ação
                move = decide_snake_move(state, last_move)
                if move:
                    execute_game_command(move)
                    last_move = move
            else:
                idle_count += 1
                if idle_count > 50: # Se ficar muito tempo sem ver nada
                    print("⚠️ Jogo parece ter sumido ou travado. Buscando...")
                    discovery = analyze_screen_salience(frame_bgr)
                    regions = discovery.get("top_regions", [])
                    if regions:
                        best = regions[0]
                        focus_region = {
                            "top": monitor["top"] + best["y"], 
                            "left": monitor["left"] + best["x"], 
                            "width": best["w"], 
                            "height": best["h"]
                        }
                    idle_count = 0
                
                if cycles > 20 and idle_count > 30: # Provável Game Over não detectado
                     break
            
            time.sleep(0.04) # 25 FPS para maior fluidez
            
        # Fim da Partida
        duration = time.time() - match_start
        avg_res = resonance_sum / max(1, cycles)
        record_match(match_count, score, avg_res, duration)
        
        best_score = max(best_score, score)
        if score >= target_score:
            print(f"🏅 Objetivo atingido! Score de {score} alcançado.")
            break
            
        print("🔄 Reiniciando em 2 segundos...")
        time.sleep(2)
        restart_game()
        time.sleep(1)

    print(f"\n[FINISH] Sessão Finalizada. Melhor Score: {best_score}")

if __name__ == "__main__":
    run_training_session()
