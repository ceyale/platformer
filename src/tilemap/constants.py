"""
Tile ID constants and automatic tile registration.

Import this module to populate the tile registry with every
standard tile type used by the engine.
"""

from src.core.settings import (
    TILE_AIR,
    TILE_DIRT,
    TILE_GRASS,
    TILE_STONE,
    TILE_BRICK,
    TILE_PLATFORM,
    COLOR_BROWN,
    COLOR_GREEN,
    COLOR_GRAY,
)
from src.tilemap.tile import Tile, register_tile

# ── Register all standard tiles ─────────────────────────────────────────

register_tile(Tile(
    tile_id=TILE_AIR,
    name="Air",
    solid=False,
    color=(0, 0, 0, 0),
))

register_tile(Tile(
    tile_id=TILE_DIRT,
    name="Dirt",
    solid=True,
    color=COLOR_BROWN,
))

register_tile(Tile(
    tile_id=TILE_GRASS,
    name="Grass",
    solid=True,
    color=COLOR_GREEN,
))

register_tile(Tile(
    tile_id=TILE_STONE,
    name="Stone",
    solid=True,
    color=COLOR_GRAY,
))

register_tile(Tile(
    tile_id=TILE_BRICK,
    name="Brick",
    solid=True,
    color=(180, 100, 60),
))

register_tile(Tile(
    tile_id=TILE_PLATFORM,
    name="Platform",
    solid=True,
    one_way=True,
    color=(200, 200, 100),
))