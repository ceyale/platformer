"""
Math helpers — common vector / geometry operations used by physics
and rendering.
"""

import math
from typing import Union

# Numeric type that can be used for scalars
Num = Union[int, float]


def clamp(value: Num, low: Num, high: Num) -> Num:
    """Constrain *value* to the range [low, high]."""
    return max(low, min(high, value))


def lerp(a: float, b: float, t: float) -> float:
    """
    Linear interpolation between *a* and *b* by factor *t* (0..1).
    """
    return a + (b - a) * clamp(t, 0.0, 1.0)


def inverse_lerp(a: float, b: float, value: float) -> float:
    """Return the normalised position of *value* within [a, b]."""
    if abs(b - a) < 1e-12:
        return 0.0
    return (value - a) / (b - a)


def sign(x: float) -> float:
    """Return -1.0, 0.0, or 1.0."""
    if x > 0.0:
        return 1.0
    if x < 0.0:
        return -1.0
    return 0.0


def approach(current: float, target: float, delta: float) -> float:
    """
    Move *current* toward *target* by at most *delta* (framerate-
    independent).  Like lerp but with a fixed step size.
    """
    diff = target - current
    if abs(diff) <= delta:
        return target
    return current + sign(diff) * delta