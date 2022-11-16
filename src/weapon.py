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
    bullet_list: arcade.SpriteList
    button_held: bool
    time_since_shoot: float

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        self.bullet_list = arcade.SpriteList()
        self.input_button = input_button
        self.car = car
        self.button_held = False
        self.time_since_shoot = 100

    def update(self):
        ...

    def draw(self):
        self.bullet_list.draw()


class Beam(Weapon):
    """
    stays on while button is pressed and moved with the ship
    """

    beam_projection: arcade.Sprite

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        super().__init__(input_button, car)
        self.beam_projection = arcade.SpriteSolidColor(1000, 5, arcade.color.RED)

    def update(self, delta_time):
        if not self.button_held and self.input_button.value:
            self.shoot()
        if self.button_held:
            self.update_active_weapon()
            if not self.input_button.value:
                self.remove_bullets()

    def shoot(self):
        self.button_held = True
        self.bullet_list.append(self.beam_projection)

    def update_active_weapon(self):
        self.beam_projection.center_x = self.car.center_x
        self.beam_projection.center_y = self.car.center_y
        self.beam_projection.angle = self.car.angle

    def remove_bullets(self):
        self.bullet_list.remove(self.beam_projection)
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

    def update(self, delta_time):
        if not self.button_held and self.input_button.value:
            self.button_held = True
            if self.time_since_shoot > 1 / self.fire_rate:
                self.shoot()
        if self.button_held and not self.input_button.value:
            self.button_held = False
        self.update_active_weapon(delta_time)
        self.remove_bullets()

    def shoot(self):
        rocket = arcade.SpriteSolidColor(50, 30, arcade.color.ORANGE)
        rocket.center_x = self.car.center_x
        rocket.center_y = self.car.center_y
        rocket.angle = self.car.angle
        self.time_since_shoot = 0
        self.bullet_list.append(rocket)

    def update_active_weapon(self, delta_time):
        for rocket in self.bullet_list:
            rocket.center_x += (
                self.rocket_speed * math.cos(math.radians(rocket.angle)) * delta_time
            )
            rocket.center_y += (
                self.rocket_speed * math.sin(math.radians(rocket.angle)) * delta_time
            )
        self.time_since_shoot += delta_time

    def remove_bullets(self):
        for rocket in self.bullet_list:
            if (
                rocket.center_x < 0
                or rocket.center_x > SCREEN_WIDTH - 300
                or rocket.center_y < 0
                or rocket.center_y > SCREEN_HEIGHT
            ):
                self.bullet_list.remove(rocket)


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

    def update(self, delta_time):
        if self.input_button.value and self.time_since_shoot > 1 / self.fire_rate:
            self.shoot()
        self.remove_bullets()
        for bullet in self.bullet_list:
            bullet.center_x += bullet.change_x * delta_time
            bullet.center_y += bullet.change_y * delta_time
        self.time_since_shoot += delta_time

    def shoot(self):
        bullet = arcade.SpriteSolidColor(10, 5, arcade.color.RED)
        bullet.center_x = self.car.center_x
        bullet.center_y = self.car.center_y
        bullet.angle = self.car.angle
        bullet_angle = math.radians(self.car.angle)
        bullet.change_x = self.bullet_speed * math.cos(bullet_angle)
        bullet.change_y = self.bullet_speed * math.sin(bullet_angle)
        self.time_since_shoot = 0
        self.bullet_list.append(bullet)

    def remove_bullets(self):
        for bullet in self.bullet_list:
            if (
                bullet.center_x < 0
                or bullet.center_x > SCREEN_WIDTH
                or bullet.center_y < 0
                or bullet.center_y > SCREEN_HEIGHT
            ):
                self.bullet_list.remove(bullet)
