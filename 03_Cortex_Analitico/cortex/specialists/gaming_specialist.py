"""
🎮 Melanora Gaming Specialist (v1.0)
Especialista em visão computacional para jogos clássicos (Snake PoC).
Traduz frames visuais em vetores de movimento.
"""

try:
    import cv2
    import numpy as np
    import pyautogui
    import pydirectinput
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    np = None
    cv2 = None
    pyautogui = None
    pydirectinput = None

import time
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

@cortex_function
def detect_snake_state(image_path: str) -> dict:
    """
    Analisa um frame do jogo Snake e identifica a cabeça e a comida.
    Focado na versão: https://patorjk.com/games/snake/
    """
    if not DEPENDENCIES_AVAILABLE:
        return {"error": "Dependencies not available"}
    
    frame = cv2.imread(image_path)
    if frame is None:
        return {"error": f"Could not read image at {image_path}"}

    # Converter para HSV para melhor detecção de cores
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Comida (Vermelho)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.add(mask_red1, mask_red2)
    
    # Snake (Geralmente escuro ou verde no fundo claro)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detecção adaptativa para lidar com diferentes fundos
    mask_snake = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY_INV, 11, 2)
    
    # Encontrar contornos da comida
    cnts_food, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    food_pos = None
    if cnts_food:
        cnts_food = [c for c in cnts_food if 5 < cv2.contourArea(c) < 500]
        if cnts_food:
            c = max(cnts_food, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                food_pos = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # Encontrar contornos da cobra
    cnts_snake, _ = cv2.findContours(mask_snake, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    snake_head = None
    if cnts_snake:
        cnts_snake = [c for c in cnts_snake if cv2.contourArea(c) > 10]
        if cnts_snake:
            c = max(cnts_snake, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                snake_head = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    return {
        "food": food_pos,
        "head": snake_head,
        "active": food_pos is not None and snake_head is not None,
        "metadata": {"food_detected": food_pos is not None, "snake_detected": snake_head is not None}
    }

@cortex_function
def check_game_over(image_path: str) -> bool:
    """Detecta se o jogo acabou."""
    if not DEPENDENCIES_AVAILABLE: return False
    
    frame = cv2.imread(image_path)
    if frame is None: return False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    roi = gray[height//3:2*height//3, width//3:2*width//3]
    
    _, thresh = cv2.threshold(roi, 100, 255, cv2.THRESH_BINARY_INV)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return 10 < len(cnts) < 50

@cortex_function
def restart_game():
    """Tenta reiniciar o jogo."""
    if not DEPENDENCIES_AVAILABLE: return False
    pydirectinput.press("space")
    time.sleep(0.5)
    pydirectinput.press("enter")
    log_event("GAME_MOTOR: Restart attempt.")
    return True

@cortex_function
def decide_snake_move(state: dict, last_move: str = None) -> str:
    """Retorna o comando de tecla."""
    if not state.get("active"):
        return None
    
    head = state["head"]
    food = state["food"]
    
    dx = food[0] - head[0]
    dy = food[1] - head[1]
    
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    
    possible_moves = []
    if dx > 0: possible_moves.append("right")
    elif dx < 0: possible_moves.append("left")
    
    if dy > 0: possible_moves.append("down")
    elif dy < 0: possible_moves.append("up")
    
    if not possible_moves: return last_move
    
    for move in sorted(possible_moves, key=lambda x: abs(dx) if x in ["left", "right"] else abs(dy), reverse=True):
        if move != opposites.get(last_move):
            return move
            
    return possible_moves[0]

@cortex_function
def execute_game_command(command: str):
    """Executa o comando de hardware."""
    if not DEPENDENCIES_AVAILABLE: return False
    if command in ["up", "down", "left", "right"]:
        pydirectinput.press(command)
        return True
    return False
