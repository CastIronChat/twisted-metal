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
        self.hud_x = hud_x - 20
        self.hud_y = hud_y - 60
        self.hearts = []
        # self.heart = arcade.Sprite(texture=HEART, scale=1.5)
        # self.sprite_lists.huds.append(self.heart)
        # self.heart.center_x = self.hud_x
        # self.heart.center_y = self.hud_y
        # for x in self.game_state_mode.lives:
            # self.hearts.append(self.heart[x])

        # x = self.lives
        # while x > 0:
        #     self.hearts.append(self.heart)
        #     x -= 1

        # print(self.hearts)
        # for y in self.hearts:
        #     self.sprite_lists.huds.append(y)

        for z in range(0, self.starting_lives):
            heart = arcade.Sprite(texture=HEART, scale=1.1)
            heart.center_x = self.hud_x + (z * 15)
            heart.center_y = self.hud_y
            self.hearts.append(heart)
            self.sprite_lists.huds.append(heart)


        # self.sprite_lists.huds.append(self.hearts)

            # use .scene.add_sprite instead of direct to sprite_lits?

    def update(self):
        print('LH GSM', self.game_state_mode.lives)
        # if self.game_state_mode.lives >= 1:
        #     self.heart.visible = True
        # elif self.game_state_mode.lives < 1:
        #     self.heart.visible = False
        # self.heart.texture = HEART
        for x in range(self.starting_lives):
            if x <= self.game_state_mode.lives - 1:
                self.hearts[x].visible = True
            else:
                self.hearts[x].visible = False




    