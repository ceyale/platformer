# Retro Platformer Engine

A custom 2D retro platformer built **from scratch** in Python using [Pygame-CE](https://pyga.me/). No high-level engines (Godot, Unity, etc.) — every system is hand-rolled for learning and total control.

## Project Structure

```
retro_platformer/
├── main.py                     # Entry point — bootstraps the game
├── requirements.txt            # Dependencies (pygame-ce)
├── README.md
├── assets/                     # Sprites, tile sets, sounds (future)
├── data/
│   └── levels/
│       ├── __init__.py
│       └── level_001.py        # Sample level data (40×15 grid)
└── src/
    ├── __init__.py
    ├── core/                   # Engine core
    │   ├── __init__.py
    │   ├── settings.py         # All configuration constants
    │   ├── game.py             # Delta-time game loop
    │   └── scene.py            # Scene system (GameplayScene, etc.)
    ├── entities/               # Entity hierarchy
    │   ├── __init__.py
    │   └── entity.py           # Base Entity class
    ├── input/                  # Input handling
    │   ├── __init__.py
    │   └── handler.py          # Action-mapped keyboard polling
    ├── rendering/              # Rendering pipeline
    │   ├── __init__.py
    │   └── camera.py           # Viewport / Camera with smooth follow
    ├── tilemap/                # Grid-based level system
    │   ├── __init__.py
    │   ├── tile.py             # Tile definition & registry
    │   ├── tileset.py          # Tile rendering (colours → surfaces)
    │   ├── constants.py        # Tile ID registration
    │   └── tilemap.py          # Tilemap class (grid, collision rects, draw)
    └── utils/                  # Shared utilities
        ├── __init__.py
        ├── math.py             # clamp, lerp, sign, approach, etc.
        └── aabb.py             # Custom AABB collision detection & resolution
```

## Architecture

### Delta-Time Game Loop (`src/core/game.py`)
- `pygame.time.Clock.tick_busy_loop()` for precise delta-time measurement in seconds.
- Framerate-independent physics — all velocities/accelerations multiplied by `dt`.
- Dual-resolution rendering: internal 320×240 pixel-art surface → scaled to 800×600 window.

### Physics & Kinematics (`src/core/scene.py` + `src/entities/entity.py`)
- Velocity, acceleration, gravity, and friction applied per-frame with `dt`.
- Player input drives acceleration; friction decelerates when no input is held.
- Gravity pulls the player down; terminal velocity is clamped.
- **Custom collision resolution** coming in a later step (AABB system already written in `src/utils/aabb.py`).

### Collision Detection (`src/utils/aabb.py`)
- Pure AABB overlap tests — no Pygame sprite groups.
- `resolve_collision()` computes penetration depths and push-out normals.
- `resolve_collisions()` iterates over a list of solid rects and pushes the entity out on the shallowest axis per tile.

### Tilemap System (`src/tilemap/`)
- Level data is a 2D list of integer tile IDs (`data/levels/level_001.py`).
- `Tile` objects define properties (solid, one-way, color).
- `Tileset` pre-renders a cache of tile surfaces for fast drawing.
- `Tilemap.draw()` performs frustum culling — only tiles in the camera's viewport are rendered.
- `Tilemap.get_solid_rects_in_region()` returns world-space rects for physics queries.

### Camera (`src/rendering/camera.py`)
- Viewport with smooth (lerp-based) follow on a target entity.
- `camera.apply()` converts world-space rects → screen-space for rendering.

### Entity System (`src/entities/entity.py`)
- Base `Entity` class with position, velocity, size, `on_ground` flag.
- Clean `update(dt)` / `draw(surface, camera)` separation.

### Input (`src/input/handler.py`)
- Action-mapped keyboard polling (e.g. `is_action_pressed("jump")`).
- `just_pressed` / `just_released` detection for one-shot actions.
- Default bindings: arrows / WASD, Space / Up to jump.

## Controls

| Key       | Action             |
|-----------|--------------------|
| ← →       | Move left / right  |
| Space / ↑ | Jump               |
| ESC       | Quit               |
| F3        | Toggle debug HUD   |
| F4        | Toggle tile grid   |

## How to Run

```bash
cd retro_platformer
pip install -r requirements.txt
python main.py
```

## What's Next

This is **Step 2** of a multi-step build. Coming in later steps:
1. ✅ **Step 1** — Delta-time game loop + window setup
2. ✅ **Step 2** — Tilemap system + camera + entity scaffold + project structure
3. 🔜 **Step 3** — Full physics pipeline (gravity integration, AABB collision response)
4. 🔜 **Step 4** — Player controller (movement, jumping, wall-sliding, coyote time)
5. 🔜 **Step 5** — Enemies & hazards
6. 🔜 **Step 6** — Collectibles, scoring, UI
7. 🔜 **Step 7** — Particle effects, screen shake, audio
8. 🔜 **Step 8** — Polish, camera improvements, game feel