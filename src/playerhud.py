from __future__ import annotations

import arcade

from lives_hud import LivesHud
from player import Player
from rounds.game_modes.stock import StockGameModePlayerState
from rounds.game_modes.empty import EmptyGameModePlayerState
from textures import RESPAWN_COUNTDOWN
from sprite_lists import SpriteLists



class PlayerHud:
    width: int = 100
    health_width: int = 100
    height: int = 4
    background_sprite: arcade.Sprite
    health_sprite: arcade.Sprite
    full_color: arcade.Color = arcade.color.GREEN
    background_color: arcade.Color = arcade.color.RED
    player: Player
    hud_x: int
    hud_y: int
    player_hud_avatar: arcade.Sprite

    def __init__(
        self, player: Player, hud_x: int, hud_y: int, player_hud_avatar: arcade.Sprite, sprite_lists: SpriteLists
    ):
        self.player = player
        self.hud_x = hud_x
        self.hud_y = hud_y
        respawn_counter_x_offset = 50
        below_health_bar_offset = 30

        self.player_respawn_countdown_sprite = arcade.Sprite()
        self.player_respawn_countdown_sprite.center_x = hud_x + respawn_counter_x_offset
        self.player_respawn_countdown_sprite.center_y = hud_y - below_health_bar_offset

        self.background_sprite = arcade.SpriteSolidColor(
            self.width, self.height, self.background_color
        )
        self.background_sprite.center_x = hud_x
        self.background_sprite.center_y = hud_y

        self.player_hud_avatar = player_hud_avatar
        self.player_hud_avatar.center_x = hud_x
        self.player_hud_avatar.center_y = hud_y - below_health_bar_offset

        self.health_sprite = arcade.SpriteSolidColor(
            self.width, self.height, self.full_color
        )
        self.health_sprite.center_x = hud_x
        self.health_sprite.center_y = hud_y

        if isinstance(self.player.game_mode_state, StockGameModePlayerState):
            self.lives_hud = LivesHud(self.player.game_mode_state, hud_x, hud_y, sprite_lists)
        elif isinstance(self.player.game_mode_state, EmptyGameModePlayerState):
            self.lives_hud = LivesHud(self.player.game_mode_state, hud_x, hud_y, sprite_lists)

    def update(self):

        # changes healthbar length based on current ratio and left sets healthbar
        if self.player.vehicle.health > 0:
            ratio = self.player.vehicle.health / 100
            self.health_sprite.width = self.health_width * ratio
            self.health_sprite.left = self.hud_x - (self.health_width // 2)
        elif self.player.vehicle.health <= 0:
            self.health_sprite.width = 0.1
            self.health_sprite.left = self.hud_x - (self.health_width // 2)
        # creates respawn timer on player's hud
        if (
            self.player.alive == False
            and len(RESPAWN_COUNTDOWN) >= self.player.time_to_respawn
            and self.player.allowed_to_respawn
        ):
            self.player_respawn_countdown_sprite.visible = True
            self.player_respawn_countdown_sprite.texture = RESPAWN_COUNTDOWN[
                self.player.time_to_respawn - round(self.player.respawn_time_passed)
            ]
        else:
            self.player_respawn_countdown_sprite.visible = False 
        
        self.lives_hud.update()
