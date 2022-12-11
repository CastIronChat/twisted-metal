import arcade
import math
from player_input import PlayerInput


import constants
# This is setup for the Player to call "drive_input" where the vehicle updates it's
# intended velocity and rotation based on the player input
# then the player calls "movement" to act on the change from "drive_input"
# this way the inputs are always registered but the movement can be skipped
# if a collision or game state makes it where the vehicle shouldnt act
# This will help avoid race conditions on collisions
# 
# 
# for checking if a vehicle should take damage from an impact. as a percentage of their top acceleration

DEFAULT_WORLD_SIZE = 750
DEFAULT_ACCELERATION_RATE = 1.5
DEFAULT_DECELERATION_RATE = 1.5
DEFAULT_BRAKE_RATE = 0.3
DEFAULT_FRICTION = 0.1
DEFAULT_DRIVE_SPEED = 100
DEFAULT_TURN_SPEED = 50
DEFAULT_VEHICLE_TYPE = 0

IMPACT_FORCE_FLOOR = 1.5


class MovementControls:

    # The stat for max (x,y) linear speed
    drive_speed: float
    # The stat for max rotational speed
    turn_speed: float

    # how fast the current acceleration goes from 0 -> 1
    acceleration_rate: float
    # how fast the brake applies to current acceleration
    decceleration_rate: float
    # how fast the vehicle's current acceleration slows while not accelerating
    friction: float


    # These are the values the vehicle updates in "drive_input"   
    current_velocity_x: float
    current_velocity_y: float
    current_velocity_turn: float
    current_acceleration: float

    # which control scheme to use
    vehicle_type: int
    # for switching between vehicle types
    toggle: bool


    def __init__(self,sprite:arcade.Sprite):
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
        self.decceleration_rate = DEFAULT_BRAKE_RATE
        self.brake_rate = DEFAULT_BRAKE_RATE
        self.friction = DEFAULT_FRICTION
        self.drive_speed = DEFAULT_DRIVE_SPEED
        self.turn_speed = DEFAULT_TURN_SPEED
        self.toggle = False
        self.impact_buffer = 0
        self.vehicle_type = DEFAULT_VEHICLE_TYPE


