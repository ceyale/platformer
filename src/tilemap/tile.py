"""
Tile — the smallest unit in the tilemap grid.

Each tile is identified by an integer ID.  The Tile definition holds
the ID, a collision flag, a pass-through flag (for one-way platforms),
and metadata that the tileset renderer uses to decide what colour / glyph
to draw.
"""

from typing import Optional


class Tile:
    """Immutable definition of a single tile type."""

    __slots__ = ("id", "name", "solid", "one_way", "color")

    def __init__(
        self,
        tile_id: int,
        name: str = "",
        solid: bool = True,
        one_way: bool = False,
        color: tuple[int, int, int] = (255, 0, 255),
    ) -> None:
        self.id = tile_id
        self.name = name
        self.solid = solid          # blocks movement
        self.one_way = one_way      # pass-through from below only
        self.color = color

    def __repr__(self) -> str:
        return f"Tile({self.id}: {self.name})"


# ── Pre-defined tile registry ──────────────────────────────────────────
# Maps tile ID → Tile for quick lookup.
TILE_REGISTRY: dict[int, Tile] = {}


def register_tile(tile: Tile) -> None:
    """Add a tile to the global registry."""
    TILE_REGISTRY[tile.id] = tile


def get_tile(tile_id: int) -> Optional[Tile]:
    """Look up a tile by ID; returns None for unknown IDs."""
    return TILE_REGISTRY.get(tile_id)