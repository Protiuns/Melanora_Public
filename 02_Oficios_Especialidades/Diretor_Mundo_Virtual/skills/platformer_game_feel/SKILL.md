---
name: Platformer Game Feel (Juice)
description: Enhancing player feedback using hitstop, squash & stretch, and visual/audio cues.
---

# Platformer Game Feel (Juice)

"Juice" é o feedback que faz o jogo parecer vivo. Pequenos detalhes visuais e temporais dão peso e satisfação às ações simples como pular e bater.

## Squash & Stretch (Esmagar e Esticar)

Alterar a escala do sprite dinamicamente durante o movimento.
- **Pulo**: Esticar no eixo Y (ex: 0.8, 1.2).
- **Pouso**: Achatar no eixo Y (ex: 1.3, 0.7).

### Implementação (Godot 4)

```gdscript
@onready var sprite = $Sprite2D
@export var return_speed = 10.0
@export var stretch_scale = Vector2(0.8, 1.2)
@export var squash_scale = Vector2(1.2, 0.8)

func _process(delta):
    # Retornar escala ao normal gradualmente
    sprite.scale = sprite.scale.lerp(Vector2(1, 1), delta * return_speed)

func apply_stretch():
    sprite.scale = stretch_scale

func apply_squash():
    sprite.scale = squash_scale
```

## Hitstop (Freeze Frame)

Pausar o tempo por frações de segundo para enfatizar um impacto.

```gdscript
func hitstop(duration: float):
    Engine.time_scale = 0.0
    await get_tree().create_timer(duration, true, false, true).timeout
    Engine.time_scale = 1.0
```
*Dica: O segundo argumento `true` no Timer permite que ele ignore o `time_scale = 0`.*

## Checkbox do Game Feel

| Elemento | Efeito | Onde aplicar? |
| :--- | :--- | :--- |
| **Screenshake** | Tremor de câmera | Explosões, dano, quedas altas. |
| **Partículas** | Poeira no chão | Pulo e pouso (Landing dust). |
| **SFX** | Sons variados | Passos (metal vs grama), impacto. |
| **Luz/Flash** | Flash branco no sprite | Ao receber dano. |

## Comparação: "Dry" vs "Juicy"
- **Dry**: O personagem encosta no inimigo e o inimigo some instantaneamente.
- **Juicy**: O jogo pausa por 0.05s, a tela treme levemente, o inimigo explode em partículas e um som de impacto satisfatório toca.
