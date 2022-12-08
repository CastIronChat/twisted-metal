from __future__ import annotations

from typing import cast

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
        print(projectile_sprite.get_adjusted_hit_box())
        if len(players_touching_projectile) > 0:
            projectile_sprite.owner.on_collision_with_player(
                delta_time, players_touching_projectile
            )


def player_hits_wall(sprite_lists: SpriteLists):
    for player_sprite in sprite_lists.players:
        player_sprite: LinkedSprite[Player]
        player = player_sprite.owner
        walls_touching_player = cast(
            list[LinkedSprite[Wall]],
            arcade.check_for_collision_with_list(player_sprite, sprite_lists.walls),
        )
        if len(walls_touching_player) > 0:
            wall_sprite = walls_touching_player[0]

            """
            stores a diagonal from center of our player and compares
            to a side of our wall, determines if intersecting based off
            of "if (t1 >= 0.0 and t1 < 1.0 and t2 >= 0.0 and t2 < 1.0)"
            Referenced https://www.youtube.com/watch?v=7Ik2vowGcU0

            included collision detection to get the behavior,
            which functions off of (1 - t1) derived in line intersection detection
             """

            wall_hitbox = wall_sprite.get_adjusted_hit_box()
            for car_corner in player_sprite.get_adjusted_hit_box():
                # Line from center of car to corner of car
                car_center = player.location
                for i, wall_corner in enumerate(wall_hitbox):
                    wall_start = wall_corner
                    wall_end = wall_hitbox[(i + 1) % len(wall_hitbox)]
                    print(car_corner)
                    print(car_corner)
                    print(wall_start)
                    print(wall_end)

                    wall_delta_x = wall_end[0] - wall_start[0]
                    wall_delta_y = wall_end[1] - wall_start[1]
                    wall_vec = (wall_delta_x, wall_delta_y)
                    car_delta_x = car_corner[0] - car_center[0]
                    car_delta_y = car_corner[1] - car_center[1]
                    car_vec = (car_delta_x, car_delta_y)
                    wall_start_to_car_delta_x = car_center[0] - wall_start[0]
                    wall_start_to_car_delta_y = car_center[1] - wall_start[1]
                    wall_start_to_car_vec = (
                        wall_start_to_car_delta_x,
                        wall_start_to_car_delta_y,
                    )

                    # 2d cross product between 2 vectors
                    # Vector from center of car to a corner
                    # Vector describing a side of the wall
                    # 0 = parallel 1 = perpendicular
                    # We want h to be higher (closer to 1) so that t1 and t2 are lower
                    # (more likely to trigger logic)
                    h = cross_product(car_vec, wall_vec)

                    # cross product of wall and wall_to_car
                    t1 = cross_product(wall_vec, wall_start_to_car_vec) / h
                    # cross product of car and wall_to_car
                    t2 = cross_product(car_vec, wall_start_to_car_vec) / h

                    # t1 is magnitude wall_start_to_car / car_vec
                    # t2 is magnitude wall_start_to_car / wall_vec

                    if t1 >= 0.0 and t1 < 1.0 and t2 >= 0.0 and t2 < 1.0:
                        player_sprite.center_x -= (1.0 - t1) * car_delta_x
                        player_sprite.center_y -= (1.0 - t1) * car_delta_y


def cross_product(vec_a: tuple[float, float], vec_b: tuple[float, float]):
    a_x, a_y = vec_a
    b_x, b_y = vec_b
    return a_x * b_y - a_y * b_x
