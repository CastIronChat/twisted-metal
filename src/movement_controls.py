from __future__ import annotations

import math
from enum import Enum
from typing import TYPE_CHECKING

import arcade

import constants
from driving.create_drive_modes import create_drive_modes
from player_input import PlayerInput

# This allows a circular import only for the purposes of type hints
if TYPE_CHECKING:
    from vehicle import Vehicle


class cars:
    Car = 0
    Ghost = 1
    Tank = 2
    Walker = 3


# This is setup for the Player to call "drive_input" where the vehicle updates it's
# intended velocity and rotation based on the player input
# then the player calls "movement" to act on the change from "drive_input"
# this way the inputs are always registered but the movement can be skipped
# if a collision or game state makes it where the vehicle shouldnt act
# This will help avoid race conditions on collisions
#
#
# for checking if a vehicle should take damage from an impact. as a percentage of their top acceleration

DEFAULT_WORLD_SIZE_X = constants.SCREEN_WIDTH
DEFAULT_WORLD_SIZE_Y = constants.SCREEN_HEIGHT
DEFAULT_ACCELERATION_RATE = 1.5
DEFAULT_BRAKE_RATE = 10.8
DEFAULT_FRICTION = 0.91
DEFAULT_DRIVE_SPEED = 10.1
DEFAULT_TURN_SPEED = 1.1

IMPACT_FORCE_FLOOR = 1.5


class MovementControls:
    # The stat for max (x,y) linear speed
    drive_speed: float
    # The stat for max rotational speed
    turn_speed: float

    # how fast the current acceleration goes from 0 -> 1
    acceleration_rate: float
    # how fast the brake applies to current acceleration
    brake_rate: float
    # how fast the vehicle's current acceleration slows while not accelerating
    friction: float

    # velocity is x,y,angular
    # the velocity applied when updationg the position
    # is a combination of the vehicle velocity and external forces
    real_velocity: (float, float, float)
    # external is the combination of forces applied on the vehicle
    external_velocity: (float, float, float)
    # These are the values the vehicle updates in "drive_input"
    # representing the intended movement of the player's input
    vehicle_velocity: (float, float, float)

    current_acceleration: float

    drive_modes: [drive_mode]

    def __init__(self, sprite: arcade.Sprite):
        self.shadow_sprite = sprite

        self.debug_world_boundary_x = DEFAULT_WORLD_SIZE_X
        self.debug_world_boundary_y = DEFAULT_WORLD_SIZE_Y

        self.drive_modes = create_drive_modes(self)

        self.change_car(1)
        print(self.car_type.name)

    def change_car(self, index: int):
        if len(self.drive_modes) > 0:
            clamped_index = index % (len(self.drive_modes))

            if self.drive_modes[clamped_index] is not None:
                self.car_type = self.drive_modes[clamped_index]

    #   Drive input is called by the player and passed that player's input
    #   to set what the vehicle's velocity and rotation should be
    #   Does not change the vehicles position
    def drive_input(self, delta_time: float, vehicle: Vehicle, input: PlayerInput):

        # for changing drive modes
        if input.accelerate_axis.value > 0:
            if input.reload_button.value is True:
                if input.primary_fire_button.value is True:
                    self.change_car(cars.Car)
                    return
                if input.secondary_fire_button.value is True:
                    self.change_car(cars.Ghost)
                    return

        if self.car_type is not None:
            self.car_type.drive_input(delta_time, vehicle, input)

    # called from the player to tell the vehicle to act on it's intended velocity and rotation
    def move(self, delta_time: float, vehicle: Vehicle, walls: arcade.SpriteList):
        if self.car_type is not None:
            self.car_type.move(delta_time, vehicle, walls)

    def check_for_valid_movement(self, vehicle: Vehicle, velocity, walls):
        # the shadow sprite is used to simplify math and planning to deal with the arena not being an array

        self.set_shadow_sprite_position(vehicle.location, velocity)

        if len(arcade.check_for_collision_with_list(self.shadow_sprite, walls)) > 0:

            return False
        return True

    def set_shadow_sprite_position(self, location, vector):

        self.shadow_sprite.center_x = location[0] + vector[0]
        self.shadow_sprite.center_y = location[1] + vector[1]
        self.shadow_sprite.angle = location[2] + vector[2]

    def apply_external_force(self, vector: (float, float)):

        if self.car_type is not None:
            self.car_type.apply_external_force((vector[0], vector[1], 0))

    def apply_external_force(self, vector: (float, float, float)):
        if self.car_type is not None:
            self.car_type.apply_external_force(vector)

    def add_vector3(self, vec_a, vec_b):
        x = vec_a[0] + vec_b[0]
        y = vec_a[1] + vec_b[1]
        angle = vec_a[2] + vec_b[2]
        return (x, y, angle)

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)
