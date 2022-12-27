from __future__ import annotations

import math
from typing import List

import arcade

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from driving.create_drive_modes import create_drive_modes
from iron_math import get_sprite_location, randrange, set_sprite_location
from linked_sprite import LinkedSprite
from movement_controls import MovementControls
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
        self.player_health = 100
        self.alive = True
        self.respawn_time_passed: float = 0
        self.time_to_respawn: float = 5
        self.initial_spawn_points = initial_spawn_points

    def update(self, delta_time: float):
        self.vehicle.update(delta_time)
        #
        # Respawn
        #
        if self.player_health <= 0:
            self.die(delta_time)

    def take_damage(self, damage: float):
        self.player_health -= damage
        if self.player_health < 0:
            self.player_health = 0

    def die(self, delta_time):
        self.alive = False
        self.respawn_time_passed = self.respawn_time_passed + delta_time
        if self.respawn_time_passed > self.time_to_respawn:
            self.respawn()

    def respawn(self):
        self.player_health = 100
        self.alive = True
        self.respawn_time_passed = 0
        chosen_spawn_point = self.initial_spawn_points[
            randrange(len(self.initial_spawn_points))
        ].transform
        self.vehicle.location = chosen_spawn_point
        self.vehicle.movement.reset_velocity()
