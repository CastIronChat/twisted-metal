from __future__ import annotations

import arcade

from arena.arena import Wall
from linked_sprite import LinkedSprite
from player import Player
from projectile import Projectile
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
            projectile_sprite.owner.on_collision_with_player(
                delta_time, players_touching_projectile
            )


def player_hits_wall(sprite_lists: SpriteLists):
    for player_sprite in sprite_lists.players:
        player_sprite: LinkedSprite[Player]
        walls_probably_touching: LinkedSprite[Wall]
        walls_touching_players = arcade.check_for_collision_with_list(
            player_sprite, sprite_lists.walls
        )
        if len(walls_touching_players) > 0:
            walls_probably_touching = walls_touching_players[0]

            """
            stores a diagonal from center of our player and compares
            to a side of our wall, determines if intersecting based off
            of "if (t1 >= 0.0 and t1 < 1.0 and t2 >= 0.0 and t2 < 1.0)"
            Referenced https://www.youtube.com/watch?v=7Ik2vowGcU0

            included collision detection to get the behavior,
            which functions off of (1 - t1) derived in line intersection detection
             """

            for corner in player_sprite.owner.list_of_corners:
                line_r1s = player_sprite.owner.location
                line_r1e = corner
                i = 0
                for sides in walls_probably_touching.owner.list_of_corners:
                    line_r2s = walls_probably_touching.owner.list_of_corners[i]
                    line_r2e = walls_probably_touching.owner.list_of_corners[
                        (i + 1) % len(sides)
                    ]

                    h = (line_r2e[0] - line_r2s[0]) * (line_r1s[1] - line_r1e[1]) - (
                        line_r1s[0] - line_r1e[0]
                    ) * (line_r2e[1] - line_r2s[1])
                    t1 = (
                        (line_r2s[1] - line_r2e[1]) * (line_r1s[0] - line_r2s[0])
                        + (line_r2e[0] - line_r2s[0]) * (line_r1s[1] - line_r2s[1])
                    ) / h
                    t2 = (
                        (line_r1s[1] - line_r1e[1]) * (line_r1s[0] - line_r2s[0])
                        + (line_r1e[0] - line_r1s[0]) * (line_r1s[1] - line_r2s[1])
                    ) / h
                    if t1 >= 0.0 and t1 < 1.0 and t2 >= 0.0 and t2 < 1.0:
                        player_sprite.center_x += (1.0 - t1) * (
                            line_r1e[0] - line_r1s[0]
                        )
                        player_sprite.center_y += (1.0 - t1) * (
                            line_r1e[1] - line_r1s[1]
                        )
