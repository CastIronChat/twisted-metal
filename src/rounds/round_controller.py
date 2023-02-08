from __future__ import annotations

import math
from enum import Enum
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


class State(Enum):
    INIT = 0
    COUNTDOWN = 1
    PLAYING = 2
    VICTORY_LAP = 3


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

    # State machine
    _state: State
    _countdown_time: float
    _victory_lap_countdown: float

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

        self._state = State.INIT

    def update(self, delta_time: float):
        # Implemented as a state machine.  `self._state` determines what phase we are in.
        # Each frame, we update according to current state, and conditionally move to the next state
        # by assigning `self._state`

        if self._state == State.INIT:
            self._countdown_time = COUNTDOWN_SECONDS
            self._hud.text = ""

            # Init for new round and reset from the previous round
            for player in self._players:
                player.round_start_spawn()
                player.allowed_to_respawn = True
                player.controls_active = False
            self.game_mode.on_round_init(self._players, self._arena, self._sprite_lists)

            self._state = State.COUNTDOWN

        if self._state == State.COUNTDOWN:
            # 3-2-1 countdown timer
            self._countdown_time -= delta_time

            if self._countdown_time > 0:
                display_countdown_number = math.ceil(self._countdown_time)
                self._hud.text = display_countdown_number

            else:
                # Timer reached zero
                # Start the game
                self._hud.text = "GO"
                for player in self._players:
                    player.controls_active = True
                self.game_mode.on_round_start()

                self._state = State.PLAYING

        if self._state == State.PLAYING:
            # Wait until we have a winner

            # Hide "GO" text after a delay
            self._countdown_time -= delta_time
            if self._countdown_time > -GO_DISPLAY_DURATION:
                self._countdown_time -= delta_time
                if self._countdown_time <= -GO_DISPLAY_DURATION:
                    self._hud.text = ""

            winner = self.game_mode.get_winner()
            if winner:
                # We have a winner
                # Display a banner and give them time for a victory lap
                self._hud.text = f"Player {winner.player_index + 1} Wins!"
                self._victory_lap_countdown = VICTORY_LAP_DURATION

                self._state = State.VICTORY_LAP

        if self._state == State.VICTORY_LAP:
            if self._victory_lap_countdown > 0:
                self._victory_lap_countdown -= delta_time

            else:
                # Victory lap finished
                self._state = State.INIT

        self.game_mode.update(delta_time)

    def draw(self):
        self._hud.draw()
