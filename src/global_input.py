from __future__ import annotations

from typing import Optional

from arcade import key
from pyglet.input import Controller
from pyglet.window.key import KeyStateHandler

from player_input import VirtualButton


class GlobalInput:
    def __init__(self, keys: KeyStateHandler, controller: Optional[Controller]) -> None:
        self._keys = keys
        self._controller = controller
        self.fullscreen_toggle = VirtualButton(keys, controller)

    def update(self):
        self.fullscreen_toggle._update()


def bind_global_inputs_to_keyboard(global_input: GlobalInput):
    global_input.fullscreen_toggle.key = key.F11
