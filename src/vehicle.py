from __future__ import annotations

from typing import TYPE_CHECKING, List

import arcade

from constants import HIT_INDICATOR_DURATION
from driving.create_drive_modes import create_drive_modes
from iron_math import (
    get_sprite_location,
    move_sprite_relative_to_parent,
    set_sprite_location,
)
from linked_sprite import LinkedSprite
from movement_controls import MovementControls
from sprite_lists import SpriteLists
from textures import FIRE, VEHICLES
from weapons.laser_beam import LaserBeam
from weapons.machine_gun import MachineGun
from weapons.rocket_launcher import RocketLauncher
from weapons.weapon import Weapon

if TYPE_CHECKING:
    from player import Player

import math


class Vehicle:
    def __init__(self, player: Player, sprite_lists: SpriteLists, player_index: int):
        self.player = player
        self.sprite = LinkedSprite[Vehicle](texture=VEHICLES[player_index], scale=0.2)
        self.sprite.owner = self
        self.sprite_lists = sprite_lists
        self.health: float = 100
        self.sprite_lists.vehicles.append(self.sprite)
        self.primary_weapon_transform = (16, 10, 0)
        self.secondary_weapon_transform = (16, -10, 0)
        # Weapons
        self.weapons_list: List[Weapon] = [
            LaserBeam,
            RocketLauncher,
            MachineGun,
        ]
        self.weapon_index: int = 0
        self.primary_weapon: Weapon
        self.secondary_weapon: Weapon
        self.primary_weapon_sprite: arcade.Sprite
        self.secondary_weapon_sprite: arcade.Sprite
        self._swap_in_weapons()
        self.hit_indicator: bool = False
        self.time_since_hit: float = 0
        self.fire_sprite = arcade.Sprite(texture=FIRE, scale=3)
        self.drive_mode_index = 0
        self.drive_modes = create_drive_modes(self)

        self.movement = MovementControls(
            LinkedSprite[Vehicle](texture=VEHICLES[1], scale=0.18)
        )

    def update(self, delta_time: float):

        # Driving and movement
        if self.player.alive:
            self.movement.drive_input(delta_time, self, self.player.input)
        self.movement.move(delta_time, self, self.sprite_lists.walls)

        # Weapons
        if self.player.alive:
            self.movement.drive_input(delta_time, self, self.player.input)
            self.primary_weapon.update(delta_time)
            self.secondary_weapon.update(delta_time)
            if self.player.input.swap_weapons_button.pressed:
                self._swap_weapons()

        if self.hit_indicator:
            self.time_since_hit += delta_time
            if self.time_since_hit > HIT_INDICATOR_DURATION:
                self.sprite.alpha = 255
                self.hit_indicator = False
                self.time_since_hit = 0

    def apply_damage(self, damage: float):
        if self.player.alive:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.die()
            self.hit_indicator = True
            self.time_since_hit = 0
            self.sprite.alpha = 150

    def die(self):
        self.player.alive = False
        self.sprite_lists.vehicle_attachments.append(self.fire_sprite)
        self.primary_weapon.deactivate()
        self.secondary_weapon.deactivate()

    def respawn(self, location):
        self.health = 100
        self.sprite_lists.vehicle_attachments.remove(self.fire_sprite)
        self.location = location
        self.movement.reset_velocity()

    def _swap_weapons(self):
        # Moves the current secondary weapon to the primary weapon slot and the next weapon on the list becomes the secondary weapon
        self._swap_out_weapons()
        self._swap_in_weapons()

    def _swap_out_weapons(self):
        self.primary_weapon.swap_out()
        self.secondary_weapon.swap_out()

    def _swap_in_weapons(self):
        self.primary_weapon = self.weapons_list[self.weapon_index](
            self.sprite_lists,
            self.player.input.primary_fire_button,
            self.primary_weapon_transform,
        )
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons_list):
            self.weapon_index = 0
        self.secondary_weapon = self.weapons_list[self.weapon_index](
            self.sprite_lists,
            self.player.input.secondary_fire_button,
            self.secondary_weapon_transform,
        )

    def _update_vehicle_attachment_locations(self):
        move_sprite_relative_to_parent(
            self.primary_weapon.weapon_sprite,
            self.sprite,
            self.primary_weapon_transform,
        )
        move_sprite_relative_to_parent(
            self.secondary_weapon.weapon_sprite,
            self.sprite,
            self.secondary_weapon_transform,
        )
        move_sprite_relative_to_parent(
            self.fire_sprite, self.sprite, (0, 0, -self.radians)
        )
        self.fire_sprite.center_y += 15

    @property
    def location(self):
        return get_sprite_location(self.sprite)

    @location.setter
    def location(self, location: tuple[float, float, float]):
        set_sprite_location(self.sprite, location)
        self._update_vehicle_attachment_locations()

    # these properties are for the convenience of calling vehicle.center_x rather than vehicle.location[0]
    @property
    def center_x(self):
        return self.sprite.center_x

    @center_x.setter
    def center_x(self, center_x: float):
        self.sprite.center_x = center_x
        self._update_vehicle_attachment_locations()

    @property
    def center_y(self):
        return self.sprite.center_y

    @center_y.setter
    def center_y(self, center_y: float):
        self.sprite.center_y = center_y
        self._update_vehicle_attachment_locations()

    @property
    def angle(self):
        return self.sprite.angle

    @angle.setter
    def angle(self, angle: float):
        self.sprite.angle = angle
        self._update_vehicle_attachment_locations()

    @property
    def radians(self):
        return self.sprite.radians

    @radians.setter
    def radians(self, radians: float):
        self.sprite.radians = radians
        self._update_vehicle_attachment_locations()

    @property
    def drive_mode(self):
        return self.drive_modes[self.drive_mode_index]

    def _swap_drive_mode(self):
        self.drive_mode_index += 1
        if self.drive_mode_index >= len(self.drive_modes):
            self.drive_mode_index = 0
