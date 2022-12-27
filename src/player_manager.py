from __future__ import annotations

from typing import List

import arcade
from pyglet.input import ControllerManager
from pyglet.window.key import KeyStateHandler

from arena.arena import Arena
from constants import (
    FRAMES_OF_INPUT_DELAY,
    KEYBOARD_PLAYER_ALSO_USES_A_CONTROLLER,
    KEYBOARD_PLAYER_INDEX,
    PLAYER_COUNT,
    START_WITH_ALTERNATE_CONTROLLER_LAYOUT,
)
from iron_math import set_sprite_location
from player import Player
from player_input import EMPTY_INPUT_SNAPSHOT, PlayerInput, PlayerInputSnapshot
from player_input_layouts import bind_to_keyboard, set_controller_layout
from sprite_lists import SpriteLists


class PlayerManager:
    """
    Responsible for allocating Players when the game starts,
    and maintaining a list of all players.

    In the future, may also be responsible for facilitating players joining /
    leaving the match.
    """

    def __init__(self, keyboard: KeyStateHandler) -> None:
        self._players: list[Player] = []
        self._keyboard = keyboard
        self._controller_manager: ControllerManager
        self._did_setup = False

    @property
    def players(self):
        """
        Guaranteed to never be replaced, only mutated.
        References to this list can be passed elsewhere so that other code
        can access the current players.
        """
        return self._players

    def setup(
        self,
        sprite_lists: SpriteLists,
        arena: Arena,
    ):
        if self._did_setup:
            raise Exception("Already setup; cannot setup twice")
        self._did_setup = True

        _controller_manager = ControllerManager()
        controllers = _controller_manager.get_controllers()

        for player_index in range(0, PLAYER_COUNT):
            controller = None
            controller_index = player_index
            if (
                player_index > KEYBOARD_PLAYER_INDEX
                and not KEYBOARD_PLAYER_ALSO_USES_A_CONTROLLER
            ):
                controller_index -= 1
            can_use_controller = KEYBOARD_PLAYER_ALSO_USES_A_CONTROLLER or (
                player_index != KEYBOARD_PLAYER_INDEX
            )
            if can_use_controller and len(controllers) > controller_index:
                print(controller_index)
                controller = controllers[controller_index]
                controller.open()
            player_input = PlayerInput(self._keyboard, controller)
            player_input.update_from_snapshot(EMPTY_INPUT_SNAPSHOT)
            if player_index == KEYBOARD_PLAYER_INDEX:
                bind_to_keyboard(player_input)
            set_controller_layout(player_input, START_WITH_ALTERNATE_CONTROLLER_LAYOUT)
            player = Player(
                player_input, sprite_lists, arena.initial_spawn_points, player_index
            )
            self.players.append(player)

        self.player_input_buffers = [
            [PlayerInputSnapshot() for i in range(FRAMES_OF_INPUT_DELAY)]
            for player in self._players
        ]

    def update_inputs(self):
        """
        Must be called at the *start* of every frame, before calling other
        gameplay logic.  Does internal input-handling bookkeeping.
        """
        for (index, player) in enumerate(self.players):
            # player_input_buffer = self.player_input_buffers[index]
            # player_input_buffer.insert(0, player.input.capture_physical_inputs())
            # snapshot_to_apply = player_input_buffer.pop()
            # player.input.update_from_snapshot(snapshot_to_apply)
            # player.input.update()
            if player.input.debug_2.pressed or player.input.debug_2.released:
                # xor
                alternate = (
                    player.input.debug_2.toggle
                    != START_WITH_ALTERNATE_CONTROLLER_LAYOUT
                )
                set_controller_layout(player.input, alternate)
