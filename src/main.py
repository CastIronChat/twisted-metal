import arcade

from player import Player
from player_input import PlayerInput

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Whatever I Want"


class MyGame(arcade.Window):
    # Declare class members; enables tab-completion
    allSprites: arcade.SpriteList
    player1: Player
    player1Input: PlayerInput

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)
        self.allSprites = None

    def setup(self):
        self.allSprites = arcade.SpriteList()

        self.input = PlayerInput()
        self.player1 = Player(self.input)
        self.allSprites.append(self.player1.sprite)

    def on_draw(self):
        # clear screen
        self.clear()
        self.allSprites.draw()

    def on_update(self, delta_time):
        # Pretty sure this does animation updates, in case any of the sprites
        # Have animations
        self.allSprites.update()

        self.player1.update(delta_time)

    # All these IO functions come from the arcade boilerplate.  I'm not sure if
    # there are any good patterns out there for IO mapping.  Would be nice to
    # abstract inputs so we don't have hard-coded names of keyboard keys all
    # over the code, especially when handling input for multiple players.
    # I'm also not sure if this handles gamepad input at all.
    def on_key_press(self, key, key_modifiers):
        input = self.player1.input
        if key == arcade.key.LEFT:
            input.left = True
        if key == arcade.key.RIGHT:
            input.right = True
        if key == arcade.key.UP:
            input.up = True
        if key == arcade.key.DOWN:
            input.down = True

    def on_key_release(self, key, key_modifiers):
        input = self.player1.input
        if key == arcade.key.LEFT:
            input.left = False
        if key == arcade.key.RIGHT:
            input.right = False
        if key == arcade.key.UP:
            input.up = False
        if key == arcade.key.DOWN:
            input.down = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()