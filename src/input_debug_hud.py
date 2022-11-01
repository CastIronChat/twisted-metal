from typing import List
from player_input import PlayerInput
import arcade
from arcade import Text


class InputDebugHud:

    player_input: PlayerInput

    controls: List[str]

    __text: Text

    def __init__(self, player_input: PlayerInput):
        self.player_input = player_input
        self.controls = [
            "x_axis",
            "y_axis",
            "rx_axis",
            "ry_axis",
            "accelerate_button",
            "brake_button",
            "primary_fire_button",
            "secondary_fire_button",
        ]
        self.__text = Text(
            "Text Drawing Examples",
            0,
            500,
            arcade.color.BLACK,
            16,
            multiline=True,
            width=9999,  # Only wrap on explicit newline
        )

    def get_readout(self):
        lines = [
            f"{control}: {getattr(self.player_input, control).value}"
            for control in self.controls
        ]
        return "\n".join(lines)

    def draw(self):
        self.__text.text = self.get_readout()
        self.__text.draw()
