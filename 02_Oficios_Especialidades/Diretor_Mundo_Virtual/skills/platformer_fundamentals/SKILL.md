---
name: Platformer Fundamentals
description: Core 2D physics loop, gravity implementation, and axis-restricted movement in Godot 4.
---

# Platformer Fundamentals

A base de qualquer plataforma 2D é a restrição de movimento aos eixos X (horizontal) e Y (vertical), simulando um plano bidimensional.

## O Ciclo da Física (Physics Loop)

No Godot 4, o movimento é processado no `_physics_process(delta)`. A lógica fundamental segue esta ordem:
1. **Verificar Chão**: Detectar se o personagem está tocando uma superfície.
2. **Aplicar Gravidade**: Se não estiver no chão, aplicar força para baixo.
3. **Processar Input**: Ler comandos de direção e pulo.
4. **Mover e Deslizar**: Executar o movimento tratando colisões.

### Implementação Básica (GDScript)

```gdscript
extends CharacterBody2D

@export var speed = 300.0
@export var gravity = 980.0

func _physics_process(delta: float) -> void:
    # 1. Aplicar Gravidade
    if not is_on_floor():
        velocity.y += gravity * delta
    
    # 2. Movimento Lateral
    var direction := Input.get_axis("ui_left", "ui_right")
    if direction:
        velocity.x = direction * speed
    else:
        velocity.x = move_toward(velocity.x, 0, speed)

    # 3. Executar Movimento
    move_and_slide()
```

## Comparação de Modelos de Física

| Característica | Modelo "Floaty" (Mario) | Modelo "Snappy" (Hollow Knight) |
| :--- | :--- | :--- |
| **Aceleração** | Gradual (inércia alta) | Instantânea (pára e corre na hora) |
| **Gravidade** | Baixa no topo do pulo | Constante e forte |
| **Game Feel** | Fluidez e peso | Precisão e controle total |

## Dicas de Implementação
- **Scale & Gravity**: Ajuste a gravidade no `Project Settings` ou via código para que o pulo não pareça "lunar". 
- **Delta**: Sempre multiplique a gravidade por `delta` para manter a consistência independente do FPS.
- **Layers & Masks**: Use `Collision Layers` (quem eu sou) e `Masks` (com quem eu colido) para otimizar a física.
