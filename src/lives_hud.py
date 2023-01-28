from __future__ import annotations

from rounds.game_modes.stock import StockGameModePlayerState


class LivesHud:
    def __init__(
        self, game_mode_state: StockGameModePlayerState, hud_x: int, hud_y: int
    ):
        self.game_mode_state = game_mode_state
        self.hud_x = hud_x
        self.hud_y = hud_y


    def update(self):
        pass
    