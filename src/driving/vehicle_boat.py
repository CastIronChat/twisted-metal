from __future__ import annotations

import math

import arcade

import constants
from driving.drive_mode import DriveMode

DEFAULT_WORLD_SIZE_X = constants.SCREEN_WIDTH
DEFAULT_WORLD_SIZE_Y = constants.SCREEN_HEIGHT
DEFAULT_ACCELERATION_RATE = 2.5
DEFAULT_DECELERATION_RATE = 0.1
DEFAULT_BRAKE_RATE = 25
DEFAULT_FRICTION = 25
DEFAULT_DRIVE_SPEED = 12
DEFAULT_TURN_SPEED = 2.2

DEFAULT_CONTROL_LOCKOUT = 0.4

IMPACT_FORCE_FLOOR = 1.5

AXIS_FLOOR = 0.3


class Boat(DriveMode):
    def __init__(self, controls: MovementControls):
        self.name = "Boat"
        self.move_controls = controls

        self.vehicle_velocity = (0, 0, 0)
        self.external_velocity = (0, 0, 0)

        self.friction = DEFAULT_FRICTION

        self.drive_speed = DEFAULT_DRIVE_SPEED
        self.turn_speed = DEFAULT_TURN_SPEED
        self.debug_world_boundary_x = DEFAULT_WORLD_SIZE_X
        self.debug_world_boundary_y = DEFAULT_WORLD_SIZE_Y
        self.impact_buffer = 0

        self.in_collision = False

        self.sail_height = 0  # 0:furled 1:unfurled
        self.raise_sail_speed = DEFAULT_DECELERATION_RATE
        self.wheel_position = 0  #:-1 full left 1:full right
        self.turn_wheel_speed = DEFAULT_DECELERATION_RATE  #:-1 full left 1:full right
        self.raise_anchor_speed = 0.5
        self.drop_anchor_speed = 2
        self.anchor_position = 0  #  0:up 1:down

        self.wind_assist = 1

    def set_stats(self, drive, turn, acc, brake):
        self.acceleration_rate = acc
        self.brake_rate = brake

        self.drive_speed = drive
        self.turn_speed = turn

    def drive_input(self, delta_time: float, vehicle: Vehicle, input: PlayerInput):

        x = 0
        y = 0
        turn = 0
        sail_change = 0
        wheel_change = -input.x_axis.value * self.turn_wheel_speed
        anchor_change = 0

        if input.accelerate_axis.value > 0.1:
            sail_change = input.accelerate_axis.value * DEFAULT_ACCELERATION_RATE

        if input.brake_axis.value > 0.1:
            sail_change = input.brake_axis.value * -self.raise_sail_speed

        if input.ry_axis.value > 0.1:
            anchor_change = input.ry_axis.value * -self.raise_anchor_speed * delta_time
        else:
            # if the anchor isnt raised all the way it should fall back to the 'down' position
            if input.ry_axis.value < -0.1 or self.anchor_position > 0:
                anchor_change = delta_time * self.drop_anchor_speed

        self.anchor_position = self.clamp(self.anchor_position + anchor_change, 0, 1)

        self.wheel_position = self.clamp(
            self.wheel_position + (wheel_change * delta_time), -1, 1
        )
        self.sail_height = self.clamp(
            self.sail_height + (sail_change * delta_time), 0, 1
        )

        vehicle_angle = vehicle.location[2]  # + (turn * delta_time)
        self.set_wind_assist(math.degrees(vehicle.location[2]) % 360)

        x = self.drive_speed * math.cos(vehicle_angle) * self.sail_height
        y = self.drive_speed * math.sin(vehicle_angle) * self.sail_height

        turn = self.wheel_position * (self.turn_speed * (1.5 - self.sail_height))

        # input buffer for locking the wheel straight
        if abs(self.wheel_position) < 0.1:
            turn = 0

        self.vehicle_velocity = (x, y, turn)

    def move(
        self,
        delta_time: float,
        vehicle: Vehicle,
        walls: arcade.SpriteList,
        vehicles: arcade.SpriteList,
    ):

        # If there are external forces moving the car, apply friction
        self.apply_reductive_force(self.friction, delta_time)
        force_this_step = (
            self.vehicle_velocity[0] * delta_time,
            self.vehicle_velocity[1] * delta_time,
            0,
        )

        # self.apply_external_force(force_this_step)
        # get the intended velocity for this frame from the player input
        # and external forces that have been applied to this car
        real_velocity = self.get_real_velocity(delta_time)

        # check if the car can move to its new position
        is_valid_position = self.move_controls.check_for_valid_movement(
            vehicle, real_velocity, walls, vehicles
        )

        if is_valid_position is False:
            # the vehicle is colliding, this checks to move the vehicle so that the collision visually appears
            # as close to the wall as possible
            smaller_velocity = (
                real_velocity[0] * 0.3,
                real_velocity[1] * 0.3,
                real_velocity[2] * 0.3,
            )

            # check if the car can move to its new position
            is_valid_position = self.move_controls.check_for_valid_movement(
                vehicle, smaller_velocity, walls, vehicles
            )

            if is_valid_position is True:
                collision_point = self.move_controls.add_vector3(
                    smaller_velocity, vehicle.location
                )

                vehicle.location = self.move_controls.add_vector3(
                    smaller_velocity, vehicle.location
                )
            else:
                collision_point = self.move_controls.add_vector3(
                    real_velocity, vehicle.location
                )

            self.collide_at_point(collision_point, real_velocity, delta_time)
            # set the in collision boolean to apply the collision force once
            # TODO: vector normal reflection for collisions
            # currently the collision just applies the opposite force

        else:
            # no wall collisions means a valid spot to move to
            # collisions with other objects result in collision
            # but are not an invalid position
            vehicle.location = self.move_controls.add_vector3(
                real_velocity, vehicle.location
            )

        # reset the shadow sprite to the vehicle position
        self.move_controls.set_shadow_sprite_position(vehicle.location, (0, 0, 0))

        # the impact buffer is a timer that locks the vehicle force briefly after a collision
        if self.impact_buffer > 0:
            self.impact_buffer -= delta_time
            if self.impact_buffer < 0:
                # self.external_velocity = (0, 0, 0)
                self.impact_buffer = 0
                self.in_collision = False

        if self.debug_world_boundary_x != 0:
            vehicle.location = (
                vehicle.center_x % self.debug_world_boundary_x,
                vehicle.center_y % self.debug_world_boundary_y,
                vehicle.radians,
            )

    def set_wind_assist(self, vehicle_angle):
        if vehicle_angle >= 0 and vehicle_angle <= 180:
            self.wind_assist = 1 + (91 - abs(90 - vehicle_angle)) / 25

        else:
            self.wind_assist = 1 + (91 - abs(270 - vehicle_angle)) / 45

    def apply_reductive_force(self, force: float, delta_time: float):
        # frictional forces or brake forces should reduce any acting velocity
        #  to zero but not into negative the way reverse acceleration would
        reductive_force = force * delta_time
        x = self.clamp(abs(self.external_velocity[0]) - reductive_force, 0, 999)
        y = self.clamp(abs(self.external_velocity[1]) - reductive_force, 0, 999)
        angle = self.clamp(abs(self.external_velocity[2]) - reductive_force, 0, 999)

        x *= math.copysign(1, self.external_velocity[0])
        y *= math.copysign(1, self.external_velocity[1])
        angle *= math.copysign(1, self.external_velocity[2])

        self.external_velocity = (x, y, angle)

    def get_real_velocity(self, delta_time):

        # get the force from external sources for this frame
        x = self.external_velocity[0] * delta_time
        y = self.external_velocity[1] * delta_time
        angle = self.external_velocity[2] * delta_time
        # then if not in the lockout window from a collision
        # get the intended force from the vehicle
        if self.in_collision is False:
            x += self.vehicle_velocity[0] * delta_time
            y += self.vehicle_velocity[1] * delta_time
            # the boat can turn while stationary
            angle += self.vehicle_velocity[2] * delta_time

        # if the boat is facing with the 'fake' wind direction get bonus speed
        x *= self.wind_assist
        y *= self.wind_assist

        # if self.vehicle_velocity[0] != 0:
        #     print(self.wind_assist)
        # if the anchor is down the boat cant move but CAN turn
        if self.anchor_position > 0.9:
            return (0, 0, angle)

        return (x, y, angle)

    def apply_external_force(self, vector: (float, float, float)):
        x = vector[0] + self.external_velocity[0]
        y = vector[1] + self.external_velocity[1]
        angle = vector[2] + self.external_velocity[2]
        self.external_velocity = (x, y, angle)

    def collide_at_point(self, point, velocity, delta_time):

        if self.in_collision is False and self.impact_buffer == 0:
            self.in_collision = True
            self.impact_buffer = DEFAULT_CONTROL_LOCKOUT

            collision_vector = (
                -velocity[0] * 0.9 / delta_time,
                -velocity[1] * 0.9 / delta_time,
                -velocity[2] * 0.9 / delta_time,
            )

            # collisions should over ride any external forces on the car
            # since those forces are included in the calculation of the collision vector
            self.external_velocity = collision_vector
            self.current_acceleration = (0, 0)

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def lerp(
        self, velocity: (float, float, float), vector: (float, float, float), delta_time
    ):
        # frictional forces or brake forces should reduce any acting velocity
        #  to zero but not into negative the way reverse acceleration would
        x = self.clamp((velocity[0]) - (vector[0]), 0, 999)
        y = self.clamp((velocity[1]) - (vector[1]), 0, 999)
        angle = self.clamp((velocity[2]) - (vector[2]), 0, 999)

        x *= delta_time * DEFAULT_ACCELERATION_RATE
        y *= delta_time * DEFAULT_ACCELERATION_RATE
        angle *= delta_time * DEFAULT_ACCELERATION_RATE

        return (velocity[0] + x, velocity[1] + y, velocity[2] + angle)
