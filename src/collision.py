from __future__ import annotations
import arcade
from projectile import Projectile
from linked_sprite import LinkedSprite
from sprite_lists import SpriteLists


def projectile_hits_wall(sprite_lists: SpriteLists):
    for projectile_sprite in sprite_lists.projectiles:
        projectile_sprite: LinkedSprite[Projectile]
        walls_touching_projectile = arcade.check_for_collision_with_list(
            projectile_sprite, sprite_lists.walls
        )

        if len(walls_touching_projectile) > 0:
            projectile_sprite.owner.on_collision_with_wall(walls_touching_projectile)


def projectile_hits_player(delta_time, sprite_lists: SpriteLists):
    for projectile_sprite in sprite_lists.projectiles:
        projectile_sprite: LinkedSprite[Projectile]
        players_touching_projectile = arcade.check_for_collision_with_list(
            projectile_sprite, sprite_lists.players
        )

        if len(players_touching_projectile) > 0:
            projectile_sprite.owner.on_collision_with_player(delta_time, players_touching_projectile)
