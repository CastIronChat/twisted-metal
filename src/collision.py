import arcade
from linked_sprite import LinkedSprite
from bullet import Projectile


def projectile_hits_wall(
    projectile_spritelist, wall_spritelist
):
    for projectile in projectile_spritelist:

        walls_touching_projectile = arcade.check_for_collision_with_list(
            projectile, wall_spritelist
        )

        if len(walls_touching_projectile) > 0:
            projectile.owner.on_collision_with_wall(projectile_spritelist, walls_touching_projectile)

def projectile_hits_player(
    projectile_spritelist, player_spritelist
):
    for projectile in projectile_spritelist:

        players_touching_projectile = arcade.check_for_collision_with_list(
            projectile, player_spritelist
        )

        if len(players_touching_projectile) > 0:
            projectile.owner.on_collision_with_player(projectile_spritelist, players_touching_projectile)


