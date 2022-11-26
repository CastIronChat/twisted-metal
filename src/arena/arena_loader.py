from __future__ import annotations

import math
from math import radians

import arcade
from pytiled_parser import ObjectLayer
from pytiled_parser.tiled_object import Rectangle

from arena.arena import Arena
from arena.wall import Wall
from constants import SCREEN_HEIGHT
from iron_math import add_vec, rotate_vec, scale_vec


def load_arena_by_name(name: str) -> Arena:
    arena = Arena()
    # Tiled counts y = 0 as top of screen, increasing y value moves downward
    # arcade does the opposite: y = 0 at bottom of the screen
    # So we must convert y coordinates
    y_offset = SCREEN_HEIGHT
    tilemap = arcade.load_tilemap(f"assets/arenas/{name}.tmx")
    # Assume map contains only a single object layer
    object_layer = next(
        layer for layer in tilemap.tiled_map.layers if isinstance(layer, ObjectLayer)
    )
    # Create walls from all rectangles with the "Wall" class set in Tiled
    for object in object_layer.tiled_objects:
        if object.class_ == "Wall":
            if not isinstance(object, Rectangle):
                raise Exception(
                    "Found a Tiled object with the 'Wall' class that is not a Rectangle. Only rectangles may be used for walls."
                )
            converted_position = (
                object.coordinates.x,
                y_offset - object.coordinates.y,
            )
            rotation = radians(-object.rotation)
            center_offset = scale_vec((object.size.width, -object.size.height), 0.5)
            rotated_center_offset = rotate_vec(center_offset, rotation)
            center = add_vec(rotated_center_offset, converted_position)

            wall = Wall(
                int(center[0]),
                int(center[1]),
                int(object.size.width),
                int(object.size.height),
                rotation,
            )
            arena._walls.append(wall)
    return arena
