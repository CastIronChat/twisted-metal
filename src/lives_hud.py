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
        self.lives = self.game_state_mode.lives
        self.hud_x = hud_x - 20
        self.hud_y = hud_y - 60
        self.heart = arcade.Sprite(texture=HEART, scale=1)
        self.sprite_lists.huds.append(self.heart)
        self.heart.center_x = self.hud_x
        self.heart.center_y = self.hud_y



    def update(self):
        print('LH',self.lives)
        print('LH GSM', self.game_state_mode.lives)
        if self.game_state_mode.lives >= 1:
            self.heart.visible = True
        elif self.game_state_mode.lives < 1:
            self.heart.visible = False
        # self.heart.texture = HEART
        
    