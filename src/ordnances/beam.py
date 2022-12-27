from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple, cast

import arcade

from arena.wall import Wall
from iron_math import (
    add_vec,
    move_sprite_polar,
    polar_to_cartesian,
    set_sprite_location,
)
from linked_sprite import LinkedSprite, LinkedSpriteCircle
from ordnances.ordnance import Ordnance
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
if TYPE_CHECKING:
    from vehicle import Vehicle


class Beam(Ordnance):
    """
    A Beam is a type of Ordncance that continues to be controlled by the weapon after it is created.
    When it collides with something, it shortens to stop at whatever it is colliding with
    """

    dps: float
    beam_range: float
    muzzle_location: Tuple[float, float, float]
    hit_location: Tuple[float, float, float]

    def __init__(
        self,
        sprite: LinkedSprite[Ordnance],
        sprite_lists: SpriteLists,
        payload_list: list[Ordnance],
        dps: float,
        beam_range: float,
    ):
        super().__init__(sprite, sprite_lists, payload_list)
        self.dps = dps
        self.beam_range = beam_range
        self.muzzle_location = (0, 0, 0)

    def update(self, delta_time: float):
        self.sprite.width = self.beam_range
        self._update_sprite_location()

    def on_collision_with_wall(
        self, walls_touching_projectile: list[LinkedSprite[Wall]]
    ):
        self._shorten_beam(walls_touching_projectile)

    def on_collision_with_vehicle(
        self,
        delta_time: float,
        vehicles_touching_projectile: list[LinkedSprite[Vehicle]],
    ):
        vehicle_sprite: LinkedSprite[Vehicle] = self._shorten_beam(
            vehicles_touching_projectile
        )
        if vehicle_sprite != None:
            vehicle_sprite.owner.apply_damage(self.dps * delta_time)

    def _shorten_beam(self, collision_list: list[LinkedSprite]):
        """
        Given a list of sprites the beam collided with, stop the beam at the first sprite it hits.
        Return that first sprite
        """
        collisions = arcade.SpriteList()
        closest_collision: Optional[LinkedSprite] = None
        for collision in collision_list:
            collisions.append(collision)
        point: Tuple[float, float] = self.muzzle_location[:2]
        point_vec: Tuple[float, float] = polar_to_cartesian(1, self.sprite.radians)
        for x in range(1, self.beam_range):
            if arcade.get_sprites_at_point(point, collisions):
                closest_collision = arcade.get_sprites_at_point(point, collisions)[0]
                self.sprite.width = x
                self.hit_location = (point[0], point[1], self.sprite.radians)
                break
            point = add_vec(point, point_vec)
        self._update_sprite_location()
        return closest_collision

    def _update_sprite_location(self):
        set_sprite_location(self.sprite, self.muzzle_location)
        move_sprite_polar(self.sprite, self.sprite.width / 2, self.muzzle_location[2])
