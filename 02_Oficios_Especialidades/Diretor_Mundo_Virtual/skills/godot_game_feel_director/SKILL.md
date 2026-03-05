---
name: Godot Game Feel Director
description: Especialista em Game Feel, Juice e Feedback Loops Matemáticos (Trauma, Decay, Curves). Garante satisfação tátil em cada input.
---

# 🎮 Godot Game Feel Director (Godot 4.6+)

Esta skill substitui "Game Feel UX" e "Feedback Architect". Ela sai do campo das ideias vagas ("fazer tremer") e entra na matemática do prazer sensorial.

## 🧪 Filosofia: "Input -> Response -> Satisfaction"

Game Feel não é mágica, é matemática. É a resposta imediata, exagerada e polida para as ações do jogador.
Nossa abordagem se baseia em **Trauma Systems**, **Freeze Frames** e **Curve Tuning**.

## 🛡️ O Protocolo de Trauma (Screen Shake 2.0)

Esqueça `random_offset(5)`. Isso é amador.
Usamos um sistema de **Trauma (0.0 a 1.0)** com decaimento.

### A Fórmula do Trauma
```gdscript
var shake_amount = pow(trauma, 2) * max_offset
rotation = max_roll * shake_amount * noise.get_noise_1d(time)
offset = max_offset * shake_amount * noise.get_noise_2d(seed, time)
```
*   **Por que ao quadrado?** Para que traumas leves (0.3) sejam quase imperceptíveis, mas traumas altos (0.9) sejam catastróficos.
*   **Noise:** Usamos `FastNoiseLite` para movimentos suaves, não randômicos.

## 🛠️ The Juice Stack (Camadas de Feedback)

Para CADA interação principal (Pulo, Tiro, Dano), você deve implementar a **Pilha Completa**:

1.  **Visual (Instant):**
    *   Flash Branco (Shader/Modulate).
    *   Squash & Stretch (Escala `1.2, 0.8` -> `1.0, 1.0`).
    *   Partículas (Via `godot_vfx_master`).

2.  **Audio (Instant):**
    *   SFX com Variação de Pitch (Via `godot_audio_master`).

3.  **Camera (Trauma):**
    *   `Camera.add_trauma(0.4)` (Tiro).
    *   `Camera.add_trauma(0.8)` (Explosão).

4.  **Time (Freeze):**
    *   `HitStop.freeze(0.05)` para impactos pesados.
    *   Isso vende o "peso" do golpe.

5.  **Controller (Haptics):**
    *   `Input.start_joy_vibration(0, trauma, trauma, 0.2)`.

## 🕹️ Input Buffering & Coyote Time

Game Feel também é controle. O jogo deve ser generoso.
*   **Jump Buffer:** O jogador apertou pular 0.1s antes de tocar o chão? O jogo deve registrar e pular assim que tocar.
*   **Coyote Time:** O jogador saiu da plataforma faz 0.1s? Permita que ele pule mesmo assim.

## 📝 Checklist de Validação
1.  [ ] A câmera usa Noise e não Random?
2.  [ ] O screen shake decai suavemente?
3.  [ ] Existe HitStop em impactos fortes?
4.  [ ] O controle vibra em sincronia com a tela?

---
"O jogo deve ser gostoso de jogar mesmo em um cubo cinza."

---

## 📐 Curvas de Bézier (Trajetórias e Animação)

Bézier Cúbica com 4 pontos de controle — ideal para projéteis curvos, knockback em arco, e animações de menu:
```gdscript
func cubic_bezier(t: float, p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2) -> Vector2:
    var u = 1.0 - t
    return u*u*u*p0 + 3.0*u*u*t*p1 + 3.0*u*t*t*p2 + t*t*t*p3
```
- `t` vai de 0.0 a 1.0 (progresso ao longo da curva).
- `p0/p3` = início/fim. `p1/p2` = pontos de controle (influenciam a curvatura).

## 📊 Easing Functions (Cheat Sheet)

| Nome | Fórmula | Sensação |
|------|---------|----------|
| ease_in_quad | `t * t` | Início lento, acelera |
| ease_out_quad | `t * (2 - t)` | Início rápido, desacelera |
| ease_in_out_cubic | `t < 0.5 ? 4*t³ : 1 - pow(-2*t+2, 3)/2` | Suave nos dois lados |
| bounce | Segmentos parabólicos | Efeito de quicar |

Usar com Tweens: `tween.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)`.

## ⏸️ Hitstop (Freeze Frame) — Implementação Minimal

```gdscript
func hitstop(duration: float = 0.06) -> void:
    Engine.time_scale = 0.0
    await get_tree().create_timer(duration, true, false, true).timeout
    Engine.time_scale = 1.0
```
- Usar em impactos fortes (espada acertando inimigo, explosão).
- O `true` no 4º argumento garante que o timer rode mesmo com time_scale = 0.

