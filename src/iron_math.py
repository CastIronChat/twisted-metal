import math
from typing import Tuple


def rotate_vec2(point: Tuple[float, float], radians: float, /) -> float:
    x, y = point
    s = math.sin(radians)
    c = math.cos(radians)
    return (c * x - s * y, s * x + c * y)


def add_vec2(point: Tuple[float, float], translation: Tuple[float, float], /) -> float:
    return (point[0] + translation[0], point[1] + translation[1])

def scale_vec2(point: Tuple[float, float], factor: float, /) -> float:
    return (point[0] * factor, point[1] * factor)
