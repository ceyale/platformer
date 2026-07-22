"""
Core game loop — the engine's heartbeat.

Owns the Pygame display, clock, and the main loop that drives
update → draw → present every frame.  All game logic is delegated
to a SceneManager (or a single Scene) so the loop itself stays
generic and reusable.
"""

import sys

import pygame

from src.core.settings import (
    WINDOW_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GAME_WIDTH,
    GAME_HEIGHT,
    FPS_CAP,
    VSYNC,
    SKY_COLOR,
    COLOR_BLACK,
    SHOW_DEBUG_OVERLAY,
    SHOW_TILE_GRID,
)


class Game:
    """Top-level engine container.  Owns the window, clock, and scene."""

    def __init__(self, scene: "Scene | None" = None) -> None:
        pygame.init()

        # ── Window ───────────────────────────────────────────────────────
        flags = pygame.SCALED | pygame.HWSURFACE
        self.screen: pygame.Surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            flags=flags,
            vsync=VSYNC,
        )
        pygame.display.set_caption(WINDOW_TITLE)

        # Low-resolution render target (pixel-art surface)
        self.render_surface: pygame.Surface = pygame.Surface(
            (GAME_WIDTH, GAME_HEIGHT), pygame.SWSURFACE
        )

        # ── Clock ────────────────────────────────────────────────────────
        self.clock = pygame.time.Clock()
        self.dt: float = 0.0
        self.running: bool = True

        # ── Debug ────────────────────────────────────────────────────────
        self.show_debug = SHOW_DEBUG_OVERLAY
        self.show_grid = SHOW_TILE_GRID
        self._font: pygame.Font = pygame.Font(None, 18)

        # ── Scene ────────────────────────────────────────────────────────
        self.scene = scene

    # ── Properties ───────────────────────────────────────────────────────

    @property
    def fps(self) -> float:
        return self.clock.get_fps()

    # ── Main Loop ────────────────────────────────────────────────────────

    def run(self) -> None:
        """The delta-time game loop."""
        while self.running:
            ms = self.clock.tick_busy_loop(FPS_CAP)
            self.dt = ms / 1000.0

            self._handle_events()
            self._update(self.dt)
            self._draw()

            # Scale the pixel-art surface to the window
            scaled = pygame.transform.scale(
                self.render_surface,
                (WINDOW_WIDTH, WINDOW_HEIGHT),
            )
            self.screen.blit(scaled, (0, 0))

            if self.show_debug:
                self._draw_debug_overlay()

            pygame.display.flip()

        self._quit()

    # ── Event Handling ───────────────────────────────────────────────────

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                elif event.key == pygame.K_F3:
                    self.show_debug = not self.show_debug
                elif event.key == pygame.K_F4:
                    self.show_grid = not self.show_grid

            # Forward event to the active scene
            if self.scene is not None:
                self.scene.handle_event(event)

    # ── Update / Draw ────────────────────────────────────────────────────

    def _update(self, dt: float) -> None:
        if self.scene is not None:
            self.scene.update(dt)

    def _draw(self) -> None:
        self.render_surface.fill(SKY_COLOR)
        if self.scene is not None:
            self.scene.draw(self.render_surface)

    # ── Debug Overlay ────────────────────────────────────────────────────

    def _draw_debug_overlay(self) -> None:
        lines = [
            f"FPS: {self.fps:.1f}   DT: {self.dt*1000:.1f}ms",
            f"Grid: {'ON' if self.show_grid else 'OFF'}  [F4]",
        ]
        y = 8
        for line in lines:
            surf = self._font.render(line, True, COLOR_BLACK)
            self.screen.blit(surf, (8, y))
            y += 20

    # ── Shutdown ─────────────────────────────────────────────────────────

    def _quit(self) -> None:
        pygame.quit()
        sys.exit()