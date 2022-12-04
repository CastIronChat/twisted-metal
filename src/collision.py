from __future__ import annotations
import arcade
from bullet import Projectile
from linked_sprite import LinkedSprite
from player import Player
from sprite_lists import SpriteLists


def projectile_hits_wall(sprite_lists: SpriteLists):
    for projectile in sprite_lists.projectiles:
        projectile: LinkedSprite[Projectile]
        walls_touching_projectile = arcade.check_for_collision_with_list(
            projectile, sprite_lists.walls
        )

        if len(walls_touching_projectile) > 0:
            projectile.owner.on_collision_with_wall(
                sprite_lists.projectiles, walls_touching_projectile
            )


def projectile_hits_player(sprite_lists: SpriteLists):
    for projectile in sprite_lists.projectiles:
        projectile: LinkedSprite[Projectile]
        players_touching_projectile = arcade.check_for_collision_with_list(
            projectile, sprite_lists.players
        )

        if len(players_touching_projectile) > 0:
            projectile.owner.on_collision_with_player(
                sprite_lists.projectiles, players_touching_projectile
            )
