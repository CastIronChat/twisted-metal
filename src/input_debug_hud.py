from __future__ import annotations

from typing import List

import arcade
from arcade import Text

from constants import DRAW_DRIVE_MODE_DEBUG_HUD, DRAW_INPUT_DEBUG_HUD
from player import Player
from player_input import PlayerInput


class DebugHud:
    def __init__(self, players: List[Player]):
        self.players = players
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
        for (index, player) in enumerate(self.players):
            player_input = player.input
            lines += [f"Player #{index + 1}"]
            if DRAW_DRIVE_MODE_DEBUG_HUD:
                lines += [f"Drive mode: {player.drive_mode.name}"]
            if DRAW_INPUT_DEBUG_HUD:
                lines += [f"Layout: {player_input.layout_name}"]
                lines += [
                    f"{control}: {getattr(player_input, control).value}"
                    for control in self.controls
                ]
        return "\n".join(lines)

    def draw(self):
        if DRAW_INPUT_DEBUG_HUD or DRAW_DRIVE_MODE_DEBUG_HUD:
            self.__text.text = self.get_readout()
            self.__text.draw()
