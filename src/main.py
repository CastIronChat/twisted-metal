from __future__ import annotations

from typing import List

import arcade

from arena.arena import Arena
from arena.arena_loader import load_arena_by_name
from bullet import bullet_behavior
from collision import projectile_hits_player, projectile_hits_wall
from constants import (
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    TICK_DURATION,
    USE_DEBUGGER_TIMING_FIXES,
)
from hud import Hud
from input_debug_hud import InputDebugHud
from player_manager import PlayerManager
from sprite_lists import SpriteLists


class MyGame(arcade.Window):
    # Declare class members; enables tab-completion
    all_sprites: arcade.SpriteList = None
    input_debug_hud: InputDebugHud = None
    sprite_lists: SpriteLists

    def __init__(self, width: int, height: int, title: str):
        super().__init__(
            width, height, title, enable_polling=True, update_rate=TICK_DURATION
        )
        self.physics_engine = None
        arcade.set_background_color(arcade.color.AMAZON)
        self.player_manager = PlayerManager(self.keyboard)
        self.sprite_lists = SpriteLists()
        self.arena: Arena

    def setup(self):
        self.all_sprites = arcade.SpriteList()
        self.projectile_sprite_list = arcade.SpriteList()

        # Arena
        self.arena = load_arena_by_name("default")
        self.arena.init_for_drawing(self.sprite_lists)

        # Players
        self.player_manager.setup(
            self.sprite_lists,
            self.arena,
        )

        # Debug UI for input handling
        self.input_debug_hud = InputDebugHud(
            [player.input for player in self.player_manager.players]
        )

        # Player Huds
        self.hud = Hud(self.player_manager.players)
        for sprite in self.hud.hud_sprite_list:
            self.all_sprites.append(sprite)

    def on_update(self, delta_time):
        # Arcade engine has a quirk where, in the debugger, it calls `on_update` twice back-to-back,
        # then `on_draw` twice, and so on.
        # We avoid this bug by ignoring the `on_update()` call from arcade, instead calling it ourselves
        # from `on_draw`
        if not USE_DEBUGGER_TIMING_FIXES:
            self.our_update(delta_time)

    def our_update(self, delta_time: float):
        # Pretty sure this does animation updates, in case any of the sprites
        # Have animations
        self.player_manager.update_inputs()
        for player in self.player_manager.players:
            player.update(delta_time)
        bullet_behavior(
            delta_time,
            self.sprite_lists,
        )
        projectile_hits_wall(self.sprite_lists)
        projectile_hits_player(self.sprite_lists)
        self.hud.update()

    def on_draw(self):
        if USE_DEBUGGER_TIMING_FIXES:
            self.our_update(TICK_DURATION)

        # clear screen
        self.clear()
        self.sprite_lists.draw()
        for player in self.player_manager.players:
            player.draw()
        self.input_debug_hud.draw()
        self.all_sprites.draw()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
