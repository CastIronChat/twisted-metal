from __future__ import annotations
from typing import TYPE_CHECKING
import arcade
import math
from arena.wall import Wall
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import add_vec, rotate_vec, move_sprite_relative_to_parent

from typing import List, cast
from linked_sprite import LinkedSprite
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
# Weapon will never create and instance of Player
if TYPE_CHECKING:
    from weapon import Weapon


class Projectile:
    def __init__(
        self, sprite: LinkedSprite[Projectile], sprite_lists: SpriteLists
    ):
        self.sprite = sprite
        sprite.owner = self
        sprite_lists.projectiles.append(self.sprite)
        self.damage = 0


class Beam:
    def __init__(
        self, sprite: LinkedSprite[Beam], sprite_lists: SpriteLists, weapon: Weapon
    ):
        self.sprite = sprite
        sprite.owner = self
        sprite_lists.beams.append(self.sprite)
        self.dps = 0
        self.weapon = weapon


# For naming purposes, a bullet can be anything that comes out of a weapon included beams, rockets, etc
def bullet_behavior(
    delta_time: float,
    sprite_lists: SpriteLists,
):
    for projectile_sprite in sprite_lists.projectiles:
        projectile_sprite: LinkedSprite[Projectile]
        wall_sprites_collided_with_bullet = cast(
            List[LinkedSprite[Wall]],
            arcade.check_for_collision_with_list(projectile_sprite, sprite_lists.walls),
        )
        if len(wall_sprites_collided_with_bullet) > 0:
            sprite_lists.projectiles.remove(projectile_sprite)
            # stop doing anything with this projectile
            continue
        projectile_sprite.center_x += projectile_sprite.change_x * delta_time
        projectile_sprite.center_y += projectile_sprite.change_y * delta_time
        if (
            projectile_sprite.center_x < 0
            or projectile_sprite.center_x > SCREEN_WIDTH
            or projectile_sprite.center_y < 0
            or projectile_sprite.center_y > SCREEN_HEIGHT
        ):
            sprite_lists.projectiles.remove(projectile_sprite)
    for beam_sprite in sprite_lists.beams:
        beam_sprite: LinkedSprite[Beam]
        move_sprite_relative_to_parent(
            beam_sprite,
            beam_sprite.owner.weapon.weapon_sprite,
            beam_sprite.owner.weapon.muzzle_transform,
        )
