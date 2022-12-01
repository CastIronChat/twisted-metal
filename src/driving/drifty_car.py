from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from driving.drive_mode import DriveMode
from iron_math import (
    rotate_vec,
    vec_magnitude,
    project_vec,
    add_vec,
    scale_vec,
    vec_dot_product,
)


class DriftyCar(DriveMode):
    """
    Driving mode with peppy acceleration, braking, turning, and a drifting
    mechanic triggered by holding gas and brake at the same time.
    """

    def setup(self):
        self.velocity = (0.0, 0.0)
        # TODO
        self._sprite = self.player.sprite

        self.accelerate_power = 1500
        """
        Effectively, torque of the engine driving forward.
        Since there is no brake, this is also braking power when driving in reverse and attempting to slow down.
        """
        self.reverse_power = 1500
        """
        Opposite of accelerate_power
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
        heading = rotate_vec((1, 0), self._sprite.radians)
        velocity_magnitude = vec_magnitude(prev_velocity)
        velocity_forward = project_vec(prev_velocity, heading)
        velocity_lateral = add_vec(prev_velocity, scale_vec(velocity_forward, -1))
        forward_acceleration = scale_vec(
            heading,
            self.input.accelerate_axis.value * self.accelerate_power,
        )
        reverse_acceleration = scale_vec(
            heading, -self.input.brake_axis.value * self.reverse_power
        )
        velocity_along_heading = vec_dot_product(velocity_forward, heading)
        if velocity_along_heading > self.max_engine_speed:
            forward_acceleration = (0, 0)
        if velocity_along_heading < -self.max_engine_speed:
            reverse_acceleration = (0, 0)
        lateral_mag = vec_magnitude(velocity_lateral)
        chosen_friction = self.static_friction
        if lateral_mag > self.lateral_velocity_kinetic_friction_threshold:
            chosen_friction = self.kinetic_friction
        drifting = (
            self.input.accelerate_axis.value > 0 and self.input.brake_axis.value > 0
        )
        if drifting:
            chosen_friction = 0
        lateral_friction_acceleration = scale_vec(velocity_lateral, chosen_friction)

        # Idea: compute the amount of lateral acceleration introduced by this
        # frame's rotation.
        # This approximates centrifugal force.
        #
        # We use this to compute friction and apply an opposing acceleration.
        # (this is a centripetal force IRL, but we don't mention mass in this code)
        #
        # If opposing acceleration equals introduced lateral acceleration, then
        # they cancel out and car continues to drive straight ahead, but at its
        # new heading.
        #
        # If opposing acceleration cannot fully counteract existing or
        # introduced lateral acceleration, then the car starts drifting.
        #
        # Presence of lateral velocity will cause this logic to switch from
        # static to kinetic friction on future frames, which will cause a drift.

        accumulated_acceleration = add_vec(forward_acceleration, reverse_acceleration)
        accumulated_acceleration = add_vec(
            accumulated_acceleration, lateral_friction_acceleration
        )

        # apply delta-time-d acceleration to velocity
        new_velocity = add_vec(
            self.velocity, scale_vec(accumulated_acceleration, delta_time)
        )
        self.velocity = new_velocity

        # apply delta-time-d velocity to position
        new_position = add_vec(
            self._sprite.position, scale_vec(new_velocity, delta_time)
        )

        # Pac-man style wrapping
        new_position = (new_position[0] % SCREEN_WIDTH, new_position[1] % SCREEN_HEIGHT)

        self._sprite.position = new_position

        # Computed based on turning radius
        max_angular_speed = velocity_magnitude / (
            self.base_turning_radius
            + velocity_magnitude * self.turning_radius_to_velocity_ratio
        )

        sign = -1
        if velocity_along_heading < 0 and not drifting:
            sign = 1
        self._sprite.radians += (
            max_angular_speed * sign * delta_time * self.input.x_axis.value
        )
