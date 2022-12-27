from __future__ import annotations

import math
from typing import TYPE_CHECKING

import arcade

import constants
from player_input import PlayerInput

# This allows a circular import only for the purposes of type hints
if TYPE_CHECKING:
    from vehicle import Vehicle

# This is setup for the Player to call "drive_input" where the vehicle updates it's
# intended velocity and rotation based on the player input
# then the player calls "movement" to act on the change from "drive_input"
# this way the inputs are always registered but the movement can be skipped
# if a collision or game state makes it where the vehicle shouldnt act
# This will help avoid race conditions on collisions
#
#
# for checking if a vehicle should take damage from an impact. as a percentage of their top acceleration

DEFAULT_WORLD_SIZE = constants.SCREEN_WIDTH
DEFAULT_ACCELERATION_RATE = 2.5
DEFAULT_BRAKE_RATE = 0.8
DEFAULT_FRICTION = 0.1
DEFAULT_DRIVE_SPEED = 150
DEFAULT_TURN_SPEED = 75

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

    # These are the values the vehicle updates in "drive_input"
    current_velocity_x: float
    current_velocity_y: float
    current_velocity_turn: float
    current_acceleration: float

    def __init__(self, sprite: arcade.Sprite):
        self.shadow_sprite = sprite
        self.shadow_sprite.center_x = sprite.center_x
        self.shadow_sprite.center_y = sprite.center_y
        self.shadow_sprite.angle = sprite.angle
        self.debug_world_boundary = DEFAULT_WORLD_SIZE
        self.current_velocity_x = 0
        self.current_velocity_y = 0
        self.current_velocity_turn = 0
        self.current_acceleration = 0
        self.external_velocity_turn = 0

        self.acceleration_rate = DEFAULT_ACCELERATION_RATE
        self.brake_rate = DEFAULT_BRAKE_RATE
        self.friction = DEFAULT_FRICTION
        self.drive_speed = DEFAULT_DRIVE_SPEED
        self.turn_speed = DEFAULT_TURN_SPEED
        self.impact_buffer = 0

    #   Drive input is called by the player and passed that player's input
    #   to set what the vehicle's velocity and rotation should be
    #   Does not change the vehicles position
    def drive_input(self, delta_time: float, vehicle: Vehicle, input: PlayerInput):

        if self.impact_buffer > 0:
            self.impact_buffer -= 1
            if self.impact_buffer <= 0:
                self.external_velocity_turn = 0

        # updates the vehicles intended  velocity and rotation based on type
        acceleration_change = 0
        self.shadow_sprite.center_x = vehicle.center_x
        self.shadow_sprite.center_y = vehicle.center_y

        if input.accelerate_axis.value:
            if self.current_acceleration < 0:
                acceleration_change += self.brake_rate
            acceleration_change += self.acceleration_rate
        elif input.brake_axis.value:
            acceleration_change -= self.brake_rate
        else:
            if abs(self.current_acceleration) != 0:
                if abs(self.current_acceleration) <= delta_time * self.friction:
                    self.current_acceleration = 0
                else:
                    acceleration_change -= (
                        math.copysign(1, self.current_acceleration) * self.friction
                    )
        # the current acceleration is used to have speed progress from zero to its maximum
        self.current_acceleration = self.clamp(
            self.current_acceleration + (acceleration_change * delta_time), -1, 1
        )

        car_angle = math.radians(vehicle.angle)

        # find the X and Y movement based on the angle of the sprite
        self.current_velocity_x = (
            self.drive_speed
            * math.cos(car_angle)
            * self.current_acceleration
            * delta_time
        )
        self.current_velocity_y = (
            self.drive_speed
            * math.sin(car_angle)
            * self.current_acceleration
            * delta_time
        )

        # a stationary car cant turn
        self.current_velocity_turn = (
            input.x_axis.value
            * self.turn_speed
            * delta_time
            * -self.current_acceleration
        )

    def reset_velocity(self):
        self.current_acceleration = 0
        self.current_velocity_x = 0
        self.current_velocity_y = 0
        self.current_velocity_turn = 0

    # called from the player to tell the vehicle to act on it's intended velocity and rotation
    def move(self, delta_time: float, vehicle: Vehicle, walls: arcade.SpriteList):
        # the shadow sprite is used to simply math and planning to deal with the arena not being an array
        self.shadow_sprite.center_x = vehicle.center_x + self.current_velocity_x
        self.shadow_sprite.center_y = vehicle.center_y + self.current_velocity_y
        self.shadow_sprite.angle = (
            self.current_velocity_turn + vehicle.angle + self.external_velocity_turn
        )
        walls_touching_player = arcade.check_for_collision_with_list(
            self.shadow_sprite, walls
        )
        if len(walls_touching_player) > 0:
            # high speed impact should damage the car, and greatly cut the velocity
            if self.current_acceleration > IMPACT_FORCE_FLOOR:
                self.current_velocity_x -= self.current_velocity_x * 0.5
                self.current_velocity_y -= self.current_velocity_y * 0.5
            else:
                self.current_acceleration -= (
                    self.current_acceleration * self.acceleration_rate * delta_time
                )
                self.current_velocity_x = 0
                self.current_velocity_y = 0
                if abs(self.current_acceleration) < 0.1:
                    self.current_acceleration = 0
                    self.current_velocity_x = 0
                    self.current_velocity_y = 0

            self.shadow_sprite.center_x = vehicle.center_x
            self.shadow_sprite.center_y = vehicle.center_y
        else:
            # no wall collisions means a valid spot to move to
            vehicle.location = (
                self.shadow_sprite.center_x,
                self.shadow_sprite.center_y,
                self.shadow_sprite.radians,
            )

        # NOTE: place holder boundaries to wrap aroung like pacman
        if self.debug_world_boundary != 0:
            vehicle.location = (
                vehicle.center_x % self.debug_world_boundary,
                vehicle.center_y % self.debug_world_boundary,
                self.shadow_sprite.radians,
            )

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)
