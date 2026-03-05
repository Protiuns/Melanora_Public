---
name: Platformer Movement Logic
description: Advanced jumping mechanics, variable jump height, and horizontal movement refinement.
---

# Platformer Movement Logic

Refinar a movimentação é o que separa um protótipo de um jogo profissional. O foco aqui é o controle do jogador sobre o pulo e a inércia.

## Pulo Variável (Variable Jump Height)

Jogadores esperam que, ao soltar o botão de pulo cedo, o personagem pare de subir. Isso dá mais controle para pulos curtos e precisos.

### Código de Exemplo (Godot 4)

```gdscript
@export var jump_velocity = -400.0
@export var jump_release_force = 0.5 # Reduz velocidade vertical pela metade

func _physics_process(delta: float) -> void:
    # Iniciar Pulo
    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = jump_velocity
        
    # Pulo Variável: Se soltar o botão enquanto sobe, corta a subida
    if Input.is_action_just_released("ui_accept") and velocity.y < 0:
        velocity.y *= jump_release_force
```

## Aceleração e Atrito (Inércia)

Mover-se instantaneamente (`velocity.x = SPEED`) pode parecer robótico. Usar `lerp` ou `move_toward` cria uma sensação de peso.

```gdscript
@export var speed = 300.0
@export var acceleration = 1200.0
@export var friction = 800.0

func apply_horizontal_movement(direction, delta):
    if direction != 0:
        velocity.x = move_toward(velocity.x, direction * speed, acceleration * delta)
    else:
        velocity.x = move_toward(velocity.x, 0, friction * delta)
```

## Comparação de Técnicas

| Técnica | O que faz? | Por que usar? |
| :--- | :--- | :--- |
| **Coyote Time** | Permite pular milissegundos após cair da plataforma. | Evita sensação de "o botão falhou" na borda. |
| **Jump Buffering** | Registra o pulo pouco antes de tocar o chão. | Torna o pulo imediato ao pousar, sem lag de input. |
| **Air Hang** | Reduz gravidade levemente no pico do pulo. | Cria um momento de "suspensão" estilo Celeste. |

## Dicas de Ouro
- **Jump Buffer**: Use um `Timer` de 0.1s para guardar o input de pulo.
- **Coyote Timer**: Inicie um `Timer` assim que `is_on_floor()` se tornar falso sem um pulo ativo.
