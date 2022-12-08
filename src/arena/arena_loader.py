from __future__ import annotations

from math import radians

import arcade
from pytiled_parser import ObjectLayer
from pytiled_parser.tiled_object import Rectangle, TiledObject

from arena.arena import Arena
from arena.patrol_waypoint import PatrolWaypoint
from arena.spawn_point import SpawnPoint
from arena.wall import Wall
from constants import SCREEN_HEIGHT
from iron_math import add_vec, rotate_vec, scale_vec
from path import Path


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
    objects_by_id = dict()
    patrol_waypoints: dict[PatrolWaypoint] = dict()
    # tiled_object_to_waypoint_map
    for object in object_layer.tiled_objects:
        objects_by_id[object.id] = object
        if object.class_ == "Wall":
            if not isinstance(object, Rectangle):
                raise Exception(
                    "Found a Tiled object with the 'Wall' class that is not a Rectangle. Only rectangles may be used for walls."
                )
            transform, size = get_rectangle_object_transform_and_size(object)

            wall = Wall(transform, size)
            arena._walls.append(wall)
        elif object.class_ == "SpawnPoint":
            transform, size = get_tile_object_transform_and_size(object)
            initial_spawn_for_player_str = object.properties.get(
                "initial_spawn_for_player"
            )
            initial_spawn_for_player = None
            if initial_spawn_for_player_str is not None:
                initial_spawn_for_player = int(initial_spawn_for_player_str)

            spawn_point = SpawnPoint(transform, initial_spawn_for_player)

            arena._spawn_points.append(spawn_point)
            if initial_spawn_for_player is not None:
                arena._initial_spawn_points[initial_spawn_for_player] = spawn_point
        elif object.class_ == "PatrolWaypoint":
            transform, size = get_tile_object_transform_and_size(object)
            patrol_waypoints[object.id] = PatrolWaypoint(transform[:2])

    # Discover patrol loops
    patrol_loops: list[list[PatrolWaypoint]] = []
    while len(patrol_waypoints):
        patrol_loop: list[PatrolWaypoint] = []
        patrol_loops.append(patrol_loop)
        object_id, waypoint = patrol_waypoints.popitem()
        first_object_id = object_id
        object = objects_by_id[object_id]
        patrol_loop.append(waypoint)
        while True:
            object_id = int(object.properties["next"])
            object = objects_by_id[object_id]
            # If we completed the loop, stop here
            if object_id == first_object_id:
                break
            waypoint = patrol_waypoints.pop(object_id)
            patrol_loop.append(waypoint)
    if len(patrol_loops) != 1:
        raise Exception(
            "Arena must have exactly one patrol loop.  This restriction will likely be removed in the future."
        )
    arena._patrol_loop = Path(
        [
            (index * 1.0, point.location[0], point.location[1])
            for index, point in enumerate(patrol_loops[0] + [patrol_loops[0][0]])
        ]
    )

    return arena


def get_tile_object_transform_and_size(object: TiledObject):
    """
    Return the transform and dimensions of a Tile Object loaded from Tiled map editor.

    Returns (transform, size) where:

    transform = (x, y, radians)

    size = (width, height)
    """
    return get_object_transform_and_size(object, True)


def get_rectangle_object_transform_and_size(object: TiledObject):
    """
    Return the transform and dimensions of a Rectangle Object loaded from Tiled map editor.

    Returns (transform, size) where:

    transform = (x, y, radians)

    size = (width, height)
    """
    return get_object_transform_and_size(object, False)


def get_object_transform_and_size(object: TiledObject, pivot_is_at_bottom: bool):
    y_offset = SCREEN_HEIGHT
    converted_position = (
        object.coordinates.x,
        y_offset - object.coordinates.y,
    )
    rotation = radians(-object.rotation)

    # TODO I kinda hate this syntax; why is python like this?
    height_offset = object.size.height if pivot_is_at_bottom else -object.size.height

    center_offset = scale_vec((object.size.width, height_offset), 0.5)
    rotated_center_offset = rotate_vec(center_offset, rotation)
    center = add_vec(rotated_center_offset, converted_position)

    transform = (center[0], center[1], rotation)

    size = (object.size.width, object.size.height)

    return (transform, size)
