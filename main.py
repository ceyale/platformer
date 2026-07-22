"""
Retro Platformer — entry point.

Run this script to launch the engine.  It creates a Game instance
with a GameplayScene, loads level 001, and starts the delta-time loop.
"""

import sys
import os

# Ensure the project root is on sys.path so absolute imports work
_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.core.game import Game
from src.core.scene import GameplayScene
from src.tilemap.tilemap import Tilemap
from src.tilemap.constants import *   # registers all standard tiles
from src.rendering.camera import Camera
from data.levels.level_001 import LEVEL_GRID


def main() -> None:
    # ── Initialise tilemap from level data ──────────────────────────────
    tilemap = Tilemap(grid=LEVEL_GRID)

    # ── Create the gameplay scene ──────────────────────────────────────
    scene = GameplayScene(tilemap=tilemap)

    # Position the player on the ground at tile (2, 12) which is grass
    scene.player.x = 2.0 * 16.0    # column 2 → pixel 32
    scene.player.y = 12.0 * 16.0 - scene.player.height  # top of grass row

    # ── Boot the engine ─────────────────────────────────────────────────
    game = Game(scene=scene)
    game.run()


if __name__ == "__main__":
    main()