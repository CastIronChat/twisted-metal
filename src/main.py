from typing import List

import arcade
from pyglet.input import ControllerManager

from hud import Hud
from input_debug_hud import InputDebugHud
from player import Player
from player_manager import PlayerManager

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "John Deer Clown School"


class MyGame(arcade.Window):
    # Declare class members; enables tab-completion
    all_sprites: arcade.SpriteList = None
    input_debug_hud: InputDebugHud = None
    controller_manager: ControllerManager = None

    def __init__(self, width, height, title):
        super().__init__(width, height, title, enable_polling=True)

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

    def on_draw(self):
        # clear screen
        self.clear()
        self.all_sprites.draw()
        self.input_debug_hud.draw()

    def on_update(self, delta_time):
        # Pretty sure this does animation updates, in case any of the sprites
        # Have animations

        # Get Sprites from player to add or remove from sprite list
        for player in self.player_manager.players:
            (added1, removed1, added2, removed2) = player.update(delta_time)
            if added1 is not None:
                self.all_sprites.append(added1)
            if added2 is not None:
                self.all_sprites.append(added2)
            if removed1 is not None:
                self.all_sprites.remove(removed1)
            if removed2 is not None:
                self.all_sprites.remove(removed2)

        self.all_sprites.update()
        self.hud.update()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
