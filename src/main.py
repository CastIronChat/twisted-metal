from msilib.schema import Control
import arcade
from input_debug_hud import InputDebugHud

from player import Player
from player_input import PlayerInput, bind_to_keyboard, set_default_controller_layout
from pyglet.input import ControllerManager

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "John Deer Clown School"


class MyGame(arcade.Window):
    # Declare class members; enables tab-completion
    allSprites: arcade.SpriteList = None
    player1: Player = None
    player1_input: PlayerInput = None
    player2_input: PlayerInput = None
    input_debug_hud: InputDebugHud = None
    controller_manager: ControllerManager = None

    def __init__(self, width, height, title):
        super().__init__(width, height, title, enable_polling=True)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.allSprites = arcade.SpriteList()

        # Input handling
        self.controller_manager = ControllerManager()
        controllers = self.controller_manager.get_controllers()
        player1_controller = None
        if len(controllers) >= 1:
            player1_controller = controllers[0]
            player1_controller.open()
        self.player1_input = PlayerInput(self.keyboard, player1_controller)
        bind_to_keyboard(self.player1_input)
        set_default_controller_layout(self.player1_input)

        player2_controller = None
        if len(controllers) >= 2:
            player2_controller = controllers[1]
            player2_controller.open()

        self.player2_input = PlayerInput(self.keyboard, player2_controller)
        set_default_controller_layout(self.player2_input)

        # Debug UI for input handling
        self.input_debug_hud = InputDebugHud([self.player1_input, self.player2_input])

        # Player
        self.player1 = Player(self.player1_input)
        self.player2 = Player(self.player2_input)

        self.allSprites.append(self.player1.sprite)
        self.allSprites.append(self.player2.sprite)

    def on_draw(self):
        # clear screen
        self.clear()
        self.allSprites.draw()
        self.input_debug_hud.draw()

    def on_update(self, delta_time):
        # Pretty sure this does animation updates, in case any of the sprites
        # Have animations

        # Get Sprites from player to add or remove from sprite list
        (added1, removed1, added2, removed2) = self.player1.update(delta_time)
        if added1 is not None:
            self.allSprites.append(added1)
        if added2 is not None:
            self.allSprites.append(added2)
        if removed1 is not None:
            self.allSprites.remove(removed1)
        if removed2 is not None:
            self.allSprites.remove(removed2)

        self.allSprites.update()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
