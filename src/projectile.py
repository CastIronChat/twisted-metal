from __future__ import annotations

import math
from typing import TYPE_CHECKING, List, Optional, Tuple, cast

import arcade

from arena.wall import Wall
from iron_math import (
    add_vec,
    move_sprite_polar,
    polar_to_cartesian,
    set_sprite_location,
    sprite_in_bounds,
)
from linked_sprite import LinkedSprite, LinkedSpriteCircle
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
# Weapon will never create and instance of Player
if TYPE_CHECKING:
    from player import Player


class Projectile:
    """
    A projectile can be anything that is created by a weapon or another projectile included beams, rockets, etc.
    It stores the characteristics of the projectile and is responible the associated sprite
    """

    sprite: LinkedSprite[Projectile]
    sprite_lists: SpriteLists
    start_location: Tuple[float, float, float]
    damage: float
    speed: float
    angle_of_motion: float
    sprite_rotation_offset: float
    exists: bool
    """
    Projectile is visible and can be collided with.  Used for long-lived projectile objects that are repeatedly added to/removed from the world over time, such as laser beams.
    """
    explosion_radius: float

    def __init__(
        self,
        sprite: LinkedSprite[Projectile],
        sprite_lists: SpriteLists,
        damage: float,
    ):
        self.sprite = sprite
        sprite.owner = self
        self.sprite_lists = sprite_lists
        self.damage = damage
        self.exists = False
        self.speed = 0
        self.angle_of_motion = 0
        self.sprite_rotation_offset = 0
        self.explosion_radius = 0

    def setup(
        self,
        muzzle_location: Tuple[float, float, float],
        speed: float,
        angle_of_motion: float,
        sprite_rotation_offet: float = 0,
        explosion_radius: float = 0,
    ):
        self.start_location = muzzle_location
        self.speed = speed
        self.angle_of_motion = angle_of_motion
        self.sprite_rotation_offset = sprite_rotation_offet
        self.explosion_radius = explosion_radius
        set_sprite_location(self.sprite, self.start_location)
        self.sprite.radians += self.sprite_rotation_offset
        self.append_sprite()

    def update(self, delta_time: float):
        move_sprite_polar(self.sprite, self.speed * delta_time, self.angle_of_motion)
        # check if the projectile left the screen
        if not sprite_in_bounds(self.sprite):
            self.remove_sprite()

    @property
    def location(self) -> Tuple[float, float, float]:
        return (
            self.sprite.center_x,
            self.sprite.center_y,
            self.sprite.radians - self.sprite_rotation_offset,
        )

    def append_sprite(self):
        self.sprite_lists.projectiles.append(self.sprite)
        self.exists = True

    def remove_sprite(self):
        self.sprite_lists.projectiles.remove(self.sprite)
        self.exists = False

    def on_collision_with_wall(self, walls_touching_projectile: arcade.SpriteList):
        self.remove_sprite()
        self._explode()

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        for player in players_touching_projectile:
            player: LinkedSprite[Player]
            player.owner.take_damage(self.damage)
        self.remove_sprite()
        self._explode()

    def _explode(self):
        explosion_appearance = LinkedSpriteCircle[Explosion](
            self.explosion_radius, arcade.color.RED, soft=False
        )
        explosion = Explosion(
            explosion_appearance,
            self.sprite_lists,
            self.damage,
        )
        explosion.setup(self.location, self.explosion_radius)


class Beam(Projectile):
    """
    A Beam is a special type of Projectile that continues to be controlled by the weapon after it is created.
    When it collides with something, it shortens to stop at whatever it is colliding with
    """

    beam_range: float

    def setup(self, beam_range: float, explosion_radius: float = 0):
        self.beam_range = beam_range
        self.explosion_radius = explosion_radius

    def update(self, delta_time: float):
        self.sprite.width = self.beam_range
        self._update_sprite_location()

    def on_collision_with_wall(
        self, walls_touching_projectile: list[LinkedSprite[Wall]]
    ):
        self._shorten_beam(walls_touching_projectile)

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        player: LinkedSprite[Player] = self._shorten_beam(players_touching_projectile)
        if player != None:
            player.owner.take_damage(self.damage * delta_time)

    def _shorten_beam(self, collision_list: list[LinkedSprite]):
        """
        Given a list of sprites the beam collided with, stop the beam at the first sprite it hits.
        Return that first sprite
        """
        collisions = arcade.SpriteList()
        closest_collision: Optional[LinkedSprite] = None
        for collision in collision_list:
            collisions.append(collision)
        point: Tuple[float, float] = self.start_location[:2]
        point_vec: Tuple[float, float] = polar_to_cartesian(1, self.sprite.radians)
        for x in range(1, self.beam_range):
            if arcade.get_sprites_at_point(point, collisions):
                closest_collision = arcade.get_sprites_at_point(point, collisions)[0]
                self.sprite.width = x
                break
            point = add_vec(point, point_vec)
        self._update_sprite_location()
        return closest_collision

    def _update_sprite_location(self):
        set_sprite_location(self.sprite, self.start_location)
        move_sprite_polar(self.sprite, self.sprite.width / 2, self.start_location[2])


def update_projectiles(
    delta_time: float,
    sprite_lists: SpriteLists,
):
    for projectile_sprite in sprite_lists.projectiles:
        projectile_sprite: LinkedSprite[Projectile]
        projectile_sprite.owner.update(delta_time)


class Explosion(Projectile):
    explosion_rate: float

    def setup(
        self, start_location: Tuple[float, float, float], explosion_radius: float
    ):
        self.start_location = start_location
        self.explosion_radius = explosion_radius
        self.sprite.height = 1
        self.sprite.width = 1
        self.explosion_rate = 50
        set_sprite_location(self.sprite, self.start_location)
        self.append_sprite()

    def update(self, delta_time: float):
        if self.sprite.height < self.explosion_radius * 2:
            self.sprite.height += self.explosion_rate * delta_time
            self.sprite.width += self.explosion_rate * delta_time
        else:
            self.remove_sprite()

    def on_collision_with_wall(
        self, walls_touching_projectile: list[LinkedSprite[Wall]]
    ):
        pass

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        pass
