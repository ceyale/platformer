"""
Game-wide configuration constants.

Every tunable value lives here so the rest of the engine stays
clean and data-driven.  No game logic — just constants.
"""

import pygame

# ── Display ──────────────────────────────────────────────────────────────
WINDOW_TITLE = "Retro Platformer"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS_CAP = 60                     # target framerate
VSYNC = 1                        # 0 = off, 1 = on

# Logical (pixel-art) resolution — everything is rendered at this
# size then scaled to the window for a crisp retro look.
GAME_WIDTH = 320
GAME_HEIGHT = 240

# ── Colours (RGB tuples) ─────────────────────────────────────────────────
COLOR_BLACK   = (0,   0,   0)
COLOR_WHITE   = (255, 255, 255)
COLOR_RED     = (255, 0,   0)
COLOR_GREEN   = (0,   255, 0)
COLOR_BLUE    = (0,   0,   255)
COLOR_CYAN    = (0,   255, 255)
COLOR_MAGENTA = (255, 0,   255)
COLOR_YELLOW  = (255, 255, 0)
COLOR_GRAY    = (128, 128, 128)
COLOR_BROWN   = (139, 69,  19)

# Background / sky
SKY_COLOR = (100, 150, 255)

# ── Tilemap ──────────────────────────────────────────────────────────────
TILE_SIZE = 16                    # pixel size of one tile in game-world
MAP_COLS_DEFAULT = 20             # 20 * 16 = 320 px = GAME_WIDTH
MAP_ROWS_DEFAULT = 15             # 15 * 16 = 240 px = GAME_HEIGHT

# Tile IDs (matching what Tileset defines)
TILE_AIR    = 0
TILE_DIRT   = 1
TILE_GRASS  = 2
TILE_STONE  = 3
TILE_BRICK  = 4
TILE_PLATFORM = 5                # one-way platform (pass-through from below)

# ── Physics (world units = pixels) ───────────────────────────────────────
GRAVITY = 980.0                   # px / s²
MAX_FALL_SPEED = 600.0            # terminal velocity
PLAYER_ACCELERATION = 500.0       # horizontal accel px/s²
PLAYER_MAX_SPEED = 250.0          # horizontal max speed px/s
PLAYER_FRICTION = 0.85            # multiplier per second (applied per frame via pow)
PLAYER_JUMP_VELOCITY = -350.0     # initial upward velocity (negative = up)

# ── Camera ───────────────────────────────────────────────────────────────
CAMERA_LERP_SPEED = 8.0           # smooth camera follow (higher = snappier)
CAMERA_DEAD_ZONE_X = 0.3          # fraction of screen width before camera moves
CAMERA_DEAD_ZONE_Y = 0.3          # fraction of screen height

# ── Dev helpers ──────────────────────────────────────────────────────────
SHOW_DEBUG_OVERLAY = False        # toggled with F3
SHOW_TILE_GRID = False            # toggled with F4