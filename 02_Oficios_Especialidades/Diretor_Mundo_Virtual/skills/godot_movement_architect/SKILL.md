---
name: Godot Movement Architect
description: Especialista em arquitetura de movimento modular para Godot 4. Define padrões de MotionProfiles, Drivers e InputBrokers para garantir desacoplamento e portabilidade entre jogos 2D e 3D.
---

# 🚀 Godot Movement Architect (v1.0)

Esta skill define os padrões para a criação de sistemas de movimento modulares no Studio Puk 97. O objetivo é remover a lógica de física dos atores principais (Player/Enemy) e delegá-la para componentes especializados.

## 🏗️ A Tríade de Movimento

A movimentação é dividida em três pilares:

1.  **MotionProfile (Recurso)**: Contém apenas os dados numéricos (velocidade, pulo, fricção).
2.  **MovementDriver (Lógica)**: Processa a física baseada no perfil e no input.
3.  **InputBroker (Controle)**: Traduz teclas, cliques ou IA em vetores de comando.

---

## 📂 Estrutura de Arquivos (studio_library/logic/)

- `motion_profile.gd`: Classe base `Resource` para configurações.
- `movement_driver.gd`: Classe base `Node` para processamento de física.
- `platformer_driver_2d.gd`: Driver especializado para jogos de plataforma 2D.
- `topdown_driver_2d.gd`: Driver para movimento top-down ou point & click.
- `fps_driver_3d.gd`: Driver para movimentação de primeira pessoa.

---

## 🛠️ Padrão de Implementação

### 1. MotionProfile
Deve ser um `Resource` para permitir a criação de múltiplos perfis (ex: `bruxa_agil.tres`, `guerreiro_pesado.tres`).

```gdscript
class_name StudioMotionProfile
extends Resource

@export_group("Horizontal")
@export var speed: float = 200.0
@export var acceleration: float = 1000.0
@export var friction: float = 1200.0

@export_group("Vertical")
@export var gravity: float = 980.0
@export var jump_velocity: float = -400.0
@export var terminal_velocity: float = 1000.0
```

### 2. MovementDriver
O Driver deve receber o input e aplicar a velocidade ao pai (`CharacterBody`).

```gdscript
class_name StudioMovementDriver
extends Node

@export var profile: StudioMotionProfile
@onready var actor: CharacterBody2D = get_parent()

func apply_movement(input_dir: Vector2, delta: float):
    # Lógica de processamento de velocidade aqui
    pass
```

### 3. Integração com Juice/VFX
Os Drivers DEVEM emitir sinais para que o `VFXDispatcher` ou `SquashStretchComponent` reajam.
- `jumped`
- `landed`
- `started_moving`
- `stopped_moving`

### 4. Habilidades Modulares (Abilities)
Para mecânicas complexas (Dash, WallJump, Glide), use nós filhos que estendem `StudioMovementAbility`.
- `MovementAbility`: Classe base com cooldown e duração.
- `AbilityDash`: Implementação agnóstica de 2D/3D.

---

## 📦 Componentes Vinculados (Registry)
- `motion_profile`: Recurso de dados para ajuste fino de movimento.
- `platformer_driver_2d`: Lógica de física de plataforma (Coyote/Buffer).
- `platformer_driver_3d`: Lógica de física de plataforma 3D (SpringArm support).
- `topdown_driver_2d`: Lógica de movimento top-down e point & click.
- `fps_driver_3d`: Câmera e física FPS 3D.
- `ability_dash`: Habilidade modular de dash.
- `squash_stretch_component`: Feedback visual de movimento (Squash/Stretch).

---

## 🏗️ Hierarquia de Cena Recomendada (Platformer 2D)

1. `CharacterBody2D` (Raiz com Script do Ator)
   - `Visuals` (Sprites/Animations)
     - `StudioSquashStretchComponent` (Linkado aos sinais do Driver)
   - `CollisionShape2D`
   - `StudioPlatformerDriver2D` (Contém o `MotionProfile`)

---

## 📝 Protocolo de Evolução Técnica
1.  **Analise o Movimento Atual**: Antes de criar um Driver, verifique se a lógica de aceleração/fricção já existe no projeto local.
2.  **Extraia para a Library**: Mova a lógica genérica para a `studio_library`.
3.  **Use Recursos**: Nunca coloque valores fixos ("magic numbers") no código do Driver; use sempre o `MotionProfile`.
4.  **Desacoplamento**: O Driver não deve saber quem é o Player, ele apenas move o `get_parent()`.
