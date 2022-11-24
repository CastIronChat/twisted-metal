from typing import Tuple
import arcade
import math
from textures import LASER_PISTOL, ROCKET_LAUNCHER, MACHINE_GUN
from iron_math import add_vec2, rotate_vec2
from player_input import VirtualButton


class Weapon:
    """
    Slotted into player's car and behaves according to it's subclass weapon type
    """

    input_button: VirtualButton
    car: arcade.Sprite
    time_since_shoot: float
    weapon_icon: arcade.texture

    def __init__(
        self,
        input_button: VirtualButton,
        car: arcade.Sprite,
        weapon_sprite_offset: Tuple[float, float],
    ):
        self.input_button = input_button
        self.car = car
        self.weapon_sprite_offset = weapon_sprite_offset
        self.time_since_shoot = 100
        self.weapon_sprite = arcade.Sprite(texture=self.weapon_icon, scale=3)

    def update(self):
        self.weapon_sprite.angle = self.car.angle
        self.weapon_sprite.position = add_vec2(
            self.car.position,
            rotate_vec2(self.weapon_sprite_offset, self.car.radians),
        )

    def swap_out(self, beam_list: arcade.SpriteList):
        pass

    def draw(self):
        self.weapon_sprite.draw()


class LaserBeam(Weapon):
    """
    stays on while button is pressed and moved with the ship
    """

    beam_projection: arcade.Sprite
    beam_range: float
    # Is a class attribute, not instance attribute
    weapon_icon = LASER_PISTOL

    def __init__(
        self,
        input_button: VirtualButton,
        car: arcade.Sprite,
        weapon_sprite_offset: Tuple[float, float],
    ):
        super().__init__(input_button, car, weapon_sprite_offset)
        self.beam_range = 500
        self.beam_projection: SpriteForBeam = SpriteForBeam(self)

        self.beam_projection.properties[
            "yeah_its_a_hack_come_at_me_bro"
        ] = self.weapon_sprite_offset

    def update(
        self,
        delta_time,
        projectile_list: arcade.SpriteList,
        beam_list: arcade.SpriteList,
    ):
        super().update()
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
    weapon_icon = ROCKET_LAUNCHER

    def __init__(
        self,
        input_button: VirtualButton,
        car: arcade.Sprite,
        weapon_sprite_offset: Tuple[float, float],
    ):
        super().__init__(input_button, car, weapon_sprite_offset)
        self.rocket_speed = 300
        self.fire_rate = 0.5

    def update(
        self,
        delta_time,
        projectile_list: arcade.SpriteList,
        beam_list: arcade.SpriteList,
    ):
        super().update()
        if self.input_button.pressed:
            if self.time_since_shoot > 1 / self.fire_rate:
                self.shoot(projectile_list)
        self.time_since_shoot += delta_time

    def shoot(self, projectile_list: arcade.SpriteList):
        rocket: SpriteForRocket = SpriteForRocket(self)
        rocket.position = self.weapon_sprite.position
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
    weapon_icon = MACHINE_GUN

    def __init__(
        self,
        input_button: VirtualButton,
        car: arcade.Sprite,
        weapon_sprite_offset: Tuple[float, float],
    ):
        super().__init__(input_button, car, weapon_sprite_offset)
        self.bullet_speed = 500
        self.fire_rate = 10

    def update(
        self,
        delta_time,
        projectile_list: arcade.SpriteList,
        beam_list: arcade.SpriteList,
    ):
        super().update()
        if self.input_button.value and self.time_since_shoot > 1 / self.fire_rate:
            self.shoot(projectile_list)
        self.time_since_shoot += delta_time

    def shoot(self, projectile_list: arcade.SpriteList):
        bullet: SpriteForMachineGun = SpriteForMachineGun(self)
        bullet.position = self.weapon_sprite.position
        bullet.change_x = self.bullet_speed * math.cos(self.weapon_sprite.radians)
        bullet.change_y = self.bullet_speed * math.sin(self.weapon_sprite.radians)
        bullet.angle = self.weapon_sprite.angle
        self.time_since_shoot = 0
        projectile_list.append(bullet)


class SpriteForBeam(arcade.SpriteSolidColor):
    def __init__(self, laser_beam: LaserBeam):
        self.beam_range = laser_beam.beam_range
        super().__init__(self.beam_range, 5, arcade.color.RED)
        self.laser_beam = laser_beam


class SpriteForMachineGun(arcade.SpriteSolidColor):
    def __init__(self, machine_gun: MachineGun):
        super().__init__(10, 5, arcade.color.RED)
        self.machine_gun = machine_gun


class SpriteForRocket(arcade.SpriteSolidColor):
    def __init__(self, rocket: Rocket):
        super().__init__(30, 20, arcade.color.ORANGE)
        self.rocket = rocket
