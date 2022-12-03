from __future__ import annotations

import math
from typing import TYPE_CHECKING, List, cast

import arcade

from arena.wall import Wall
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import add_vec, move_sprite_relative_to_parent, rotate_vec
from linked_sprite import LinkedSprite
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
# Weapon will never create and instance of Player
if TYPE_CHECKING:
    from weapon import Weapon
    from player import Player


class Projectile:
    def __init__(self, sprite: LinkedSprite[Projectile], sprite_lists: SpriteLists):
        self.sprite = sprite
        sprite.owner = self
        sprite_lists.projectiles.append(self.sprite)
        self.damage = 0

    def on_collision_with_wall(projectile, projectile_spritelist: arcade.SpriteList, walls_touching_projectile: arcade.SpriteList):
        projectile_spritelist.remove(projectile.sprite)
        
    def on_collision_with_player(projectile, projectile_spritelist: arcade.SpriteList, players_touching_projectile: arcade.SpriteList):
        for player in players_touching_projectile:
            player: LinkedSprite[Player]
            projectile: LinkedSprite[projectile]
            player.owner.player_health -= projectile.damage
        projectile_spritelist.remove(projectile.sprite)


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
