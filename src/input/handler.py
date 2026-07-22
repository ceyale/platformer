"""
InputHandler — keyboard state polling and action mapping.

Provides a clean API for querying actions (e.g. ``is_action_pressed('jump')``)
while the underlying key-to-action mapping is configurable.
"""

import pygame
from pygame.locals import (
    K_LEFT, K_RIGHT, K_UP, K_DOWN,
    K_SPACE, K_LSHIFT, K_LCTRL, K_z, K_x,
)


# Default action → key bindings
DEFAULT_BINDINGS: dict[str, int] = {
    "move_left":  K_LEFT,
    "move_right": K_RIGHT,
    "move_up":    K_UP,
    "move_down":  K_DOWN,
    "jump":       K_SPACE,
    "jump_alt":   K_UP,
    "sprint":     K_LSHIFT,
    "action":     K_z,
    "action_alt": K_x,
}


class InputHandler:
    """
    Polls keyboard state each frame and exposes action-based queries.

    Usage
    -----
    handler = InputHandler()
    # Inside game loop, after event polling:
    handler.update()
    if handler.is_action_pressed("jump"):
        ...
    """

    def __init__(self, bindings: dict[str, int] | None = None) -> None:
        self._bindings = bindings or DEFAULT_BINDINGS
        self._previous_keys: pygame.key.ScancodeWrapper | None = None
        self._current_keys: pygame.key.ScancodeWrapper | None = None

    def update(self) -> None:
        """
        Snap the current keyboard state.  Call once per frame *after*
        event processing.
        """
        self._previous_keys = self._current_keys
        self._current_keys = pygame.key.get_pressed()

    # ── Query helpers ──────────────────────────────────────────────────

    def is_key_pressed(self, key: int) -> bool:
        """Is *key* currently held down?"""
        if self._current_keys is None:
            return False
        return bool(self._current_keys[key])

    def is_key_just_pressed(self, key: int) -> bool:
        """Was *key* pressed this frame (transition from up → down)?"""
        if self._previous_keys is None or self._current_keys is None:
            return False
        return bool(self._current_keys[key]) and not bool(self._previous_keys[key])

    def is_key_just_released(self, key: int) -> bool:
        """Was *key* released this frame (transition from down → up)?"""
        if self._previous_keys is None or self._current_keys is None:
            return False
        return not bool(self._current_keys[key]) and bool(self._previous_keys[key])

    # ── Action-based queries ────────────────────────────────────────────

    def is_action_pressed(self, action: str) -> bool:
        """Is any key bound to *action* currently held?"""
        key = self._bindings.get(action)
        if key is None:
            return False
        return self.is_key_pressed(key)

    def is_action_just_pressed(self, action: str) -> bool:
        """Was *action* triggered this frame?"""
        key = self._bindings.get(action)
        if key is None:
            return False
        return self.is_key_just_pressed(key)

    def is_action_just_released(self, action: str) -> bool:
        """Was *action* released this frame?"""
        key = self._bindings.get(action)
        if key is None:
            return False
        return self.is_key_just_released(key)

    # ── Raw axis helpers ────────────────────────────────────────────────

    def get_axis(self, negative: str, positive: str) -> float:
        """
        Return -1, 0, or 1 for directional input.
        Useful for horizontal / vertical movement.
        """
        value = 0.0
        if self.is_action_pressed(negative):
            value -= 1.0
        if self.is_action_pressed(positive):
            value += 1.0
        return value

    def get_horizontal(self) -> float:
        """Return -1, 0, or 1 for left/right."""
        return self.get_axis("move_left", "move_right")

    def get_vertical(self) -> float:
        """Return -1, 0, or 1 for up/down."""
        return self.get_axis("move_up", "move_down")