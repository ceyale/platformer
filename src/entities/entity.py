"""
Base Entity — the foundation for every object in the game world.

Entities have position, velocity, size, and follow the standard
update/draw contract.  The physics component is separate so it
can be shared / composed.
"""

from typing import Optional

import pygame

from src.rendering.camera import Camera
from src.core.settings import TILE_SIZE


class Entity:
    """
    Base class for all in-world objects (player, enemies, items).

    Attributes
    ----------
    x, y : float
        World-space position (top-left corner).
    width, height : float
        Bounding-box dimensions.
    vx, vy : float
        Velocity in pixels / second.
    """

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        width: float = TILE_SIZE,
        height: float = TILE_SIZE,
    ) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height

        # Velocity (pixels / second)
        self.vx: float = 0.0
        self.vy: float = 0.0

        # Acceleration (pixels / s²) — applied by physics or input
        self.ax: float = 0.0
        self.ay: float = 0.0

        # State flags
        self.on_ground: bool = False
        self.active: bool = True

    # ── Derived helpers ─────────────────────────────────────────────────

    @property
    def rect(self) -> pygame.Rect:
        """World-space bounding rect (integer coords for Pygame)."""
        return pygame.Rect(
            int(self.x), int(self.y),
            int(self.width), int(self.height),
        )

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2.0

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2.0

    @property
    def position(self) -> tuple[float, float]:
        return (self.x, self.y)

    @position.setter
    def position(self, value: tuple[float, float]) -> None:
        self.x, self.y = value

    # ── Entity API ──────────────────────────────────────────────────────

    def update(self, dt: float) -> None:
        """
        Called every frame.  Subclasses override to add behaviour.

        Base implementation applies acceleration → velocity → position.
        """
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        """
        Called every frame.  Subclasses override to render themselves.
        The base class draws a simple coloured rectangle placeholder.
        """
        screen_rect = camera.apply(self.rect)
        pygame.draw.rect(surface, (255, 255, 255), screen_rect)