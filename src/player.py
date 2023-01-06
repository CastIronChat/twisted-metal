from __future__ import annotations

import random

from arena.spawn_point import SpawnPoint
from player_input import PlayerInput
from sprite_lists import SpriteLists
from vehicle import Vehicle


class Player:
    def __init__(
        self,
        input: PlayerInput,
        sprite_lists: SpriteLists,
        initial_spawn_points: list[SpawnPoint],
        player_index: int,
    ):
        self.input = input
        self.vehicle = Vehicle(self, sprite_lists)
        self.vehicle.location = initial_spawn_points[player_index].transform
        self.alive: bool = True
        self.respawn_time_passed: float = 0
        self.time_to_respawn: float = 5
        self.initial_spawn_points = initial_spawn_points

    def update(self, delta_time: float):
        self.vehicle.update(delta_time)
        #
        # Wait for Respawn
        #
        if not self.alive:
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
