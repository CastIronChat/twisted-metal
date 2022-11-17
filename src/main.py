from typing import List

import arcade

from constants import (
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    TICK_DURATION,
    USE_DEBUGGER_TIMING_FIXES,
)
from input_debug_hud import InputDebugHud

from player_manager import PlayerManager
from hud import Hud


class MyGame(arcade.Window):
    # Declare class members; enables tab-completion
    all_sprites: arcade.SpriteList = None
    input_debug_hud: InputDebugHud = None

    def __init__(self, width, height, title):
        super().__init__(
            width, height, title, enable_polling=True, update_rate=TICK_DURATION
        )

        arcade.set_background_color(arcade.color.AMAZON)
        self.player_manager = PlayerManager(self.keyboard)

    def setup(self):
        self.all_sprites = arcade.SpriteList()

        # Players
        self.player_manager.setup()
        for player in self.player_manager.players:
            self.all_sprites.append(player.sprite)

        # Debug UI for input handling
        self.input_debug_hud = InputDebugHud(
            [player.input for player in self.player_manager.players]
        )

        # Player Huds
        self.hud = Hud(self.player_manager.players)
        for sprite in self.hud.hud_sprite_list:
            self.all_sprites.append(sprite)

    def on_update(self, delta_time):
        # In the debugger, we intentionally ignore the on_update() call we get from arcade engine.
        # Instead, we call our own our_update() within on_draw()
        # This avoids a known issue where debugger pauses can cause `on_update`` and `on_draw`` to happen in this order:
        #   update
        #   update
        #   draw
        #   draw
        #   update
        #   update
        #   draw
        #   draw
        #   ...and so on.  Each is called twice, back-to-back.
        if not USE_DEBUGGER_TIMING_FIXES:
            self.our_update(delta_time)

    def our_update(self, delta_time):
        # Pretty sure this does animation updates, in case any of the sprites
        # Have animations

        for player in self.player_manager.players:
            player.update(delta_time)

        self.hud.update()

    def on_draw(self):
        if USE_DEBUGGER_TIMING_FIXES:
            self.our_update(TICK_DURATION)

        # clear screen
        self.clear()
        self.all_sprites.draw()
        for player in self.player_manager.players:
            player.draw()
        self.input_debug_hud.draw()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
