from typing import List

import arcade
from arena.arena import Arena
from arena.arena_loader import load_arena_by_name

from constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH, TICK_DURATION
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
        self.physics_engine = None
        arcade.set_background_color(arcade.color.AMAZON)
        self.player_manager = PlayerManager(self.keyboard)
        self.arena: Arena

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

        self.arena = load_arena_by_name("default")
        self.arena.init_for_drawing()

    def on_draw(self):
        # clear screen
        self.clear()
        self.arena.draw()
        self.all_sprites.draw()
        for player in self.player_manager.players:
            player.draw()
        self.input_debug_hud.draw()

    def on_update(self, delta_time):
        # Pretty sure this does animation updates, in case any of the sprites
        # Have animations

        for player in self.player_manager.players:
            player.update(delta_time)

        self.hud.update()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
