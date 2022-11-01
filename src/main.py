import arcade
from input_debug_hud import InputDebugHud

from player import Player
from player_input import PlayerInput, bind_to_keyboard

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "John Deer Clown School"


class MyGame(arcade.Window):
    # Declare class members; enables tab-completion
    allSprites: arcade.SpriteList = None
    player1: Player = None
    player1Input: PlayerInput = None
    player1InputDebugHud: InputDebugHud = None

    def __init__(self, width, height, title):
        super().__init__(width, height, title, enable_polling=True)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.allSprites = arcade.SpriteList()
        self.player1Input = PlayerInput(self.keyboard)
        self.player1InputDebugHud = InputDebugHud(self.player1Input)
        # self.input.bind_to_controller(1)
        bind_to_keyboard(self.player1Input)
        self.player1 = Player(self.player1Input)
        self.allSprites.append(self.player1.sprite)

    def on_draw(self):
        # clear screen
        self.clear()
        self.allSprites.draw()
        self.player1InputDebugHud.draw()

    def on_update(self, delta_time):
        # Pretty sure this does animation updates, in case any of the sprites
        # Have animations
        self.allSprites.update()

        self.player1.update(delta_time)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
