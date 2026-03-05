"""
👀 Comentarista Espectador (Visão Biomimética)
Usa o MathVision (OpenCV) para "assistir" o humano jogador.
Ao invés de emitir comandos para o motor atuar, ele emite comentários falados no terminal.
"""

import time
import sys
import platform

try:
    from cortex.perception.math_vision import MathVisionCortex
except ImportError as e:
    print(f"Erro de importação: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("[SYSTEM] Preparando os sensores... Estou pronta para assistir voce, Newton!")
    print("[INFO] Eu (Melanora) serei a sua comentarista.")
    print("Vou tentar focar nos movimentos da sua tela usando minha Visao Matematica.")
    print("Abra o jogo Snake (seu ou o nosso Lab). Tem 5 segundos...")
    for i in range(5, 0, -1):
        time.sleep(1)

class SportsCommentator:
    def __init__(self):
        self.last_apple_pos = None
        self.snack_count = 0
        self.last_comment_time = time.time()
        
    def watch(self, scene_data):
        now = time.time()
        entities = scene_data.get("entities", [])
        green_masses = [e for e in entities if e["type"] == "green_mass"]
        red_masses = [e for e in entities if e["type"] == "red_mass"]
        
        # Filtra o spam para falar no máximo a cada 1.5s
        if now - self.last_comment_time < 1.5:
            return
            
        if not green_masses:
            print("[DICA] Newton, cade a cobra?? Voce morreu ou saiu do jogo?")
            self.last_comment_time = now
            return
            
        if red_masses:
            apple = red_masses[0]["bbox"]
            
            # Se a maçã mudou de lugar, quer dizer que você pegou a antiga
            if self.last_apple_pos and (
                abs(apple[0] - self.last_apple_pos[0]) > 20 or 
                abs(apple[1] - self.last_apple_pos[1]) > 20
            ):
                self.snack_count += 1
                print(f"[BOA!] PEGOU! Boa, Newton! Ja sao {self.snack_count} macas! Cresce cobrinha!")
                self.last_apple_pos = apple
                self.last_comment_time = now
                return
                
            self.last_apple_pos = apple
            
            # Comentário espacial
            head = green_masses[0]["bbox"]
            dx = apple[0] - head[0]
            dy = apple[1] - head[1]
            
            if abs(dx) > abs(dy):
                if dx > 0: print("[->] Vai pra direita! Pega aquela maca!")
                else: print("[<-] Ta na esquerda, Newton, nao deixa escapar!")
            else:
                if dy > 0: print("[V] Desce pra pegar!")
                else: print("[A] A maca ta em cima!")
                
            self.last_comment_time = now

commentator = SportsCommentator()
if __name__ == "__main__":
    vision = MathVisionCortex()
    
    print("\n(Olhos Abertos. Pressione Ctrl+C a qualquer momento para eu fechar os olhos.)\n")
    
    try:
        vision.perceive_continuously(commentator.watch, fps=15, duration_sec=60)
    except KeyboardInterrupt:
        print("\n[OK] Cansei de assistir por agora. Foi divertido!")
    except Exception as e:
        print(f"[ERRO] Deu algo errado nos meus olhos virtuais: {e}")
    
    print("[FINAL] Sessao de observacao finalizada. Foi otimo te ver jogar!")
