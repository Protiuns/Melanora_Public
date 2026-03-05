"""
🦾 Córtex Motor (Atuadores Físicos Virtuais)
Responsável por converter decisões cognitivas em inputs reais no nível do Sistema Operacional.
Simula mãos humanas (Teclado e Mouse) usando PyAutoGUI / Keyboard.
"""

import time
import logging

# Usando pyautogui como atuador cross-platform padrão para evitar lock de permissão de admin
try:
    import pyautogui
    pyautogui.FAILSAFE = False # Permitir movimentos extremos na tela se necessário
except ImportError:
    pyautogui = None
    logging.warning("[AVISO] PyAutoGUI nao encontrado. Atuadores simulados na nuvem. Rode: pip install pyautogui")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [MOTOR] %(message)s")

class VirtualMotorCortex:
    def __init__(self):
        self.active = True
        
    def press_key(self, key_name: str):
        """Pressiona uma tecla virtual. Mapeamento para nomes padrão."""
        if not self.active: return
        
        # Mapeamento de setas (ArrowUp -> up)
        key_map = {
            "ArrowUp": "up",
            "ArrowDown": "down",
            "ArrowLeft": "left",
            "ArrowRight": "right",
            "Enter": "enter",
            "Space": "space"
        }
        
        target_key = key_map.get(key_name, key_name.lower())
        
        logging.info(f"Disparando tecla: [{target_key}]")
        if pyautogui:
            pyautogui.press(target_key)
            
    def move_mouse_to(self, x: int, y: int, duration: float = 0.1):
        """Move o mouse humanoide."""
        if not self.active: return
        logging.info(f"Movendo mouse para ({x}, {y})")
        if pyautogui:
            pyautogui.moveTo(x, y, duration=duration)
            
    def click(self):
        """Clica o botão esquerdo."""
        if not self.active: return
        logging.info("Clique esquerdo simulado")
        if pyautogui:
            pyautogui.click()
            
    def hold_gamepad_button(self, button_name: str, duration: float):
        """Placeholder para futuro projeto de Gamepad (VJoy / XInput)."""
        logging.warning(f"Feature de Gamepad não conectada ainda. Botão solicitado: {button_name}")


motor = VirtualMotorCortex()

def physical_press(key: str):
    motor.press_key(key)

if __name__ == "__main__":
    # Teste unitário do motor
    print("Testando reflexo motor em 3 segundos. O mouse deve ir para o centro da tela e rolar para baixo se possível.")
    time.sleep(3)
    motor.move_mouse_to(500, 500)
    print("Enviando comando de seta para baixo...")
    motor.press_key("ArrowDown")
    print("Teste motor concluído.")
