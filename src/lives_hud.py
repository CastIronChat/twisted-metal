from __future__ import annotations

import arcade

from rounds.game_modes.stock import StockGameModePlayerState
from rounds.game_modes.empty import EmptyGameModePlayerState
from sprite_lists import SpriteLists
from player import Player
from textures import HEART


class LivesHud:
    def __init__(
        self, game_state_mode, hud_x: int, hud_y: int, sprite_lists: SpriteLists
    ):
        self.game_state_mode = game_state_mode

        self.sprite_lists = sprite_lists
        self.starting_lives = self.game_state_mode.lives
        
        # Sets x position of 1st heart based on how many lives player has
        self.hud_x = hud_x - ((self.starting_lives - 1) * 7)
        
        self.hud_y = hud_y - 60
        self.hearts = []

        for z in range(0, self.starting_lives):
            heart = arcade.Sprite(texture=HEART, scale=1.1)
            heart.center_x = self.hud_x + (z * 14)
            heart.center_y = self.hud_y
            self.hearts.append(heart)
            self.sprite_lists.huds.append(heart)

    def update(self):
        for x in range(self.starting_lives):
            if x < self.game_state_mode.lives:
                self.hearts[x].visible = True
            else:
                self.hearts[x].visible = False




    