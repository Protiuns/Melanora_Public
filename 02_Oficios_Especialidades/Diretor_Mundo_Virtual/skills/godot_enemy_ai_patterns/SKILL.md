---
name: Godot Enemy AI Patterns
description: Catálogo de padrões de IA para inimigos, incluindo FSMs, comportamentos reativos e integração com componentes do Studio.
---

# 🤖 Godot Enemy AI Patterns (v1.0)

Esta skill documenta padrões de IA reutilizáveis para inimigos, garantindo comportamentos consistentes e configuráveis.

## 📊 Padrões Disponíveis

| Padrão | Complexidade | Componente Base | Uso |
|--------|--------------|-----------------|-----|
| Chase | ⭐ | ChaseAI2D/3D | Perseguição direta |
| FSM Modular | ⭐⭐ | StudioAIFiniteStateMachine | Comportamentos complexos e desacoplados |
| Steering | ⭐⭐⭐ | SteeringAgent2D | Movimento orgânico (Seek, Flee, Wander) |

---

## 📦 Componentes Vinculados (Registry)
- `ai_fsm_controller`: Controlador central de estados.
- `ai_state_idle`: Comportamento de espera.
- `ai_state_patrol_2d`: Patrulha horizontal com sensores.
- `ai_state_chase_2d`: Perseguição modular 2D.
- `steering_agent_2d`: Perseguição/Fuga orgânica (forças vetoriais).
- `ai_state_chase_3d`: Perseguição modular 3D (Navigation).
- `chase_ai_2d/3d`: Versões simplificadas (sem FSM).
- `detection_area_2d`: Gatilho visual para a IA.

---

## 🏗️ Hierarquia de Cena Recomendada (Inimigo com FSM)

1. `CharacterBody2D` (Script: `PukGreedSlime.gd`)
   - `Visuals` (AnimatedSprite/Mesh)
   - `CollisionShape2D`
   - `StudioHealthComponent` (Vida)
   - `StudioAIFiniteStateMachine` (Controle)
     - `StudioAIStateIdle` (Child: "idle")
     - `StudioAIStatePatrol2D` (Child: "patrol")
     - `StudioAIStateChase2D` (Child: "chase")
   - `StudioDetectionArea2D` (Sensor)

---

## 🎯 Padrão 1: Chase (Perseguição)

### Componentes Utilizados
- `StudioChaseAI2D` ou `StudioChaseAI3D`
- `StudioHealthComponent`
- `StudioDamageArea2D/3D`

### Configuração Típica
```gdscript
# No Inspector ou via código
chase_ai.chase_speed = 4.0
chase_ai.detection_range = 10.0
chase_ai.stop_distance = 1.5
chase_ai.target_group = "player"
```

### Comportamento
1. Procura alvo no grupo configurado
2. Se distância ≤ detection_range → persegue
3. Se distância ≤ stop_distance → emite `target_reached` (atacar)
4. Se distância > detection_range × 1.5 → emite `target_lost` (para)

### Integração com Ataque
```gdscript
func _ready():
    $ChaseAI.target_reached.connect(_on_reached_player)

func _on_reached_player():
    $DamageArea.monitoring = true
    await get_tree().create_timer(0.5).timeout
    $DamageArea.monitoring = false
```

---

## 🔄 Padrão 2: Patrol → Chase

### Estado: Patrol (Ronda)
```gdscript
var patrol_points: Array[Vector3] = []
var current_point: int = 0

func _patrol_logic(delta):
    if patrol_points.is_empty():
        return
    
    var target = patrol_points[current_point]
    var direction = (target - global_position).normalized()
    direction.y = 0
    
    velocity.x = direction.x * patrol_speed
    velocity.z = direction.z * patrol_speed
    
    if global_position.distance_to(target) < 1.0:
        current_point = (current_point + 1) % patrol_points.size()
```

### Transição para Chase
```gdscript
enum State { PATROL, CHASE, RETURN }
var state = State.PATROL

func _physics_process(delta):
    var dist_to_player = global_position.distance_to(player.global_position)
    
    match state:
        State.PATROL:
            if dist_to_player < detection_range:
                state = State.CHASE
            else:
                _patrol_logic(delta)
        
        State.CHASE:
            if dist_to_player > detection_range * 2:
                state = State.RETURN
            else:
                _chase_logic(delta)
        
        State.RETURN:
            # Volta ao patrol point mais próximo
            _return_to_patrol()
```

---

## 🧠 Padrão 3: Steering Behaviors (Movimento Orgânico)
Para inimigos que precisam se mover "como vivos" e não em linhas retas robóticas. Baseado em forças (Reynolds).

### Componente: `SteeringAgent2D`
Calcula vetores de velocidade baseados em comportamentos desejados.

