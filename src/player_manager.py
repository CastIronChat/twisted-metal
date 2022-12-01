from typing import List, cast
import arcade

from pyglet.input import ControllerManager, Controller
from pyglet.window.key import KeyStateHandler
from arena.arena import Arena
from constants import START_WITH_ALTERNATE_CONTROLLER_LAYOUT
from iron_math import move_sprite

from player import Player
from player_input import (
    PlayerInput,
    bind_to_keyboard,
    set_controller_layout,
)

PLAYER_COUNT = 4
KEYBOARD_PLAYER_INDEX = 0
KEYBOARD_PLAYER_ALSO_USES_A_CONTROLLER = True
"""
If false, keyboard player will be controlled by keyboard, *not* a controller.
Useful if you want to debug two players and you only have one controller.
"""


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
        projectile_sprite_list: arcade.SpriteList,
        beam_sprite_list: arcade.SpriteList,
        player_sprite_list: arcade.SpriteList,
        arena: Arena,
    ):
        if self._did_setup:
            raise Exception("Already setup; cannot setup twice")
        self._did_setup = True

        _controller_manager = ControllerManager()
        controllers = cast(List[Controller], _controller_manager.get_controllers())

        for player_index in range(0, PLAYER_COUNT):
            controller = None
            controller_index = player_index
            if (
                player_index > KEYBOARD_PLAYER_INDEX
                and not KEYBOARD_PLAYER_ALSO_USES_A_CONTROLLER
            ):
                controller_index -= 1
            if len(controllers) > controller_index:
                controller = controllers[controller_index]
                controller.open()
            player_input = PlayerInput(self._keyboard, controller)
            if player_index == KEYBOARD_PLAYER_INDEX:
                bind_to_keyboard(player_input)
            set_controller_layout(player_input, START_WITH_ALTERNATE_CONTROLLER_LAYOUT)
            player = Player(player_input, projectile_sprite_list, beam_sprite_list)
            spawn_point = arena.initial_spawn_points[player_index]
            move_sprite(player.sprite, spawn_point.transform)
            player_sprite_list.append(player.sprite)
            self.players.append(player)

    def update_inputs(self):
        """
        Must be called at the *start* of every frame, before calling other
        gameplay logic.  Does internal input-handling bookkeeping.
        """
        for player in self.players:
            player.input.update()
            if player.input.debug_2.pressed or player.input.debug_2.released:
                # xor
                alternate = (
                    player.input.debug_2.toggle
                    != START_WITH_ALTERNATE_CONTROLLER_LAYOUT
                )
                set_controller_layout(player.input, alternate)
