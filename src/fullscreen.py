from __future__ import annotations

from arcade import Window

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, START_FULLSCREEN
from global_input import GlobalInput


class FullscreenController:
    """
    Turns fullscreen on and off, both at the start of the game, and when
    keybinds are hit to toggle it.  Sets viewport to preserve aspect ratio.

    Viewport is described in game coordinates.  It is scaled to match the
    screen's resolution.  This means our game's logic is written against a
    fixed screen resolution declared in `constants.py`.  The GPU stretches the
    fixed resolution to fill the physical screen.

    For example, if the game is coded against a resolution of 800 by 600, and
    its running on a 1920x1080 television, then we set the viewport to:

        left = -240
        right = 1040
        bottom = 0
        top = 600
    """

    def __init__(self, window: Window, input: GlobalInput):
        self._window = window
        self._input = input
        self.is_fullscreen = START_FULLSCREEN
        self._dirty = True

    def update(self):
        if self._input.fullscreen_toggle.pressed:
            self.is_fullscreen = not self.is_fullscreen
            self._dirty = True
        if self._dirty:
            self._update_viewport()
            self._dirty = False

    def _update_viewport(self):
        if self.is_fullscreen:
            self._window.set_fullscreen(True)
            (w, h) = self._window.get_size()
            w_ratio = w / SCREEN_WIDTH
            h_ratio = h / SCREEN_HEIGHT
            if w_ratio > h_ratio:
                # black bars on left and right
                w_scaled = w * SCREEN_HEIGHT / h
                bar_size = (w_scaled - SCREEN_WIDTH) / 2
                print((w_scaled, -bar_size, SCREEN_WIDTH + bar_size, 0, SCREEN_HEIGHT))
                self._window.set_viewport(
                    -bar_size, SCREEN_WIDTH + bar_size, 0, SCREEN_HEIGHT
                )
            else:
                # black bars on top and bottom
                h_scaled = h * SCREEN_WIDTH / w
                bar_size = h_scaled / 2
                self._window.set_viewport(
                    0, SCREEN_WIDTH, -bar_size, SCREEN_HEIGHT + bar_size
                )
        else:
            self._window.set_fullscreen(False)
            self._window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
