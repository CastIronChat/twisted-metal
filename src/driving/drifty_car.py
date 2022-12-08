from __future__ import annotations

from typing import TYPE_CHECKING

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from curve import Curve
from driving.drive_mode import DriveMode
from iron_math import (
    add_vec,
    clamp,
    project_vec,
    rescale_value_between,
    rotate_vec,
    scale_vec,
    vec_dot_product,
    vec_magnitude,
)

if TYPE_CHECKING:
    from player import Player


def drifty_car(player: Player):
    return DriftyCar(player)


def mike_drifty_car(player: Player):
    drive_mode = DriftyCar(player)
    drive_mode.forward_acceleration = Curve([(0.1, 500), (0.8, 3000)])
    # drive_mode.acceleration_curve = Curve([(0, 1500)])
    # drive_mode.acceleration_curve = Curve([(0.1, 3000), (0.9, 1000)])


class DriftyCar(DriveMode):
    """
    Driving mode with peppy acceleration, braking, turning, and a drifting
    mechanic triggered by holding gas and brake at the same time.
    """

    def setup(self):
        self.velocity = (0.0, 0.0)
        # TODO
        self._sprite = self.player.sprite

        # Single point on the curve means it's a flat line: all Y values
        # are the same
        self.forward_acceleration = Curve([(0.0, 1500)])
        """
        Effectively, torque of the engine driving forward.
        Since there is no brake, this is also braking power when driving in reverse and attempting to slow down.
        """
        self.reverse_acceleration = Curve([(0.0, 1500)])
        self.reverse_power = 1500
        """
        Opposite of forward_acceleration
        """
        self.max_engine_speed = 500
        """
        Engine is only strong enough to push car up to this speed.  It may be pushed higher by external forces,
        but engine RPMs max out at this speed.
        """
        self.base_turning_radius = 90
        """
        Steering speed is calculated from a turning radius which is roughly described as:
            base_turning_radius + speed * turning_radius_to_velocity_ratio
        This allows turning radius to increase as the car speeds up.
        We use absolute speed in *any* direction so that the car continues to spin at an intuitive rate
        even as you e.g. do a 720, drifting past enemies, shooting in all directions.  This is fun but
        not realistic.
        """
        self.turning_radius_to_velocity_ratio = 0.1
        "see `base_turning_radius`"
        self.kinetic_friction = -10
        """
        Kinetic friction for wheels to resist lateral sliding.
        Note: the math here is wonky, does not follow real-world physics rules.
        """
        self.static_friction = -100
        "Static friction for wheels to resist lateral sliding."
        self.lateral_velocity_kinetic_friction_threshold = 40
        """
        When lateral velocity exceeds this value, we switch from static to kinetic friction.
        The goal is for drifting to start after you attempt to turn too aggressively.
        TODO needs work.
        """

    def update(self, delta_time: float):
        prev_velocity = self.velocity

        # Holding both gas and reverse means you're in "drift mode"
        drifting = (
            self.input.accelerate_axis.value > 0 and self.input.brake_axis.value > 0
        )

        # Break down the car's current heading and velocity in a variety of ways
        # We use these values later
        heading = rotate_vec((1, 0), self._sprite.radians)
        "Unit vector pointing in front of the car's hood, independent of velocity"
        absolute_speed = vec_magnitude(prev_velocity)
        forward_velocity = project_vec(prev_velocity, heading)
        forward_speed = vec_dot_product(forward_velocity, heading)
        "Can be negative if moving backwards; this is important"
        lateral_velocity = add_vec(prev_velocity, scale_vec(forward_velocity, -1))
        absolute_lateral_speed = vec_magnitude(lateral_velocity)

        forward_speed_percentage_of_max = (
            clamp(forward_speed, -self.max_engine_speed, self.max_engine_speed)
            / self.max_engine_speed
        )
        """
        Car's speed along the heading axis.  Negative means it is drifting
        backwards. Excludes any lateral movement of the car.
        """

        # Compute how much the wheels are pushing the car forward due to throttle
        if forward_speed > self.max_engine_speed:
            forward_acceleration = (0, 0)
        else:
            # Maximum acceleration power, iff the player is fully holding the accelerate axis
            max_forward_acceleration = self.forward_acceleration.sample(
                forward_speed_percentage_of_max
            )
            forward_acceleration = scale_vec(
                heading,
                self.input.accelerate_axis.value * max_forward_acceleration,
            )

        # Compute how much the wheels are pushing the car backward due to throttle
        if forward_speed < -self.max_engine_speed:
            reverse_acceleration = (0, 0)
        else:
            max_reverse_acceleration = self.reverse_acceleration.sample(
                -forward_speed_percentage_of_max
            )
            reverse_acceleration = scale_vec(
                heading,
                -self.input.brake_axis.value * max_reverse_acceleration,
            )

        # Compute friction of the wheels resisting the car sliding laterally
        if drifting:
            chosen_friction = 0
        elif absolute_lateral_speed > self.lateral_velocity_kinetic_friction_threshold:
            chosen_friction = self.kinetic_friction
        else:
            chosen_friction = self.static_friction
        lateral_friction_acceleration = scale_vec(lateral_velocity, chosen_friction)

        # Sum up net accelerations
        acceleration = add_vec(forward_acceleration, reverse_acceleration)
        acceleration = add_vec(acceleration, lateral_friction_acceleration)

        # apply delta-time-d acceleration to velocity
        new_velocity = add_vec(self.velocity, scale_vec(acceleration, delta_time))
        self.velocity = new_velocity

        # apply delta-time-d velocity to position
        new_position = add_vec(
            self._sprite.position, scale_vec(new_velocity, delta_time)
        )

        # Pac-man style screen wrapping
        new_position = (new_position[0] % SCREEN_WIDTH, new_position[1] % SCREEN_HEIGHT)

        self._sprite.position = new_position

        # Compute maximum rate of angular acceleration, if player is holding
        # control stick fully to one side.
        # This math starts by choosing a turning radius which depends on the car's absolute speed.
        # Then it derives angular speed from there.
        max_angular_speed = absolute_speed / (
            self.base_turning_radius
            + absolute_speed * self.turning_radius_to_velocity_ratio
        )

        # Apply rotation
        sign = -1
        if forward_speed < 0 and not drifting:
            sign = 1
        self._sprite.radians += (
            max_angular_speed * sign * delta_time * self.input.x_axis.value
        )
