from __future__ import annotations

import math
from typing import TYPE_CHECKING, List, cast

import arcade

from arena.wall import Wall
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import move_sprite_relative_to_parent, move_sprite_polar
from linked_sprite import LinkedSprite
from sprite_lists import SpriteLists


class Projectile:
    sprite: LinkedSprite[Projectile]
    sprite_lists: SpriteLists
    damage: float
    speed: float
    radians: float
    sprite_rotation_offset: float
    beam: bool
    explodes: bool

    def __init__(
        self, sprite: LinkedSprite[Projectile], sprite_lists: SpriteLists, speed: float, radians: float, damage: float
    ):
        self.sprite = sprite
        sprite.owner = self
        self.sprite_lists = sprite_lists
        self.speed = speed
        self.radians = radians
        self.damage = damage
        self.beam = False
        self.explodes = False
        self.sprite_rotation_offset = 0
        self.sprite_lists.projectiles.append(self.sprite)

    def update(self, delta_time: float):
        move_sprite_polar(self.sprite, self.speed * delta_time, self.radians)

    def set_beam(self):
        self.beam = True


# For naming purposes, a bullet can be anything that comes out of a weapon included beams, rockets, etc
def bullet_behavior(
    delta_time: float,
    sprite_lists: SpriteLists,
):
    for projectile_sprite in sprite_lists.projectiles:
        projectile_sprite: LinkedSprite[Projectile]
        # If beam, skip the current projectile collision code that deletes projectiles that hit walls
        if projectile_sprite.owner.beam:
            continue
        projectile_sprite.owner.update(delta_time)
        wall_sprites_collided_with_bullet = cast(
            List[LinkedSprite[Wall]],
            arcade.check_for_collision_with_list(projectile_sprite, sprite_lists.walls),
        )
        if len(wall_sprites_collided_with_bullet) > 0:
            sprite_lists.projectiles.remove(projectile_sprite)
            # stop doing anything with this projectile
            continue
        if (
            projectile_sprite.center_x < 0
            or projectile_sprite.center_x > SCREEN_WIDTH
            or projectile_sprite.center_y < 0
            or projectile_sprite.center_y > SCREEN_HEIGHT
        ):
            sprite_lists.projectiles.remove(projectile_sprite)
        
