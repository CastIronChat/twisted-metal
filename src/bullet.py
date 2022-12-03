from __future__ import annotations

from typing import List, Tuple, cast

import arcade
from arena.wall import Wall
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import move_sprite_polar, set_sprite_location
from linked_sprite import LinkedSprite
from sprite_lists import SpriteLists


class Projectile:
    """
    A projectile can be anything that is created by a weapon or another projectile included beams, rockets, etc.
    It stores the characteristics of the projectile and is responible the associated sprite
    """

    sprite: LinkedSprite[Projectile]
    sprite_lists: SpriteLists
    damage: float
    speed: float
    radians: float
    sprite_rotation_offset: float
    exists: bool
    beam: bool
    beam_range: float
    explodes: bool

    def __init__(
        self,
        sprite: LinkedSprite[Projectile],
        sprite_lists: SpriteLists,
        speed: float,
        radians: float,
        damage: float,
    ):
        self.sprite = sprite
        sprite.owner = self
        self.sprite_lists = sprite_lists
        self.speed = speed
        self.radians = radians
        self.damage = damage
        self.beam = False
        self.beam_range = 0
        self.explodes = False
        self.sprite_rotation_offset = 0
        self.append_sprite()

    def update(self, delta_time: float):
        move_sprite_polar(self.sprite, self.speed * delta_time, self.radians)

    def set_location(self, location: Tuple[float, float, float]):
        set_sprite_location(self.sprite, location)
        self.sprite.radians += self.sprite_rotation_offset

    def set_beam(self, range: float):
        self.beam = True
        self.beam_range = range

    def set_sprite_rotation_offset(self, radians: float):
        self.sprite_rotation_offset = radians

    def set_explodes(self):
        self.explodes = True
    
    def append_sprite(self):
        self.sprite_lists.projectiles.append(self.sprite)
        self.exists = True

    def remove_sprite(self):
        self.sprite_lists.projectiles.remove(self.sprite)
        self.exists = False

def projectile_behavior(
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
