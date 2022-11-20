import arcade
import math
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player_manager import PlayerManager

#For naming purposes, a bullet can be anything that comes out of a weapon included beams, rockets, etc
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
            beam.center_x = player.sprite.center_x + beam.velocity * math.cos(player.sprite.radians)
            beam.center_y = player.sprite.center_y + beam.velocity * math.sin(player.sprite.radians)
