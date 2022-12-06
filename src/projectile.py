from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple, cast

import arcade

from iron_math import move_sprite_polar, set_sprite_location, sprite_in_bounds
from linked_sprite import LinkedSprite
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
    muzzle_location: Tuple[float, float, float]
    damage: float
    speed: float
    angle_of_motion: float
    sprite_rotation_offset: float
    exists: bool
    """
    Projectile is visible and can be collided with.  Used for long-lived projectile objects that are repeatedly added to/removed from the world over time, such as laser beams.
    """

    explodes: bool

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

    def setup(self, muzzle_location : Tuple[float, float, float], speed: float,
        angle_of_motion: float, sprite_rotation_offet:float = 0, explodes: bool = False):
        self.muzzle_location = muzzle_location
        self.speed = speed
        self.angle_of_motion = angle_of_motion
        self.sprite_rotation_offset = sprite_rotation_offet
        self.explodes = explodes
        set_sprite_location(self.sprite, muzzle_location)
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

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        for player in players_touching_projectile:
            player: LinkedSprite[Player]
            player.owner.take_damage(self.damage)
        self.remove_sprite()


class Beam(Projectile):

    beam_range: float

    def setup(self, beam_range:float, explodes: bool = False):
        self.beam_range = beam_range
        self.explodes = explodes

    def update(self, delta_time: float):
        set_sprite_location(self.sprite, self.muzzle_location)
        move_sprite_polar(self.sprite, self.sprite.width/2, self.muzzle_location[2])

    def on_collision_with_wall(self, walls_touching_projectile: arcade.SpriteList):
        pass

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        for player in players_touching_projectile:
            player: LinkedSprite[Player]
            player.owner.take_damage(self.damage * delta_time)


def update_projectiles(
    delta_time: float,
    sprite_lists: SpriteLists,
):
    for projectile_sprite in sprite_lists.projectiles:
        projectile_sprite: LinkedSprite[Projectile]
        projectile_sprite.owner.update(delta_time)
