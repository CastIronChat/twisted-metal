from __future__ import annotations

import math
from typing import Tuple

import arcade

from constants import SCREEN_HEIGHT, SCREEN_WIDTH

#
# Note: all functions in this file should use positional-only parameters because
# it's slightly faster.  The `, /` suffix at the end denotes this.
# https://peps.python.org/pep-0570/#performance
#
# All functions accept and return radians, not degrees, unless otherwise specified.
#


def rotate_vec(vector: Tuple[float, float], radians: float, /):
    """
    Rotate a 2d vector about the origin.

    vector = (x, y)

    Returns (x, y)
    """
    x, y = vector
    s = math.sin(radians)
    c = math.cos(radians)
    return (c * x - s * y, s * x + c * y)


def add_vec(*vectors: Tuple[float, float]):
    """
    Add zero or more 2d cartesian vectors together.

    Example usage:
        result = add_vec((0.0, 1.0), (-3.0, 4.0), (5.0, 0.0))
        # result is (2.0, 5.0)
    """
    x = 0.0
    y = 0.0
    for vector in vectors:
        x += vector[0]
        y += vector[1]
    return (x, y)


def subtract_vec(vector_a: tuple[float, float], vector_b: tuple[float, float], /):
    """
    Subtract vector_b from vector_a, getting the relative vector pointing from b to a.

    vector_a = (x, y)

    vector_b = (x, y)

    Returns (x, y)
    """
    return (vector_a[0] - vector_b[0], vector_a[1] - vector_b[1])


def scale_vec(vector: Tuple[float, float], factor: float, /):
    """
    Scale a 2d vector by a given factor.

    vector = (x, y)
    """
    return (vector[0] * factor, vector[1] * factor)


def vec_magnitude(vector: Tuple[float, float], /):
    x, y = vector
    return math.sqrt(x * x + y * y)


def normalize_vec(vector: Tuple[float, float], /):
    x, y = vector
    mag = vec_magnitude(vector)
    if mag == 0:
        return (0, 0)
    return (x / mag, y / mag)


def vec_dot_product(vector: Tuple[float, float], vector2: Tuple[float, float], /):
    x, y = vector
    x2, y2 = vector2
    return x * x2 + y * y2


def project_vec(vector: Tuple[float, float], axis: Tuple[float, float], /):
    axis_normalized = normalize_vec(axis)
    return scale_vec(axis_normalized, vec_dot_product(axis_normalized, vector))


def move_sprite_relative_to_parent(
    child: arcade.Sprite,
    parent: arcade.Sprite,
    transform: Tuple[float, float, float],
    /,
):
    """
    Move child to a new position and rotation, derived by applying the given transformation
    to parent's position and rotation.

    transform = (x, y, radians)
    """
    child.radians = parent.radians + transform[2]
    child.position = add_vec(parent.position, rotate_vec(transform[:2], parent.radians))


def get_sprite_location(sprite: arcade.Sprite, /):
    """
    Return a sprite's position and rotation.

    Returns (x, y, radians)
    """
    return (sprite.position[0], sprite.position[1], sprite.radians)


def set_sprite_location(
    sprite: arcade.Sprite,
    location: Tuple[float, float, float],
    /,
):
    """
    Set sprite's position and rotation.

    location = (x, y, radians)
    """
    sprite.radians = location[2]
    sprite.position = location[:2]


def move_sprite_polar(sprite: arcade.Sprite, distance: float, angle: float, /):
    """
    move sprite from current location given a distance and angle
    """
    sprite.position = add_vec(sprite.position, polar_to_cartesian(distance, angle))


def get_transformed_location(
    parent: arcade.Sprite, transform: Tuple[float, float, float], /
):
    """
    Apply a geometric transformation to the position and rotation of `parent`, returning
    the new position and rotation.
    Does not move parent.

    transform = (x, y, radians)

    Returns (x, y, radians)
    """
    angle = parent.radians + transform[2]
    position = add_vec(parent.position, rotate_vec(transform[:2], parent.radians))
    return (position[0], position[1], angle)


def polar_to_cartesian(magnitude: float, radians: float, /):
    """
    Convert polar coordinates to certesian. If you pass a negative magnitude, it
    is equivalent to flipping the vector 180 degrees, making it point in the
    opposite direction.

    Returns (x, y)
    """
    return rotate_vec((magnitude, 0), radians)


def clamp(value: float, min: float, max: float):
    if max < min:
        raise Exception("max must be >= to min")
    if value > max:
        return max
    if value < min:
        return min
    return value


def rescale_value_between(
    value: float,
    from_min: float,
    from_max: float,
    to_min: float = 0,
    to_max: float = 1,
    /,
):
    """
    Lerp a value between two extremes described like this:

        When foo is 10, bar should be 20
        When foo is 80, bar should be 100
        Smoothly transition between.

    This function accepts the values: foo, 10, 80, 20, 100
    It returns: bar

    Another way to think about it:

    Imagine a line between two points: (from_min, to_min) and (from_max, to_max)
    Return the Y position on that line at the X position of `value`
    """
    x = value - from_min
    rise = to_max - to_min
    run = from_max - from_min
    return to_min + x * rise / run


def sprite_in_bounds(sprite: arcade.Sprite, /) -> bool:
    """
    Checks if a sprite is within the screen limits and return a bool
    """
    if (
        sprite.center_x < 0
        or sprite.center_x > SCREEN_WIDTH
        or sprite.center_y < 0
        or sprite.center_y > SCREEN_HEIGHT
    ):
        return False
    else:
        return True
