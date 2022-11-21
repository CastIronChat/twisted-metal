import arcade
import math
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import add_vec2, rotate_vec2
from player_manager import PlayerManager

# For naming purposes, a bullet can be anything that comes out of a weapon included beams, rockets, etc
def bullet_behavior(delta_time, player_manager: PlayerManager):
    for player in player_manager.players:
        for projectile in player.projectile_list:
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
            beam.position = add_vec2(
                player.sprite.position,
                rotate_vec2(
                    add_vec2(
                        beam.properties.get("yeah_its_a_hack_come_at_me_bro"),
                        (beam.width / 2, 0),
                    ),
                    player.sprite.radians,
                ),
            )
