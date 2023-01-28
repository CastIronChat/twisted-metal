from __future__ import annotations

import random
from typing import Any, Sequence

from arena.spawn_point import SpawnPoint
from player_input import PlayerInput
from rounds.round_controller import RoundController
from sprite_lists import SpriteLists
from vehicle import Vehicle


class Player:

    round_controller: RoundController
    "Necessary for player to notify the round controller and game mode about relevant events"

    game_mode_state: Any

    def __init__(
        self,
        input: PlayerInput,
        sprite_lists: SpriteLists,
        initial_spawn_point: SpawnPoint,
        spawn_points: Sequence[SpawnPoint],
        player_index: int,
    ):
        self.input = input
        self.vehicle = Vehicle(self, sprite_lists, player_index)
        self._initial_spawn_point = initial_spawn_point
        self._spawn_points = spawn_points
        self.alive: bool = True
        self.controls_active: bool = False
        "Is false between rounds, when you're not allowed to move yet"
        self.allowed_to_respawn: bool = True
        """
        Is set false by game mode if you've run out of lives, or whatever other
        criteria that mode has
        """
        self.respawn_time_passed: float = 0
        self.time_to_respawn: float = 5
        self.player_index = player_index

    def __hash__(self) -> int:
        return self.player_index

    def update(self, delta_time: float):
        self.vehicle.update(delta_time)
        #
        # Wait for Respawn
        #
        if not self.alive and self.allowed_to_respawn:
            self.respawn_time_passed = self.respawn_time_passed + delta_time
            if self.respawn_time_passed > self.time_to_respawn:
                self.respawn()

    def round_start_spawn(self):
        """
        Spawning that happens at round start
        """
        self._spawn(self._initial_spawn_point)

    def respawn(self):
        """
        Spawning that happens mid-round, following a death.
        """
        chosen_spawn_point = self._spawn_points[
            random.randrange(len(self._spawn_points))
        ]
        self._spawn(chosen_spawn_point)

    def _spawn(self, spawn_point: SpawnPoint):
        self.alive = True
        self.respawn_time_passed = 0
        self.vehicle.respawn(spawn_point.transform)
