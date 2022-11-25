from typing import List
from player_input import PlayerInput
import arcade
from arcade import Text


class InputDebugHud:

    player_inputs: List[PlayerInput]

    controls: List[str]

    __text: Text

    def __init__(self, player_inputs: List[PlayerInput]):
        self.player_inputs = player_inputs
        self.controls = [
            "x_axis",
            "y_axis",
            "rx_axis",
            "ry_axis",
            "accelerate_axis",
            "brake_axis",
            "primary_fire_button",
            "secondary_fire_button",
            "swap_weapons_button",
            "reload_button",
            "debug_1",
            "debug_2",
            "debug_3",
            "debug_4",
        ]
        self.__text = Text(
            "Text Drawing Examples",
            0,
            550,
            arcade.color.WHITE,
            12,
            multiline=True,
            width=9999,  # Only wrap on explicit newline
        )

    def get_readout(self):
        lines = []
        for (index, player_input) in enumerate(self.player_inputs):
            lines += [f"Player #{index + 1}: {player_input.layout_name} layout"]
            lines += [
                f"{control}: {getattr(player_input, control).value}"
                for control in self.controls
            ]
        return "\n".join(lines)

    def draw(self):
        self.__text.text = self.get_readout()
        self.__text.draw()
