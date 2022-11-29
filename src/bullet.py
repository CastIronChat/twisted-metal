from __future__ import annotations
from typing import TYPE_CHECKING
import arcade
import math
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import add_vec, rotate_vec, move_sprite_relative_to_parent

from typing import List, cast
from arena.wall import SpriteForWall
from linked_sprite import LinkedSprite


# This allows a circular import only for the purposes of type hints
# Weapon will never create and instance of Player
if TYPE_CHECKING:
    from weapon import Weapon
    from player import Player


class Projectile:
    def __init__(
        self, sprite: LinkedSprite[Projectile], sprite_list: arcade.SpriteList
    ):
        self.sprite = sprite
        sprite.owner = self
        sprite_list.append(self.sprite)
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
        self, sprite: LinkedSprite[Beam], sprite_list: arcade.SpriteList, weapon: Weapon
    ):
        self.sprite = sprite
        sprite.owner = self
        sprite_list.append(self.sprite)
        self.dps = 0
        self.weapon = weapon


# For naming purposes, a bullet can be anything that comes out of a weapon included beams, rockets, etc
def bullet_behavior(
    delta_time,
    player_spritelist: arcade.SpriteList,
    projectile_spritelist: arcade.SpriteList,
    beam_spritelist: arcade.SpriteList,
    list_of_walls: arcade.SpriteList,
):
    for projectile_sprite in projectile_spritelist:
        # projectile_sprite: LinkedSprite[Projectile]
        # wall_sprites_collided_with_bullet = cast(
        #     List[SpriteForWall],
        #     arcade.check_for_collision_with_list(projectile_sprite, list_of_walls),
        # )
        # if len(wall_sprites_collided_with_bullet) > 0:
        #     projectile_spritelist.remove(projectile_sprite)
        #     # stop doing anything with this projectile
        #     continue
        projectile_sprite.center_x += projectile_sprite.change_x * delta_time
        projectile_sprite.center_y += projectile_sprite.change_y * delta_time
        if (
            projectile_sprite.center_x < 0
            or projectile_sprite.center_x > SCREEN_WIDTH
            or projectile_sprite.center_y < 0
            or projectile_sprite.center_y > SCREEN_HEIGHT
        ):
            projectile_spritelist.remove(projectile_sprite)
    for beam_sprite in beam_spritelist:
        beam_sprite: LinkedSprite[Beam]
        move_sprite_relative_to_parent(
            beam_sprite,
            beam_sprite.owner.weapon.weapon_sprite,
            beam_sprite.owner.weapon.muzzle_transform,
        )
