from __future__ import annotations

import math
from math import radians
from typing import TYPE_CHECKING, Generator, cast

from arcade import Text

from arena.arena import Arena
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import add_vec, polar_to_cartesian
from rounds.game_modes.game_mode import GameMode
from sprite_lists import SpriteLists

if TYPE_CHECKING:
    from player import Player


COUNTDOWN_SECONDS = 3.0
"Number of seconds of countdown before round starts"
GO_DISPLAY_DURATION = 0.5
"Number of seconds to show GO after 3-2-1 countdown"
VICTORY_LAP_DURATION = 5.0


class RoundController:
    """
    A single `RoundController` is responsible for starting and ending each round
    of the game.

    For example, if there's a 3-2-1 countdown timer to start the round, the `RoundController`
    can handle that, locking everyone's controls and unlocking when it hits "Go"

    `RoundController` talks to `GameMode`.
    `GameMode` is responsible for deciding when the round ends.
    Once `GameMode` says the round is over, `RoundController` handles the flashy stuff:
    "Player X Wins!" graphics, camerawork, etc.
    """

    def __init__(
        self,
        game_mode: GameMode,
        players: list[Player],
        arena: Arena,
        sprite_lists: SpriteLists,
    ) -> None:
        self.game_mode = game_mode
        self._players = players
        # In the future, we might have a mechanism to change the arena between rounds
        self._arena = arena
        self._sprite_lists = sprite_lists

        hud_rotation_deg = 0
        # Arcade has pesky requirements about the x/y of a Text element
        (hud_x, hud_y) = add_vec(
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            polar_to_cartesian(-SCREEN_WIDTH / 2, radians(hud_rotation_deg)),
        )
        print(hud_x, hud_y)
        print(polar_to_cartesian(-SCREEN_WIDTH / 2, radians(hud_rotation_deg)))
        self._hud = Text(
            "",
            hud_x,
            hud_y,
            width=SCREEN_WIDTH,
            font_size=32,
            align="center",
            rotation=hud_rotation_deg,
            bold=True,
        )
        self._generator = None

    def update(self, delta_time: float):
        if not self._generator:
            self._generator = self._state_machine()
            self._generator.send(cast(float, None))
        try:
            self._generator.send(delta_time)
        except StopIteration:
            self._generator = None

        self.game_mode.update(delta_time)

    # TODO Rewrite to not be a generator; is not worth the complexity
    def _state_machine(self) -> Generator[None, float, None]:
        countdown_time = COUNTDOWN_SECONDS
        delta_time = yield

        # Init for new round and reset from the previous round
        for player in self._players:
            player.allowed_to_respawn = True
            player.controls_active = False
        self.game_mode.on_round_init(self._players, self._arena, self._sprite_lists)

        while countdown_time > 0:
            delta_time = yield
            countdown_time -= delta_time
            display_countdown_number = math.ceil(countdown_time)
            self._hud.text = display_countdown_number

        # Timer reached zero
        # Start the game
        self._hud.text = "GO"
        for player in self._players:
            player.controls_active = True
        self.game_mode.on_round_start()

        while True:
            delta_time = yield

            # Hide "GO" text after a delay
            if countdown_time > -GO_DISPLAY_DURATION:
                countdown_time -= delta_time
                if countdown_time <= -GO_DISPLAY_DURATION:
                    self._hud.text = ""
            winner = self.game_mode.get_winner()
            if winner:
                break

        # We have a winner
        self._hud.text = f"Player {winner.player_index + 1} Wins!"
        victory_lap_countdown = VICTORY_LAP_DURATION
        while victory_lap_countdown > 0:
            delta_time = yield
            victory_lap_countdown -= delta_time

        self._hud.text = ""

    def draw(self):
        self._hud.draw()