#   Drive input is called by the player and passed that player's input 
#   to set what the vehicle's velocity and rotation should be
#   Does not change the vehicles position
    def drive_input(self,delta_time: float, input: PlayerInput,vehicle: arcade.Sprite,walls: arcade.SpriteList):
        # for testing to change between driving types
        # TODO:find a permanent place for this logic that is not in movement
        if self.toggle:
            if input.reload_button.value == False:
                self.toggle = False
        else:
            if self.toggle == False and input.reload_button.value == True:
                if input.accelerate_axis.value == 1 and input.brake_axis.value == 1:
                    self.toggle = True
                    self.change_vehicle(vehicle)


        if self.impact_buffer > 0:
                self.impact_buffer -= 1
                if self.impact_buffer <= 0:
                    self.external_velocity_turn = 0

        # updates the vehicles intended  velocity and rotation based on type
        # only the car currently does anything special with checking for wall collisions beyond just not moving into them
        if self.vehicle_type == 0:
            self.car(delta_time,input,vehicle,walls)
        elif self.vehicle_type == 1:
            self.ghost(delta_time,input,vehicle)
        elif self.vehicle_type == 2:
            self.ghost_screen_facing(delta_time,input,vehicle)
        elif self.vehicle_type == 3:
            self.tank(delta_time,input,vehicle)
        elif self.vehicle_type == 4:
            self.mars_walker(delta_time,input,vehicle)

    # called from the player to tell the vehicle to act on it's intended velocity and rotation
    def move(self, vehicle: arcade.Sprite,walls: arcade.SpriteList):
        # the shadow sprite is used to simply math and planning to deal with the arena not being an array
        self.shadow_sprite.center_x = vehicle.center_x + self.current_velocity_x
        self.shadow_sprite.center_y = vehicle.center_y + self.current_velocity_y
        self.shadow_sprite.angle = self.current_velocity_turn + vehicle.angle + self.external_velocity_turn
        walls_touching_player = arcade.check_for_collision_with_list(
            self.shadow_sprite, walls
        )
        if len(walls_touching_player) > 0:
            if self.impact_buffer < 2:
                self.impact_buffer += 1
                self.external_velocity_turn +=  .02 * self.turn_speed * math.copysign(abs(self.current_velocity_x - self.current_velocity_y),(self.current_velocity_x - self.current_velocity_y))
            # collided with a wall, which should push against the car
            
            # high speed impact should damage the car, and greatly cut the velocity 
            if self.current_acceleration > IMPACT_FORCE_FLOOR:
                self.current_velocity_x -= self.current_velocity_x * .5
                self.current_velocity_y -= self.current_velocity_y * .5
            else:
                self.current_acceleration -= self.current_acceleration * .1
                self.current_velocity_x -= self.current_velocity_x * .1
                self.current_velocity_y -= self.current_velocity_y * .1
                if abs(self.current_acceleration) < .1:
                    self.current_acceleration = 0
                    self.current_velocity_x = 0
                    self.current_velocity_y = 0

            self.shadow_sprite.center_x = vehicle.center_x 
            self.shadow_sprite.center_y = vehicle.center_y
        else:
            # no wall collisions means a valid spot to move to
            vehicle.center_x = self.shadow_sprite.center_x
            vehicle.center_y = self.shadow_sprite.center_y


        vehicle.angle  = self.shadow_sprite.angle
        # NOTE: place holder boundaries to wrap aroung like pacman
        if self.debug_world_boundary != 0:
            vehicle.center_x = vehicle.center_x % self.debug_world_boundary
            vehicle.center_y = vehicle.center_y % self.debug_world_boundary
 

    def change_vehicle(self,vehicle: arcade.Sprite):
        self.current_acceleration = 0
        self.current_velocity_x = 0
        self.current_velocity_y = 0
        self.current_velocity_turn = 0
        self.vehicle_type += 1

        if self.vehicle_type > 4:
            self.vehicle_type = 0



    def car(self,delta_time: float, input: PlayerInput,vehicle: arcade.Sprite,walls: arcade.SpriteList):
        # speed progressing from 0 to max while either acceleration is held
        # otherwise the car should coast to a stop using the friction value [TODO:that should be a constant]

        acceleration_change = 0
        self.shadow_sprite.center_x = vehicle.center_x
        self.shadow_sprite.center_y = vehicle.center_y

        


        if input.accelerate_axis.value:
            if self.current_acceleration < 0:
                acceleration_change += self.brake_rate
            acceleration_change += self.acceleration_rate
        elif input.brake_axis.value:
            acceleration_change -= self.decceleration_rate
        else:
            if abs(self.current_acceleration) != 0:
                if abs(self.current_acceleration) <= delta_time * self.friction:
                    self.current_acceleration = 0
                else:
                    acceleration_change -= math.copysign(1,self.current_acceleration) * self.friction
        # the current acceleration is used to have speed progress from zero to its maximum 
        self.current_acceleration = self.clamp(self.current_acceleration + (acceleration_change * delta_time),-1,1)

        # NOTE: because of the place holder sprite's facing add 90 degrees
        car_angle = math.radians(vehicle.angle)

        # find the X and Y movement based on the angle of the sprite
        self.current_velocity_x =  self.drive_speed * math.cos(car_angle) * self.current_acceleration * delta_time
        self.current_velocity_y =  self.drive_speed * math.sin(car_angle) * self.current_acceleration * delta_time

        # a stationary car cant turn
        turn_change  = input.x_axis.value * self.turn_speed * delta_time * -self.current_acceleration

        # check if there is room to turn
        self.shadow_sprite.angle = vehicle.angle + turn_change
        walls_touching_player = arcade.check_for_collision_with_list(
            self.shadow_sprite, walls
        )
        if len(walls_touching_player) > 0:
            turn_change = 0

        self.current_velocity_turn  = turn_change

    def tank(self,delta_time: float, input: PlayerInput,vehicle: arcade.Sprite):
        # drive as if on two treads set to the leftstick  Y and rightstick Y axis
        # if both inputs are in the same direction, drive in that direction
        acceleration_change = 0
        self.current_velocity_turn = 0

        diff_axis_value = input.y_axis.value - input.ry_axis.value
        self.current_velocity_turn  = diff_axis_value * -self.turn_speed * delta_time
        pass
        if input.y_axis.value > 0.1 and input.ry_axis.value > 0.1:
            acceleration_change += self.acceleration_rate
        elif input.y_axis.value < -0.1 and input.ry_axis.value < -0.1:
            acceleration_change -= self.acceleration_rate
        else:
            self.current_velocity_turn  = input.y_axis.value * -self.turn_speed * delta_time
            self.current_velocity_turn  += input.ry_axis.value * self.turn_speed * delta_time
            if abs(self.current_acceleration) != 0:
                if abs(self.current_acceleration) <= delta_time * self.friction:
                    self.current_acceleration = 0
                else:
                    acceleration_change -= math.copysign(1,self.current_acceleration) * self.friction
        # the current acceleration is used to have speed progress from zero to its maximum 
        self.current_acceleration = self.clamp(self.current_acceleration + (acceleration_change * delta_time),-1,1)

        # NOTE: because of the place holder sprite's facing add 90 degrees
        car_angle = math.radians(vehicle.angle)

        # find the X and Y movement based on the angle of the sprite
        self.current_velocity_x =  self.drive_speed * math.cos(car_angle) * self.current_acceleration * delta_time
        self.current_velocity_y =  self.drive_speed * math.sin(car_angle) * self.current_acceleration * delta_time


        
    def ghost(self,delta_time: float, input: PlayerInput, vehicle: arcade.Sprite):
        # move in the direction of the x/y axis input relative to the car's angle

        acceleration_change = 0
        if input.brake_axis.value:
            acceleration_change -= self.decceleration_rate
        elif input.x_axis.value != 0 or input.y_axis.value != 0:
            acceleration_change += self.acceleration_rate
        else:
            if abs(self.current_acceleration) != 0:
                if abs(self.current_acceleration) <= delta_time * self.friction:
                    self.current_acceleration = 0
                else:
                    acceleration_change -= self.friction
        
        # the current acceleration is used to have speed progress from zero to its maximum 
        self.current_acceleration = self.clamp(self.current_acceleration + (acceleration_change * delta_time),0,1)

        # NOTE: because of the place holder sprite's facing add 90 degrees
        car_angle = math.radians(vehicle.angle )

        xNormalized = input.x_axis.value 
        yNormalized = input.y_axis.value

        if abs(input.y_axis.value) + abs(input.x_axis.value) > 1:
            xNormalized = input.x_axis.value / (input.y_axis.value + input.x_axis.value)
            yNormalized = input.y_axis.value / (input.y_axis.value + input.x_axis.value)

            
        self.current_velocity_y =  self.drive_speed * ((math.cos(car_angle) * input.y_axis.value) + (math.sin(car_angle) * input.x_axis.value)) * self.current_acceleration * delta_time
        self.current_velocity_x =  self.drive_speed * ((math.sin(car_angle) * input.y_axis.value) - (math.cos(car_angle) * input.x_axis.value)) * self.current_acceleration * delta_time 

        # a stationary car cant turn
        self.current_velocity_turn = input.rx_axis.value * self.turn_speed * delta_time 


    def ghost_screen_facing(self,delta_time: float, input: PlayerInput, vehicle: arcade.Sprite):
        # ghost controls but agnostic of the current facing of the car


        acceleration_change = 0
        if input.x_axis.value != 0 or input.y_axis.value != 0 :
            acceleration_change += self.acceleration_rate * delta_time
        else:
            if abs(self.current_acceleration) != 0:
                if abs(self.current_acceleration) <= delta_time * self.friction:
                    self.current_acceleration = 0
                else:
                    acceleration_change -= delta_time * self.friction
        
        # the current acceleration is used to have speed progress from zero to its maximum 
        self.current_acceleration = self.clamp(self.current_acceleration + (acceleration_change * delta_time),0,1)

        xNormalized = input.x_axis.value
        yNormalized = input.y_axis.value
        if abs(input.y_axis.value) + abs(input.x_axis.value) > 1:
            xNormalized = input.x_axis.value / (abs(input.y_axis.value) + abs(input.x_axis.value))
            yNormalized = input.y_axis.value / (abs(input.y_axis.value) + abs(input.x_axis.value))



        self.current_velocity_y =  self.drive_speed * yNormalized * self.current_acceleration 
        self.current_velocity_x =  self.drive_speed * xNormalized * self.current_acceleration 
        
        self.current_velocity_turn  = input.rx_axis.value * self.turn_speed * delta_time 

    def mars_walker(self,delta_time: float, input: PlayerInput,vehicle: arcade.Sprite):
        # speed progressing from 0 to max while either acceleration is held
        # otherwise the car should coast to a stop using the friction value [TODO:that should be a constant]


        if input.x_axis.value != 0:
            self.current_velocity_x = 0
            self.current_velocity_y = 0
            self.current_velocity_turn  = input.x_axis.value * self.turn_speed * delta_time 
        else:
            self.current_velocity_turn  = 0
            car_angle = math.radians(vehicle.angle)

            # find the X and Y movement based on the angle of the sprite
            self.current_velocity_x =  self.drive_speed * math.cos(car_angle) * input.accelerate_axis.value * delta_time
            self.current_velocity_y =  self.drive_speed * math.sin(car_angle) * input.accelerate_axis.value * delta_time






    def clamp(self,num, min_value, max_value):
        return max(min(num, max_value), min_value)