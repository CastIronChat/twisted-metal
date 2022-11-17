from typing import List

from pyglet.input import ControllerManager
from pyglet.window.key import KeyStateHandler

from player import Player
from player_input import PlayerInput, bind_to_keyboard, set_default_controller_layout

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

    def setup(self):
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
            if len(controllers) > controller_index:
                controller = controllers[controller_index]
                controller.open()
            player_input = PlayerInput(self._keyboard, controller)
            if player_index == KEYBOARD_PLAYER_INDEX:
                bind_to_keyboard(player_input)
            set_default_controller_layout(player_input)
            player = Player(player_input)
            self.players.append(player)
