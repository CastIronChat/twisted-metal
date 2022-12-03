from __future__ import annotations

import arcade

from bullet import Projectile
from linked_sprite import LinkedSprite
from player import Player


def projectile_hits_wall(projectile_spritelist, wall_spritelist):
    for projectile in projectile_spritelist:
        projectile: LinkedSprite[Projectile]
        walls_touching_projectile = arcade.check_for_collision_with_list(
            projectile, wall_spritelist
        )

        if len(walls_touching_projectile) > 0:
            projectile.owner.on_collision_with_wall(
                projectile_spritelist, walls_touching_projectile
            )


def projectile_hits_player(projectile_spritelist, player_spritelist):
    for projectile in projectile_spritelist:
        projectile: LinkedSprite[Projectile]
        players_touching_projectile = arcade.check_for_collision_with_list(
            projectile, player_spritelist
        )

        if len(players_touching_projectile) > 0:
            projectile.owner.on_collision_with_player(
                projectile_spritelist, players_touching_projectile
            )


def player_hits_wall(player_spritelist, wall_spritelist):
    for player in player_spritelist:
        player: LinkedSprite[Player]
        walls_touching_players = arcade.check_for_collision_with_list(
            player, wall_spritelist
        )
        collision_tolerance = 10
        if len(walls_touching_players) > 0:
            if abs(walls_touching_players[0].top - player.bottom) < collision_tolerance:
                player.bottom = walls_touching_players[0].bottom + player.height
            if abs(walls_touching_players[0].bottom - player.top) < collision_tolerance:
                player.top = walls_touching_players[0].top - player.height
            if abs(walls_touching_players[0].left - player.right) < collision_tolerance:
                player.left = walls_touching_players[0].left - player.width
            if abs(walls_touching_players[0].right - player.left) < collision_tolerance:
                player.right = walls_touching_players[0].right + player.width
