import arcade
import math
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

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


class LaserBeam(Weapon):
    """
    stays on while button is pressed and moved with the ship
    """

    beam_projection: arcade.Sprite
    button_held: bool

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        super().__init__(input_button, car)
        self.beam_projection = arcade.SpriteSolidColor(1000, 5, arcade.color.RED)
        self.button_held = False

    def update(self, delta_time, projectile_list: arcade.SpriteList, beam_list: arcade.SpriteList):
        if self.input_button.pressed:
            self.shoot(beam_list)
        if self.button_held:
            if not self.input_button.value:
                self.remove_bullets(beam_list)

    def shoot(self, beam_list: arcade.SpriteList):
        self.button_held = True
        beam_list.append(self.beam_projection)

    def remove_bullets(self, beam_list: arcade.SpriteList):
        beam_list.remove(self.beam_projection)
        self.button_held = False


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
        self.update_active_weapon(delta_time)

    def shoot(self, projectile_list: arcade.SpriteList):
        rocket = arcade.SpriteSolidColor(50, 30, arcade.color.ORANGE)
        rocket.center_x = self.car.center_x
        rocket.center_y = self.car.center_y
        rocket_angle = self.car.radians
        rocket.change_x = self.rocket_speed * math.cos(rocket_angle)
        rocket.change_y = self.rocket_speed * math.sin(rocket_angle)
        rocket.angle = self.car.angle
        self.time_since_shoot = 0
        projectile_list.append(rocket)

    def update_active_weapon(self, delta_time):
        self.time_since_shoot += delta_time


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
        bullet.angle = self.car.angle
        bullet_angle = self.car.radians
        bullet.change_x = self.bullet_speed * math.cos(bullet_angle)
        bullet.change_y = self.bullet_speed * math.sin(bullet_angle)
        self.time_since_shoot = 0
        projectile_list.append(bullet)
