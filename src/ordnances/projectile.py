from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple, cast

import arcade

from ordnances.ordnance import Ordnance
from arena.wall import Wall
from iron_math import (
    move_sprite_polar,
    set_sprite_location,
    sprite_in_bounds,
)
from linked_sprite import LinkedSprite, LinkedSpriteCircle
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
# Weapon will never create and instance of Player
if TYPE_CHECKING:
    from player import Player

class Projectile(Ordnance):
    """
    A Projectile is a type of Ordncance that is created by a weapon with a direction and speed, and then forgotten about by the weapon.
    When it collides with something, it activates its payload and is removed
    """

    damage: float
    speed: float
    angle_of_motion: float

    def __init__(
        self,
        sprite: LinkedSprite[Ordnance],
        sprite_lists: SpriteLists,
        payload_list: list[Ordnance],
        damage: float,
        muzzle_location: Tuple[float, float, float],
        speed: float,
        angle_of_motion: float,
        sprite_rotation_offet: float = 0,
    ):
        super().__init__(sprite, sprite_lists, payload_list)
        self.damage = damage
        self.speed = speed
        self.angle_of_motion = angle_of_motion
        self.sprite_rotation_offset = sprite_rotation_offet
        set_sprite_location(self.sprite, muzzle_location)
        self.sprite.radians += self.sprite_rotation_offset
        self.append_sprite()

    def update(self, delta_time: float):
        move_sprite_polar(self.sprite, self.speed * delta_time, self.angle_of_motion)
        # check if the projectile left the screen
        if not sprite_in_bounds(self.sprite):
            self.remove_sprite()

    def on_collision_with_wall(self, walls_touching_projectile: arcade.SpriteList):
        self.remove_sprite()
        self.activate_payload()

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        for player_sprite in players_touching_projectile:
            player_sprite: LinkedSprite[Player]
            player_sprite.owner.take_damage(self.damage)
        self.remove_sprite()
        self.activate_payload()