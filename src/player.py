from __future__ import annotations

import random

from arena.spawn_point import SpawnPoint
from player_input import PlayerInput
from rounds.round_controller import RoundController
from sprite_lists import SpriteLists
from vehicle import Vehicle


class Player:

    round_controller: RoundController
    "Necessary for player to notify the round controller and game mode about relevant events"

    def __init__(
        self,
        input: PlayerInput,
        sprite_lists: SpriteLists,
        initial_spawn_points: list[SpawnPoint],
        player_index: int,
    ):
        self.input = input
        self.vehicle = Vehicle(self, sprite_lists, player_index)
        self.vehicle.location = initial_spawn_points[player_index].transform
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
        self.initial_spawn_points = initial_spawn_points
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

    def respawn(self):
        self.alive = True
        self.respawn_time_passed = 0
        chosen_spawn_point = self.initial_spawn_points[
            random.randrange(len(self.initial_spawn_points))
        ].transform
        self.vehicle.respawn(chosen_spawn_point)
