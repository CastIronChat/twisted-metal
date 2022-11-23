import math
import arcade
from typing import Tuple


def rotate_vec(point: Tuple[float, float], radians: float, /) -> float:
    x, y = point
    s = math.sin(radians)
    c = math.cos(radians)
    return (c * x - s * y, s * x + c * y)


def add_vec(point: Tuple[float, float], translation: Tuple[float, float], /) -> float:
    return (point[0] + translation[0], point[1] + translation[1])


def scale_vec(point: Tuple[float, float], factor: float, /) -> float:
    return (point[0] * factor, point[1] * factor)


def offset_sprite_from(
    child: arcade.Sprite, parent: arcade.Sprite, offset: Tuple[float, float, float]
):
    child.angle = parent.angle + offset[2]
    child.position = add_vec(parent.position, rotate_vec(offset[:2], parent.radians))


def combine_transform(parent: arcade.Sprite, offset: Tuple[float, float, float]):
    angle = parent.angle + offset[2]
    position = add_vec(parent.position, rotate_vec(offset[:2], parent.radians))
    return (position[0], position[1], angle)


def polar_to_vec(speed: float, radians: float):
    return rotate_vec((speed, 0), radians)
