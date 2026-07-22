"""
AABB (Axis-Aligned Bounding Box) Collision Detection & Response.

All collision math is done from scratch — no Pygame sprite groups.
Uses float-based AABB to avoid integer truncation issues.
"""

from typing import Optional

import pygame


def aabb_overlap_f(
    ax: float, ay: float, aw: float, ah: float,
    bx: float, by: float, bw: float, bh: float,
) -> bool:
    """
    Float-based AABB overlap test.
    Returns True if the two boxes intersect.
    """
    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )


def resolve_collisions_f(
    ex: float, ey: float, ew: float, eh: float,
    solid_rects: list[pygame.Rect],
    vx: float, vy: float,
) -> tuple[float, float, bool, bool]:
    """
    Resolve an entity (float AABB) against a list of solid tile rects.

    Iteratively pushes the entity out on the shallowest axis per tile,
    which handles corner cases and multi-tile contacts.

    Parameters
    ----------
    ex, ey : float
        Entity's current top-left position (float).
    ew, eh : float
        Entity's width and height.
    solid_rects : list[pygame.Rect]
        List of solid tile rects (world-space, integer).
    vx, vy : float
        Entity's velocity (used for direction hint).

    Returns
    -------
    (corrected_x, corrected_y, hit_ground, hit_wall)
    """
    hit_ground = False
    hit_wall = False

    for tile_rect in solid_rects:
        tx, ty, tw, th = tile_rect.x, tile_rect.y, tile_rect.width, tile_rect.height

        # Check float-based overlap
        if not aabb_overlap_f(ex, ey, ew, eh, tx, ty, tw, th):
            continue

        # Calculate overlap amounts on each axis
        overlap_left   = (ex + ew) - tx   # how far entity right is inside tile left
        overlap_right  = (tx + tw) - ex   # how far entity left is inside tile right
        overlap_top    = (ey + eh) - ty   # how far entity bottom is inside tile top
        overlap_bottom = (ty + th) - ey   # how far entity top is inside tile bottom

        # Minimum push distance on each axis
        min_overlap_x = min(overlap_left, overlap_right)
        min_overlap_y = min(overlap_top, overlap_bottom)

        # Resolve along the axis of least penetration
        if min_overlap_x < min_overlap_y:
            # Push out on X
            if overlap_left < overlap_right:
                ex -= overlap_left   # push left
            else:
                ex += overlap_right  # push right
            hit_wall = True
        else:
            # Push out on Y
            if overlap_top < overlap_bottom:
                ey -= overlap_top    # push up → was on ground
                hit_ground = True
            else:
                ey += overlap_bottom # push down → hit ceiling
            # Don't set hit_wall here

    return ex, ey, hit_ground, hit_wall