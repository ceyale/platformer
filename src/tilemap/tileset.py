"""
Tileset — the visual / rendering side of tiles.

A Tileset defines how each Tile ID is drawn: what colour, whether
to apply a border, a one-way arrow, etc.  For now everything uses
solid-colour rectangles; later this can be swapped for sprite-sheet
regions.
"""

import pygame

from src.core.settings import TILE_SIZE
from src.tilemap.tile import get_tile
from src.core.settings import (
    COLOR_BLACK,
    COLOR_WHITE,
    COLOR_GREEN,
    COLOR_BROWN,
    COLOR_GRAY,
    COLOR_MAGENTA,
)


class Tileset:
    """
    Renders tile IDs onto surfaces.

    Each tile ID maps to a cached pygame Surface (drawn once,
    reused every frame for performance).
    """

    def __init__(self) -> None:
        self._cache: dict[int, pygame.Surface] = {}
        self._build_cache()

    # ── Colour map: tile ID → (fill_colour, border_colour, flags) ──────

    @staticmethod
    def _lookup_color(tile_id: int) -> tuple[int, int, int]:
        """Return the fill colour for a given tile ID."""
        palette: dict[int, tuple[int, int, int]] = {
            0: (0, 0, 0, 0),          # air → transparent
            1: COLOR_BROWN,            # dirt
            2: COLOR_GREEN,            # grass
            3: COLOR_GRAY,             # stone
            4: (180, 100, 60),         # brick
            5: (200, 200, 100),        # platform
        }
        return palette.get(tile_id, COLOR_MAGENTA)

    def _build_cache(self) -> None:
        """Pre-render a surface for every registered tile ID."""
        from src.tilemap.tile import TILE_REGISTRY

        for tile_id in TILE_REGISTRY:
            self._render_tile(tile_id)

        # Always include air (ID 0) and a fallback
        for tid in (0, 99):
            if tid not in self._cache:
                self._render_tile(tid)

    def _render_tile(self, tile_id: int) -> None:
        """Create and cache a small surface for *tile_id*."""
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        tile = get_tile(tile_id)
        color = self._lookup_color(tile_id) if tile is None else tile.color

        # Fill
        if tile_id == 0:  # air — fully transparent
            surf.fill((0, 0, 0, 0))
        else:
            surf.fill(color)
            # Thin border for visual clarity
            pygame.draw.rect(surf, COLOR_BLACK, surf.get_rect(), 1)

        self._cache[tile_id] = surf

    def get_surface(self, tile_id: int) -> pygame.Surface:
        """Return the cached surface for *tile_id* (or a magenta fallback)."""
        surf = self._cache.get(tile_id)
        if surf is not None:
            return surf
        # Generate on-the-fly fallback
        self._render_tile(tile_id)
        return self._cache.get(tile_id, self._cache.get(99))