"""
Tilemap — the grid-based level representation.

A Tilemap holds a 2D array of tile IDs, knows its dimensions in
tiles and pixels, and can render visible tiles to a surface
(camera-aware) or return collision rectangles for physics.
"""

from typing import Optional

import pygame

from src.core.settings import TILE_SIZE
from src.tilemap.tile import get_tile
from src.tilemap.tileset import Tileset
from src.rendering.camera import Camera


class Tilemap:
    """
    Grid-based level data.

    The grid is stored as a list of lists: ``grid[row][col]``.
    Row 0 is the top of the map.
    """

    def __init__(
        self,
        grid: list[list[int]],
        tileset: Optional[Tileset] = None,
    ) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

        self.tileset = tileset or Tileset()

    # ── Dimensions ───────────────────────────────────────────────────────

    @property
    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    @property
    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE

    # ── Tile access ──────────────────────────────────────────────────────

    def get_tile_id(self, col: int, row: int) -> int:
        """Return the tile ID at grid position (col, row)."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return 0  # out-of-bounds → air

    def set_tile_id(self, col: int, row: int, tile_id: int) -> None:
        """Set the tile ID at grid position (col, row)."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = tile_id

    def is_solid(self, col: int, row: int) -> bool:
        """Is the tile at (col, row) solid (blocks movement)?"""
        tile = get_tile(self.get_tile_id(col, row))
        return tile is not None and tile.solid

    def is_one_way(self, col: int, row: int) -> bool:
        """Is the tile at (col, row) a one-way platform?"""
        tile = get_tile(self.get_tile_id(col, row))
        return tile is not None and tile.one_way

    # ── World-space helpers ──────────────────────────────────────────────

    @staticmethod
    def tile_to_world(col: int, row: int) -> tuple[float, float]:
        """Return the top-left pixel coordinate of tile (col, row)."""
        return (col * TILE_SIZE, row * TILE_SIZE)

    @staticmethod
    def world_to_tile(x: float, y: float) -> tuple[int, int]:
        """Return the (col, row) of the tile containing world point (x, y)."""
        return (int(x // TILE_SIZE), int(y // TILE_SIZE))

    # ── Collision rects ──────────────────────────────────────────────────

    def get_solid_rects_in_region(
        self, region: pygame.Rect
    ) -> list[pygame.Rect]:
        """
        Return a list of world-space pygame.Rects for every solid tile
        that intersects *region*.  Used by the physics system.
        """
        rects: list[pygame.Rect] = []
        start_col = max(0, region.left // TILE_SIZE)
        end_col = min(self.cols - 1, region.right // TILE_SIZE)
        start_row = max(0, region.top // TILE_SIZE)
        end_row = min(self.rows - 1, region.bottom // TILE_SIZE)

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                if self.is_solid(col, row):
                    wx, wy = self.tile_to_world(col, row)
                    rects.append(pygame.Rect(wx, wy, TILE_SIZE, TILE_SIZE))

        return rects

    # ── Rendering ────────────────────────────────────────────────────────

    def draw(
        self,
        surface: pygame.Surface,
        camera: Camera,
        show_grid: bool = False,
    ) -> None:
        """
        Draw all visible tiles to *surface*, offset by the camera.

        Only tiles that intersect the camera's viewport are drawn
        (frustum culling).
        """
        cam = camera.rect

        # Tile-range visible in the viewport
        start_col = max(0, int(cam.left // TILE_SIZE))
        end_col = min(self.cols - 1, int(cam.right // TILE_SIZE))
        start_row = max(0, int(cam.top // TILE_SIZE))
        end_row = min(self.rows - 1, int(cam.bottom // TILE_SIZE))

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                tile_id = self.grid[row][col]
                if tile_id == 0:
                    continue  # skip air

                wx, wy = self.tile_to_world(col, row)
                screen_x = wx - camera.x
                screen_y = wy - camera.y

                tile_surf = self.tileset.get_surface(tile_id)
                surface.blit(tile_surf, (screen_x, screen_y))

                # Optional grid overlay
                if show_grid:
                    pygame.draw.rect(
                        surface,
                        (255, 255, 255, 60),
                        (screen_x, screen_y, TILE_SIZE, TILE_SIZE),
                        1,
                    )