from __future__ import annotations

import math
import random
from typing import List

import arcade

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from driving.create_drive_modes import create_drive_modes
from iron_math import get_sprite_location, set_sprite_location
from linked_sprite import LinkedSprite
from player_input import PlayerInput
from sprite_lists import SpriteLists
from textures import RED_CAR
from weapon import LaserBeam, MachineGun, RocketLauncher, Weapon


class Player:
    def __init__(
        self, input: PlayerInput, sprite_lists: SpriteLists, initial_spawn_points: list
    ):
        self.sprite = LinkedSprite[Player](texture=RED_CAR, scale=0.2)
        self.sprite.owner = self
        self.sprite.center_x = 256
        self.sprite.center_y = 256
        self.input = input
        self.sprite_lists = sprite_lists
        self.primary_weapon_transform = (16, 10, 0)
        self.secondary_weapon_transform = (16, -10, 0)
        # Weapons
        self.weapons_list: List[Weapon] = [
            LaserBeam,
            RocketLauncher,
            MachineGun,
        ]
        self.weapon_index = 0
        self.primary_weapon: Weapon
        self.secondary_weapon: Weapon
        self.primary_weapon_sprite: arcade.Sprite
        self.secondary_weapon_sprite: arcade.Sprite
        self._swap_in_weapons()
        self.player_health = 100
        self.alive = True
        self.respawn_time_passed: float = 0
        self.time_to_respawn: float = 5
        self.initial_spawn_points = initial_spawn_points
        self.x_shift = float
        self.y_shift = float

        self.drive_mode_index = 0
        self.drive_modes = create_drive_modes(self)
        self.velocity = (0.0, 0.0)
        "Translational velocity -- (x,y) tuple -- measured in pixels per second"

    def update(self, delta_time: float):
        #
        # Driving and movement
        #
        if self.input.debug_3.pressed:
            self._swap_drive_mode()
        if self.alive:
            self.drive_modes[self.drive_mode_index].drive(delta_time)

        # Pac-man style screen wrapping
        position = self.sprite.position
        self.sprite.position = (position[0] % SCREEN_WIDTH, position[1] % SCREEN_HEIGHT)

        #
        # Weapons
        #
        if self.alive:
            self.primary_weapon.update(delta_time)
            self.secondary_weapon.update(delta_time)
            if self.input.swap_weapons_button.pressed:
                self._swap_weapons()

        #
        # Respawn
        #
        if self.player_health <= 0:
            self.die(delta_time)

    @property
    def drive_mode(self):
        return self.drive_modes[self.drive_mode_index]

    def _swap_drive_mode(self):
        self.drive_mode_index += 1
        if self.drive_mode_index >= len(self.drive_modes):
            self.drive_mode_index = 0

    def _swap_weapons(self):
        # Moves the current secondary weapon to the primary weapon slot and the next weapon on the list becomes the secondary weapon
        self._swap_out_weapons()
        self._swap_in_weapons()

    def _swap_out_weapons(self):
        self.primary_weapon.swap_out()
        self.secondary_weapon.swap_out()

    def _swap_in_weapons(self):
        self.primary_weapon = self.weapons_list[self.weapon_index](
            self,
            self.input.primary_fire_button,
            self.primary_weapon_transform,
        )
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons_list):
            self.weapon_index = 0
        self.secondary_weapon = self.weapons_list[self.weapon_index](
            self,
            self.input.secondary_fire_button,
            self.secondary_weapon_transform,
        )

    def draw(self):
        self.primary_weapon.draw()
        self.secondary_weapon.draw()

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
            random.randrange(len(self.initial_spawn_points))
        ].transform
        set_sprite_location(self.sprite, chosen_spawn_point)

    @property
    def location(self):
        return get_sprite_location(self.sprite)

    @location.setter
    def location(self, location: tuple[float, float, float]):
        return set_sprite_location(self.sprite, location)
