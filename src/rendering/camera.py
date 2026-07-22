"""
Camera / Viewport — controls which portion of the world is visible.

The camera tracks a target entity (typically the player) with
optional dead-zone and smooth lerp interpolation.
"""

import pygame

from src.core.settings import (
    GAME_WIDTH,
    GAME_HEIGHT,
    CAMERA_LERP_SPEED,
)


class Camera:
    """
    A viewport into the game world.

    The camera has a position (top-left of the view) in world
    coordinates.  All world-space entities offset their draw
    position by ``-camera.x, -camera.y``.
    """

    def __init__(
        self,
        width: int = GAME_WIDTH,
        height: int = GAME_HEIGHT,
    ) -> None:
        self.width = width
        self.height = height
        self.x: float = 0.0
        self.y: float = 0.0

        # Smooth follow target
        self._target_x: float = 0.0
        self._target_y: float = 0.0

    # ── Properties ───────────────────────────────────────────────────────

    @property
    def rect(self) -> pygame.Rect:
        """Viewport rect in world-space coordinates."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # ── Follow ───────────────────────────────────────────────────────────

    def follow(self, target_rect: pygame.Rect) -> None:
        """
        Set the camera's desired position to center on *target_rect*.
        Call every frame before *update* to track a target.
        """
        self._target_x = target_rect.centerx - self.width // 2
        self._target_y = target_rect.centery - self.height // 2

    def follow_snap(self, target_rect: pygame.Rect) -> None:
        """
        Instantly snap the camera to centre on *target_rect*
        (no smooth interpolation).
        """
        self.x = target_rect.centerx - self.width // 2
        self.y = target_rect.centery - self.height // 2
        self._target_x = self.x
        self._target_y = self.y

    def update(self, dt: float) -> None:
        """
        Smoothly interpolate the camera toward its target position
        using exponential ease (framerate-independent).
        """
        # Exponential ease: factor approaches 1.0 over time.
        # Clamp the base to avoid complex numbers from pow(negative, dt).
        raw_base = 1.0 - CAMERA_LERP_SPEED * dt
        base = max(0.0, raw_base)
        lerp_factor = 1.0 - pow(base, dt)
        lerp_factor = max(0.0, min(1.0, lerp_factor))

        self.x += (self._target_x - self.x) * lerp_factor
        self.y += (self._target_y - self.y) * lerp_factor

    def apply(self, world_rect: pygame.Rect) -> pygame.Rect:
        """
        Convert a world-space rect to screen-space by subtracting
        the camera offset.
        """
        return world_rect.move(-self.x, -self.y)

    def apply_point(self, point: tuple[float, float]) -> tuple[float, float]:
        """Convert a world-space point to screen-space."""
        return (point[0] - self.x, point[1] - self.y)

    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """Alias for *apply*."""
        return self.apply(rect)