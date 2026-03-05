# ⚙️ Mechanics & Patterns Library
*Reference for "Deep Dive" and Implementation Details*

## 1. Core Action Mechanics (The "Feel")
### Movement
*   **Coyote Time**: Allow jumping 0.1s after leaving a platform.
    *   *Godot*: Check `!is_on_floor()` and `timer < coyote_time`.
*   **Jump Buffer**: Queue jump input 0.1s before hitting ground.
    *   *Godot*: Store `jump_pressed_time` timestamp.
*   **Dash/Dodge**: Temporary high velocity + Invincibility Frames (i-frames).
    *   *Godot*: `velocity = dir * dash_speed`, disable `CollisionShape` or boolean `is_invincible`.
*   **Top-Down Movement**: 8-way movement with normalization.
    *   *Godot*: `input_vector.normalized()` to prevent fast diagonals.

### Combat
*   **Hitstop (Freeze Frame)**: Pause game for 0.05-0.1s on impact.
    *   *Godot*: `Engine.time_scale = 0.0` -> Timer -> `Engine.time_scale = 1.0`.
*   **Knockback**: Apply impulse opposite to damage source.
    *   *Godot*: `velocity = (global_position - enemy.global_position).normalized() * knockback_force`.
*   **Invulnerability (Mercy) Frames**: Flashing sprite after taking damage.
    *   *Godot*: `Timer` + `AnimationPlayer` (blink visibility).

## 2. Adventure & Puzzle Patterns (Zelda-Like)
### Gated Progression (Lock & Key)
*   **Item Gates**: Obstacles only removable by specific items.
    *   *Ex*: Bushes (Sword), Cracks (Bomb), Gaps (Hookshot).
*   **Backtracking**: Returning to old areas with new powers.
*   **Dungeon Structure**: Hub -> Puzzle Rooms -> Mini-Boss (Item) -> Boss Key -> Boss.

### Interaction
*   **Push Blocks**: Grid-based or Physics-based objects.
    *   *Godot*: `CharacterBody2D` pushing `RigidBody2D` (freeze rotation) or Raycast checks.
*   **Switches**: Toggle state (Crystal Switch, Floor Plate).
    *   *Godot*: Signals `toggled(bool)` to linked doors/bridges.
*   **Destructibles**: Grass/Pots that drop loot.
    *   *Godot*: `Area2D` that plays animation -> instantiates `LootDrop` -> `queue_free()`.

## 3. Systems & Economy
### Stats (RPG)
*   **Health**: Hearts (integers) or Bar (float).
*   **Mana/Stamina**: Regenerating resource for actions.
*   **Progression**: Heart Containers (Max HP Up) vs Stat Points.

### Inventory
*   **Passive**: Persistent upgrades (Double Jump, Swim).
*   **Active**: Equippable items (Sword, Bow, Potion).
*   **Wallet**: Currency caps (99, 255, 999) to force spending.

## 4. Game Feel Patterns (Juice)
*   **Screenshake**: Random offset to Camera during impacts.
*   **Particles**: Dust on jump, sparks on hit, debris on death.
*   **Sfx Variation**: Random pitch (0.9 - 1.1) on repetitive sounds (footsteps, hits).