```gdscript
# No State de Movimento (ex: Chase)
func physics_update(delta):
    var steering = actor.get_node("SteeringAgent2D")
    
    # SEEK (Perseguir suavemente)
    var force = steering.seek(player.global_position)
    
    # FLEE (Fugir suavemente)
    # var force = steering.flee(player.global_position)
    
    # WANDER (Vagar aleatoriamente)
    # var force = steering.wander()
    
    # Aplicar força ao ator
    actor.velocity += force * delta
    actor.move_and_slide()
```

---

## 🏃 Padrão 3: Flee (Fuga)

### Lógica Invertida
```gdscript
func _flee_logic(delta):
    var away_dir = (global_position - player.global_position).normalized()
    away_dir.y = 0
    
    velocity.x = away_dir.x * flee_speed
    velocity.z = away_dir.z * flee_speed
    
    move_and_slide()
```

### Trigger de Fuga
```gdscript
# Fugir quando HP baixo
func _on_health_changed(current, max_hp):
    if current < max_hp * 0.3:
        state = State.FLEE
```

---

## 🛡️ Padrão 4: Guard (Guarda)

### Comportamento
1. Fica parado em posição inicial
2. Se jogador entra na área → persegue
3. Se jogador sai da área OU distância > leash_range → retorna

```gdscript
@export var guard_position: Vector3
@export var guard_radius: float = 5.0
@export var leash_range: float = 10.0

func _guard_logic():
    var dist_from_post = global_position.distance_to(guard_position)
    var dist_to_player = global_position.distance_to(player.global_position)
    
    if dist_from_post > leash_range:
        # Retornar ao posto
        _return_to(guard_position)
    elif dist_to_player < guard_radius:
        # Perseguir intruso
        _chase_logic()
    else:
        # Ficar parado
        velocity = Vector3.ZERO
```

---

## 📋 Checklist de Implementação de Inimigo

1. [ ] CharacterBody2D/3D com grupo "enemy"
2. [ ] HealthComponent anexado
3. [ ] Componente de IA apropriado (Chase, Patrol, etc.)
4. [ ] DamageArea para causar dano ao jogador
5. [ ] Conectar `health_depleted` a função de morte
6. [ ] Visual feedback (animação, cor) nos estados

---

## 🔗 Integração com Sistema

### Morte do Inimigo
```gdscript
func _on_death():
    # Notificar sistema global
    if SignalBus:
        SignalBus.entity_died.emit(self, "enemy")
    
    # Efeitos visuais aqui (partículas, som)
    queue_free()
```

### Registro de Kill (via GameManager)
```gdscript
# No script do nível ou GameManager
func _ready():
    SignalBus.entity_died.connect(_on_entity_died)

func _on_entity_died(entity, type):
    if type == "enemy":
        GameManager.add_score(100)
```

---

## 🧭 Padrão 5: Pathfinding Inteligente

### Quando Usar Cada Ferramenta

| Cenário | Ferramenta | Vantagem |
|---------|-----------|----------|
| Grid fixo (tilemap) | `AStarGrid2D` | Simples, direto, grid-based |
| Movimento livre | `NavigationAgent2D` | Desvio dinâmico (RVO) |
| Híbrido | Ambos | AStar para rota, NavAgent para execução |

### AStarGrid2D (Grid-Based)
Perfeito para dungeons baseadas em TileMap:
```gdscript
var astar = AStarGrid2D.new()
astar.region = Rect2i(0, 0, grid_w, grid_h)
astar.cell_size = Vector2(16, 16)
astar.update()

# Marcar paredes do TileMap como sólidas
for cell in tilemap.get_used_cells():
    var data = tilemap.get_cell_tile_data(cell)
    if data and data.get_custom_data("is_wall"):
        astar.set_point_solid(cell, true)

# Calcular caminho
var path = astar.get_id_path(enemy_cell, player_cell)
```

### NavigationAgent2D (Mesh-Based com Desvio)
Para inimigos que precisam desviar de outros inimigos em tempo real:
```gdscript
@onready var nav: NavigationAgent2D = $NavigationAgent2D

func chase_player(player_pos: Vector2) -> void:
    nav.target_position = player_pos

func _physics_process(_delta: float) -> void:
    if nav.is_navigation_finished():
        return
    var next = nav.get_next_path_position()
    velocity = (next - global_position).normalized() * speed
    move_and_slide()
```

### Integração com FSM
No estado `CHASE`, substituir perseguição direta por pathfinding:
```gdscript
# State: Chase (com pathfinding)
func physics_update(delta):
    if not player: return
    nav_agent.target_position = player.global_position
    if not nav_agent.is_navigation_finished():
        var next = nav_agent.get_next_path_position()
        actor.velocity = (next - actor.global_position).normalized() * chase_speed
    actor.move_and_slide()
```
