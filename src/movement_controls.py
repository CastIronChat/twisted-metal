import arcade
import math
from player_input import PlayerInput

# This is setup for the Player to call "drive_input" where the vehicle updates it's
# intended velocity and rotation based on the player input
# then the player calls "movement" to act on the change from "drive_input"
# this way the inputs are always registered but the movement can be skipped
# if a collision or game state makes it where the vehicle shouldnt act
# This will help avoid race conditions on collisions
#
#
#


class MovementControls:
    # used to create pacman style screen wrapping preventing vehicles from going off screen
    debug_world_boundary: float
    # The stat for max (x,y) linear speed
    drive_speed: float
    # The stat for max rotational speed
    turn_speed: float

    # how fast the current acceleration goes from 0 -> 1
    acceleration_rate: float
    # how fast the vehicle's current acceleration slows while not accelerating
    friction: float

    # These are the values the vehicle updates in "drive_input"
    current_velocity_x: float
    current_velocity_y: float
    # changed as per requested to be similar to linear movement
    current_velocity_turn: float
    current_acceleration: float

    # which control scheme to use
    vehicle_type: int
    # for switching between vehicle types
    toggle: bool

    def __init__(self):
        self.debug_world_boundary = 750
        self.current_velocity_x = 0
        self.current_velocity_y = 0
        self.current_velocity_turn = 0
        self.current_acceleration = 0
        self.acceleration_rate = 0.9
        self.brake_rate = 0.3
        self.friction = 0.1
        self.drive_speed = 100
        self.turn_speed = 100
        self.toggle = False
        self.vehicle_type = 0

    #   Drive input is called by the player and passed that player's input
    #   to set what the vehicle's Velocity and rotation should be
    #   Does not change the vehicles position
    #   Does not need a just x,y position and angle.
    def drive_input(self, delta_time, input, vehicle: arcade.Sprite):
        # for testing to change between driving types
        # while holding brake and accelerate, pressing reload changes types
        # TODO:find a permanent place for this logic that is not in movement
        if self.toggle:
            if input.reload_button.value == False:
                self.toggle = False
        else:
            if self.toggle == False and input.reload_button.value == True:
                if input.accelerate_axis.value == 1 and input.brake_axis.value == 1:
                    self.toggle = True
                    self.change_vehicle()

        # updates the vehicles intended  velocity and rotation based on type
        if self.vehicle_type == 0:
            self.car(delta_time, input, vehicle)
        elif self.vehicle_type == 1:
            self.ghost(delta_time, input, vehicle)
        elif self.vehicle_type == 2:
            self.ghost_screen_facing(delta_time, input, vehicle)
        elif self.vehicle_type == 3:
            self.tank(delta_time, input, vehicle)
        elif self.vehicle_type == 4:
            self.mars_walker(delta_time, input, vehicle)

    def change_vehicle(self):
        self.current_acceleration = 0
        self.current_velocity_x = 0
        self.current_velocity_y = 0
        self.current_velocity_turn = 0
        self.vehicle_type += 1
        if self.vehicle_type > 4:
            self.vehicle_type = 0

    # called from the player to tell the vehicle to act on it's intended velocity and rotation
    def move(self, vehicle: arcade.Sprite):
        # find the X and Y movement based on the angle of the sprite
        new_x_pos = self.current_velocity_x + vehicle.center_x
        new_y_pos = self.current_velocity_y + vehicle.center_y

        # NOTE: place holder boundaries
        if self.debug_world_boundary != 0:
            new_x_pos = new_x_pos % self.debug_world_boundary
            new_y_pos = new_y_pos % self.debug_world_boundary

        vehicle.center_x = new_x_pos
        vehicle.center_y = new_y_pos

        vehicle.angle += self.current_velocity_turn

    def car(self, delta_time, input, vehicle):
        # speed progressing from 0 to max while either acceleration is held
        # otherwise the car should coast to a stop using the friction value [TODO:that should be a constant]

        acceleration_change = 0

        if input.accelerate_axis.value:
            if self.current_acceleration < 0:
                acceleration_change += self.brake_rate
            acceleration_change += self.acceleration_rate
        elif input.brake_axis.value:
            acceleration_change -= self.brake_rate
        else:
            # if neither brake or acceleration is being held
            # cost to a stop based on friction
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

    def tank(self, delta_time, input, vehicle):
        # drive as if on two treads set to the leftstick  Y and rightstick Y axis
        # if both inputs are in the same direction, drive in that direction
        acceleration_change = 0
        self.current_velocity_turn = 0

        diff_axis_value = input.y_axis.value - input.ry_axis.value
        self.current_velocity_turn = diff_axis_value * -self.turn_speed * delta_time

        if input.y_axis.value > 0.1 and input.ry_axis.value > 0.1:
            acceleration_change += self.acceleration_rate
        elif input.y_axis.value < -0.1 and input.ry_axis.value < -0.1:
            acceleration_change -= self.acceleration_rate

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

    def ghost(self, delta_time, input, vehicle):
        # move in the direction of the x/y axis input relative to the car's angle

        acceleration_change = 0
        if input.brake_axis.value:
            acceleration_change -= self.brake_rate
        elif input.x_axis.value != 0 or input.y_axis.value != 0:
            acceleration_change += self.acceleration_rate
        else:
            if abs(self.current_acceleration) != 0:
                if abs(self.current_acceleration) <= delta_time * self.friction:
                    self.current_acceleration = 0
                else:
                    acceleration_change -= delta_time

        # the current acceleration is used to have speed progress from zero to its maximum
        self.current_acceleration = self.clamp(
            self.current_acceleration + (acceleration_change * delta_time), 0, 1
        )

        car_angle = math.radians(vehicle.angle)

        xNormalized = input.x_axis.value
        yNormalized = input.y_axis.value

        if abs(input.y_axis.value) + abs(input.x_axis.value) > 1:
            xNormalized = input.x_axis.value / (
                abs(input.y_axis.value) + abs(input.x_axis.value)
            )
            yNormalized = input.y_axis.value / (
                abs(input.y_axis.value) + abs(input.x_axis.value)
            )

        self.current_velocity_x = (
            self.drive_speed
            * (
                (math.cos(car_angle) * input.y_axis.value)
                + (math.sin(car_angle) * input.x_axis.value)
            )
            * self.current_acceleration
            * delta_time
        )
        self.current_velocity_y = (
            self.drive_speed
            * (
                (math.sin(car_angle) * input.y_axis.value)
                - (math.cos(car_angle) * input.x_axis.value)
            )
            * self.current_acceleration
            * delta_time
        )

        # a stationary car cant turn
        self.current_velocity_turn = input.rx_axis.value * -self.turn_speed * delta_time

    def ghost_screen_facing(self, delta_time, input, vehicle):
        # ghost controls but agnostic of the current facing of the car

        acceleration_change = 0
        if input.x_axis.value != 0 or input.y_axis.value != 0:
            acceleration_change += self.acceleration_rate
        else:
            if abs(self.current_acceleration) != 0:
                if abs(self.current_acceleration) <= delta_time * self.friction:
                    self.current_acceleration = 0
                else:
                    acceleration_change -= delta_time * self.friction

        # the current acceleration is used to have speed progress from zero to its maximum
        self.current_acceleration = self.clamp(
            self.current_acceleration + (acceleration_change * delta_time), 0, 1
        )

        car_angle = math.radians(vehicle.angle)

        xNormalized = input.x_axis.value
        yNormalized = input.y_axis.value
        if abs(input.y_axis.value) + abs(input.x_axis.value) > 1:
            xNormalized = input.x_axis.value / (
                abs(input.y_axis.value) + abs(input.x_axis.value)
            )
            yNormalized = input.y_axis.value / (
                abs(input.y_axis.value) + abs(input.x_axis.value)
            )

        self.current_velocity_y = (
            self.drive_speed * yNormalized * self.current_acceleration * delta_time
        )
        self.current_velocity_x = (
            self.drive_speed * xNormalized * self.current_acceleration * delta_time
        )

        self.current_velocity_turn = input.rx_axis.value * -self.turn_speed * delta_time

    def mars_walker(self, delta_time, input, vehicle):
        # speed progressing from 0 to max while either acceleration is held
        # otherwise the car should coast to a stop using the friction value [TODO:that should be a constant]

        if input.x_axis.value != 0:
            self.current_velocity_x = 0
            self.current_velocity_y = 0
            self.current_velocity_turn = (
                input.x_axis.value * -self.turn_speed * delta_time
            )
        else:
            self.current_velocity_turn = 0
            car_angle = math.radians(vehicle.angle)

            # find the X and Y movement based on the angle of the sprite
            self.current_velocity_x = (
                self.drive_speed
                * math.cos(car_angle)
                * input.accelerate_axis.value
                * delta_time
            )
            self.current_velocity_y = (
                self.drive_speed
                * math.sin(car_angle)
                * input.accelerate_axis.value
                * delta_time
            )

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)
