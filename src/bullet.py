import arcade
import math
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import add_vec, rotate_vec
from player_manager import PlayerManager
from typing import List, cast
from arena.wall import SpriteForWall

# For naming purposes, a bullet can be anything that comes out of a weapon included beams, rockets, etc
def bullet_behavior(
    delta_time, player_manager: PlayerManager, list_of_walls: arcade.SpriteList
):
    for player in player_manager.players:
        for projectile in player.projectile_list:
            wall_sprites_collided_with_bullet = cast(
                List[SpriteForWall],
                arcade.check_for_collision_with_list(projectile, list_of_walls),
            )
            if len(wall_sprites_collided_with_bullet) > 0:
                player.projectile_list.remove(projectile)
            projectile.center_x += projectile.change_x * delta_time
            projectile.center_y += projectile.change_y * delta_time
            if (
                projectile.center_x < 0
                or projectile.center_x > SCREEN_WIDTH
                or projectile.center_y < 0
                or projectile.center_y > SCREEN_HEIGHT
            ):
                player.projectile_list.remove(projectile)
        for beam in player.beam_list:
            beam.angle = player.sprite.angle
            beam.position = add_vec(
                player.sprite.position,
                rotate_vec(
                    add_vec(
                        beam.properties.get("yeah_its_a_hack_come_at_me_bro"),
                        (beam.width / 2, 0),
                    ),
                    player.sprite.radians,
                ),
            )
