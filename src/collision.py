from __future__ import annotations

import arcade

from linked_sprite import LinkedSprite
from ordnances.ordnance import Ordnance
from sprite_lists import SpriteLists


def ordnance_hits_wall(sprite_lists: SpriteLists):
    for ordnance_sprite in sprite_lists.ordnance:
        ordnance_sprite: LinkedSprite[Ordnance]
        walls_touching_ordnance = arcade.check_for_collision_with_list(
            ordnance_sprite, sprite_lists.walls
        )

        if len(walls_touching_ordnance) > 0:
            ordnance_sprite.owner.on_collision_with_wall(walls_touching_ordnance)


def ordnance_hits_vehicle(delta_time, sprite_lists: SpriteLists):
    for ordnance_sprite in sprite_lists.ordnance:
        ordnance_sprite: LinkedSprite[Ordnance]
        vehicles_touching_ordnance = arcade.check_for_collision_with_list(
            ordnance_sprite, sprite_lists.vehicles
        )

        if len(vehicles_touching_ordnance) > 0:
            ordnance_sprite.owner.on_collision_with_vehicle(
                delta_time, vehicles_touching_ordnance
            )
