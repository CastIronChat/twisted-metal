from __future__ import annotations

from rounds.game_modes.stock import StockGameModePlayerState
from rounds.game_modes.empty import EmptyGameModePlayerState


class LivesHud:
    def __init__(
        self, game_mode_state, hud_x: int, hud_y: int
    ):
        self.game_mode_state = game_mode_state
        self.hud_x = hud_x
        self.hud_y = hud_y


    def update(self):
        pass
    