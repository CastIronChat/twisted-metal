import arcade
import math

from player_input import VirtualButton


class Weapon:
    """
    Slotted into player's car and behaves according to it's subclass weapon type
    """

    input_button: VirtualButton
    car: arcade.Sprite
    time_since_shoot: float

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        self.input_button = input_button
        self.car = car
        self.time_since_shoot = 100

    def update(self):
        ...

    def swap_out(self, beam_list: arcade.SpriteList):
        pass


class LaserBeam(Weapon):
    """
    stays on while button is pressed and moved with the ship
    """

    beam_projection: arcade.Sprite
    beam_range: float


    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        super().__init__(input_button, car)
        self.beam_range = 500
        self.beam_projection = arcade.SpriteSolidColor(self.beam_range, 5, arcade.color.RED)
        #this is currently used to store half the lenght so the update method can make the beam not centered on the car
        self.beam_projection.velocity = self.beam_range/2

    def update(self, delta_time, projectile_list: arcade.SpriteList, beam_list: arcade.SpriteList):
        if self.input_button.pressed:
            self.shoot(beam_list)
        if self.input_button.released and self.beam_projection in beam_list:
            beam_list.remove(self.beam_projection)

    def shoot(self, beam_list: arcade.SpriteList):
        beam_list.append(self.beam_projection)

    def swap_out(self, beam_list: arcade.SpriteList):
        if self.beam_projection in beam_list:
            beam_list.remove(self.beam_projection)



class Rocket(Weapon):
    """
    Fires a projectile that is now independent of the ship and travels unil it reaches a designated distance
    """

    rocket_speed: float
    fire_rate: float

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        super().__init__(input_button, car)
        self.rocket_speed = 200
        self.fire_rate = 0.5

    def update(self, delta_time, projectile_list: arcade.SpriteList, beam_list: arcade.SpriteList):
        if self.input_button.pressed:
            if self.time_since_shoot > 1 / self.fire_rate:
                self.shoot(projectile_list)
        self.time_since_shoot += delta_time

    def shoot(self, projectile_list: arcade.SpriteList):
        rocket = arcade.SpriteSolidColor(50, 30, arcade.color.ORANGE)
        rocket.center_x = self.car.center_x
        rocket.center_y = self.car.center_y
        rocket.change_x = self.rocket_speed * math.cos(self.car.radians)
        rocket.change_y = self.rocket_speed * math.sin(self.car.radians)
        rocket.angle = self.car.angle
        self.time_since_shoot = 0
        projectile_list.append(rocket)

class MachineGun(Weapon):
    """
    Fires many projectiles that move idependently from each other at a given fire rate
    """

    bullet_speed: float
    fire_rate: float

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        super().__init__(input_button, car)
        self.bullet_speed = 300
        self.fire_rate = 10

    def update(self, delta_time, projectile_list: arcade.SpriteList, beam_list: arcade.SpriteList):
        if self.input_button.value and self.time_since_shoot > 1 / self.fire_rate:
            self.shoot(projectile_list)
        self.time_since_shoot += delta_time

    def shoot(self, projectile_list: arcade.SpriteList):
        bullet = arcade.SpriteSolidColor(10, 5, arcade.color.RED)
        bullet.center_x = self.car.center_x
        bullet.center_y = self.car.center_y
        bullet.change_x = self.bullet_speed * math.cos(self.car.radians)
        bullet.change_y = self.bullet_speed * math.sin(self.car.radians)
        self.time_since_shoot = 0
        projectile_list.append(bullet)
