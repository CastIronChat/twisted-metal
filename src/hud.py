from typing import List
import arcade

from player import Player
from playerhud import PlayerHud
from textures import PLAYER_AVATARS


class Hud:

    # generates Player Huds and stores each instance in player_huds.
    def __init__(self, player_list: List[Player]):

        self.sprite: arcade.Sprite
        self.player_hud_startx: int = 100
        self.player_hud_starty: int = 575
        self.hud_sprite_list: list = []
        self.player_number_tracker: int = 0
        self.player_huds: list[PlayerHud]
        self.player_hud_avatars: list[arcade.Sprite]

        self.player_huds = []
        self.player_hud_avatars = [
            arcade.Sprite(texture=texture) for texture in PLAYER_AVATARS
        ]

        for player in player_list:
            self.sprite = PlayerHud(
                player,
                self.player_hud_startx,
                self.player_hud_starty,
                self.player_hud_avatars[self.player_number_tracker],
            )
            self.player_huds.append(self.sprite)

            self.hud_sprite_list.append(self.sprite.background_sprite)
            self.hud_sprite_list.append(self.sprite.health_sprite)
            self.hud_sprite_list.append(self.sprite.player_hud_avatar)

            self.player_hud_startx += 150
            self.player_number_tracker += 1

    def update(self):

        for player_hud in self.player_huds:

            player_hud.update()
