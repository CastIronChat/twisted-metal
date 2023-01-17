from __future__ import annotations

import math

import arcade

import constants
from driving.drive_mode import DriveMode

DEFAULT_WORLD_SIZE_X = constants.SCREEN_WIDTH
DEFAULT_WORLD_SIZE_Y = constants.SCREEN_HEIGHT
DEFAULT_ACCELERATION_RATE = 2
DEFAULT_DECELERATION_RATE = 0.2
DEFAULT_BRAKE_RATE = 25
DEFAULT_FRICTION = 25
DEFAULT_DRIVE_SPEED = 100
DEFAULT_TURN_SPEED = 0.8

DEFAULT_CONTROL_LOCKOUT = 0.4

IMPACT_FORCE_FLOOR = 1.5

AXIS_FLOOR = 0.3


class BasicCar(DriveMode):
    def __init__(self, controls: MovementControls):
        self.name = "Cable"
        self.move_controls = controls
        self.current_acceleration = 0

        self.vehicle_velocity = (0, 0, 0)
        self.external_velocity = (0, 0, 0)

        self.friction = DEFAULT_FRICTION
        self.acceleration_rate = DEFAULT_ACCELERATION_RATE
        self.decel_rate = DEFAULT_ACCELERATION_RATE
        self.brake_rate = DEFAULT_BRAKE_RATE
        self.current_brake = DEFAULT_BRAKE_RATE

        self.drive_speed = DEFAULT_DRIVE_SPEED
        self.turn_speed = DEFAULT_TURN_SPEED
        self.debug_world_boundary_x = DEFAULT_WORLD_SIZE_X
        self.debug_world_boundary_y = DEFAULT_WORLD_SIZE_Y
        self.impact_buffer = 0

        self.in_collision = False

    def set_stats(self, drive, turn, acc, brake):
        self.acceleration_rate = acc
        self.brake_rate = brake

        self.drive_speed = drive
        self.turn_speed = turn

    def drive_input(self, delta_time: float, vehicle: Vehicle, input: PlayerInput):

        x = 0
        y = 0
        turn = 0
        acc_change = 0

        if self.in_collision is False:

            if (
                abs(input.accelerate_axis.value) > AXIS_FLOOR
                or abs(input.brake_axis.value) > AXIS_FLOOR
            ):
                acc_change -= self.brake_rate * input.brake_axis.value
                acc_change += self.acceleration_rate * input.accelerate_axis.value
            else:
                # if the throttle is not being pressed the vehicle should not add force
                # and the acceleration should decay towards zero to allow feathering the throttle

                acc_total = abs(self.current_acceleration)

                if acc_total < self.decel_rate * delta_time:
                    self.current_acceleration = 0
                else:
                    acc_change = (
                        -math.copysign(1, self.current_acceleration) * self.decel_rate
                    )

            if input.reload_button.value is True:
                self.current_brake = 1
            else:
                self.current_brake = 0

            # the current acceleration is used to have speed progress from zero to its maximum
            self.current_acceleration = self.clamp(
                self.current_acceleration + (acc_change * delta_time), -1, 1
            )

            turn = (
                input.x_axis.value
                * self.turn_speed
                * -math.copysign(1, self.current_acceleration)
                # * abs(self.current_acceleration)
            )

        # consioder the new angle after turning for the intended vehicle velocity
        car_angle = vehicle.location[2] + (turn * delta_time)

        if acc_change != 0:
            # find the X and Y movement based on the angle of the sprite
            x = self.drive_speed * math.cos(car_angle) * self.current_acceleration
            y = self.drive_speed * math.sin(car_angle) * self.current_acceleration
        # else:
        #     # a stationary car cant turn
        #     turn = 0

        self.vehicle_velocity = (x, y, turn)
        return (x, y, turn)

    def move(self, delta_time: float, vehicle: Vehicle, walls: arcade.SpriteList):

        # If there are external forces moving the car, apply friction
        self.apply_reductive_force(self.friction, delta_time)
        self.apply_reductive_force(self.brake_rate * self.current_brake, delta_time)

        # get the intended velocity for this frame from the player input
        # and external forces that have been applied to this car
        real_velocity = self.get_real_velocity(delta_time)

        # check if the car can move to its new position
        is_valid_position = self.move_controls.check_for_valid_movement(
            vehicle, real_velocity, walls
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
                vehicle, smaller_velocity, walls
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

        x = 0
        y = 0
        angle = 0

        x += self.external_velocity[0] * delta_time
        y += self.external_velocity[1] * delta_time
        angle += self.external_velocity[2] * delta_time

        if self.in_collision is False:
            x += self.vehicle_velocity[0] * delta_time
            y += self.vehicle_velocity[1] * delta_time

            magnitude = abs(x) + abs(y)
            # a stationary car cant turn
            if magnitude != 0:
                bonus_turn_from_speed = 1 + (magnitude / self.drive_speed)
                angle += self.vehicle_velocity[2] * bonus_turn_from_speed * delta_time

        return (x, y, angle)

    def apply_external_force(self, vector: (float, float, float)):
        x = vector[0] + self.external_velocity[0]
        y = vector[1] + self.external_velocity[1]
        angle = vector[2] + self.external_velocity[2]
        self.external_velocity = (x, y, angle)

    def collide_at_point(self, point, velocity, delta_time):
        #
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
            self.current_acceleration = 0

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)
