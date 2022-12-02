import math
import arcade
from typing import Tuple

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


def add_vec(
    vector: Tuple[float, float],
    translation: Tuple[
        float,
        float,
    ],
    /,
):
    return (vector[0] + translation[0], vector[1] + translation[1])


def scale_vec(vector: Tuple[float, float], factor: float, /):
    """
    Scale a 2d vector by a given factor.

    vector = (x, y)
    """
    return (vector[0] * factor, vector[1] * factor)


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

def move_sprite_polar(sprite: arcade.Sprite, distance: float, angle: float):
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
