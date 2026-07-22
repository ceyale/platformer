"""
Scene — a discrete game state / screen.

Scenes encapsulate a full game mode (e.g. menu, gameplay, pause).
Every scene must implement:
  - handle_event(event)
  - update(dt)
  - draw(surface)

The Game loop delegates to whichever scene is currently active.
"""

from typing import Optional

import pygame

from src.rendering.camera import Camera
from src.tilemap.tilemap import Tilemap
from src.tilemap.tileset import Tileset
from src.entities.entity import Entity
from src.input.handler import InputHandler
from src.utils.aabb import resolve_collisions_f


class Scene:
    """Abstract base for all scenes."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single Pygame event."""
        pass

    def update(self, dt: float) -> None:
        """Update game logic for this scene."""
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Render this scene onto *surface*."""
        pass


class GameplayScene(Scene):
    """
    The main platformer gameplay scene.

    Owns the tilemap, camera, entities, input handler, and
    ties them all together each frame.
    """

    def __init__(self, tilemap: Tilemap) -> None:
        super().__init__()
        self.tilemap = tilemap
        self.camera = Camera()
        self.input = InputHandler()

        # ── Player entity ────────────────────────────────────────────────
        self.player = Entity(
            x=32.0,
            y=32.0,
            width=12,
            height=14,
        )
        # Snap camera to player on start
        self.camera.follow_snap(self.player.rect)

        # ── Additional entities ──────────────────────────────────────────
        self.entities: list[Entity] = []

    # ── Overrides ────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        """Let the input handler absorb key-down events for just-pressed checks."""
        pass  # InputHandler polls state, no per-event feeding needed

    def update(self, dt: float) -> None:
        # 1. Update input state
        self.input.update()

        # 2. Player input-driven forces (set velocity, not position yet)
        self._apply_player_input(dt)

        # 3. Apply gravity (integrate acceleration into velocity)
        self._apply_gravity(dt)

        # 4. Move the player on each axis SEPARATELY, resolving collisions
        #    per-axis to get proper wall-sliding and ground landing.
        self._move_and_collide(dt)

        # 5. Update all other entities
        for entity in self.entities:
            entity.update(dt)

        # 6. Camera follow
        self.camera.follow(self.player.rect)
        self.camera.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        # 1. Draw tilemap (background layer)
        self.tilemap.draw(surface, self.camera)

        # 2. Draw entities (player drawn as a cyan rectangle)
        self.player.draw(surface, self.camera)
        for entity in self.entities:
            entity.draw(surface, self.camera)

    # ── Physics Pipeline ─────────────────────────────────────────────────

    def _apply_player_input(self, dt: float) -> None:
        """
        Convert player input into horizontal velocity.
        Does NOT apply gravity — that's done in _apply_gravity.
        """
        from src.core.settings import (
            PLAYER_ACCELERATION,
            PLAYER_MAX_SPEED,
            PLAYER_FRICTION,
        )

        h = self.input.get_horizontal()

        if h != 0:
            # Accelerate
            self.player.vx += h * PLAYER_ACCELERATION * dt
        else:
            # Friction (framerate-independent exponential decay)
            self.player.vx *= pow(1.0 - PLAYER_FRICTION, dt * 60.0)
            if abs(self.player.vx) < 0.5:
                self.player.vx = 0.0

        # Clamp horizontal speed
        self.player.vx = max(
            -PLAYER_MAX_SPEED, min(PLAYER_MAX_SPEED, self.player.vx)
        )

        # Jump
        from src.core.settings import PLAYER_JUMP_VELOCITY
        if self.input.is_action_just_pressed("jump") and self.player.on_ground:
            self.player.vy = PLAYER_JUMP_VELOCITY
            self.player.on_ground = False

    def _apply_gravity(self, dt: float) -> None:
        """
        Apply gravitational acceleration to vertical velocity,
        clamping to terminal velocity.
        """
        from src.core.settings import GRAVITY, MAX_FALL_SPEED

        self.player.vy += GRAVITY * dt
        if self.player.vy > MAX_FALL_SPEED:
            self.player.vy = MAX_FALL_SPEED

    def _move_and_collide(self, dt: float) -> None:
        """
        Move the player on X and Y axes separately, resolving
        collisions with solid tiles after each axis.
        Uses float-based AABB to avoid integer truncation issues.
        """
        pw = self.player.width
        ph = self.player.height

        # ── 1. Move on X axis ───────────────────────────────────────────
        ex = self.player.x + self.player.vx * dt
        ey = self.player.y

        # Gather solid rects near the player's bounding box
        probe_rect = pygame.Rect(int(ex) - 2, int(ey) - 2, int(pw) + 4, int(ph) + 4)
        solid_rects = self.tilemap.get_solid_rects_in_region(probe_rect)

        ex, ey, hit_ground_x, hit_wall = resolve_collisions_f(
            ex, ey, pw, ph, solid_rects, self.player.vx, self.player.vy
        )
        self.player.x = ex
        if hit_wall:
            self.player.vx = 0.0

        # ── 2. Move on Y axis ───────────────────────────────────────────
        ex = self.player.x
        ey = self.player.y + self.player.vy * dt

        probe_rect = pygame.Rect(int(ex) - 2, int(ey) - 2, int(pw) + 4, int(ph) + 4)
        solid_rects = self.tilemap.get_solid_rects_in_region(probe_rect)

        ex, ey, hit_ground, hit_wall_y = resolve_collisions_f(
            ex, ey, pw, ph, solid_rects, self.player.vx, self.player.vy
        )
        self.player.y = ey

        # Update ground / ceiling states
        self.player.on_ground = hit_ground
        if hit_ground:
            self.player.vy = 0.0
