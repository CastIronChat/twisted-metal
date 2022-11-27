from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Tuple
import math
import arcade
from linked_sprite import LinkedSprite
from textures import LASER_PISTOL, ROCKET_LAUNCHER, MACHINE_GUN, ROCKET
from iron_math import add_vec, move_sprite_relative_to_parent, polar_to_cartesian
from player_input import VirtualButton

# This allows a circular import only for the purposes of type hints
# Weapon will never create and instance of Player
if TYPE_CHECKING:
    from player import Player


class Weapon:
    """
    Slotted into player's car and behaves according to it's subclass weapon type
    """

    input_button: VirtualButton
    player: Player
    time_since_shoot: float
    weapon_icon: arcade.texture
    muzzle_transform: Tuple[float, float, float]

    def __init__(
        self,
        player: Player,
        input_button: VirtualButton,
        weapon_transform: Tuple[float, float, float],
    ):
        self.input_button = input_button
        self.player = player
        self.weapon_transform = weapon_transform
        self.time_since_shoot = 100
        self.weapon_sprite = arcade.Sprite(texture=self.weapon_icon, scale=3)
        self.setup()

    def setup(self):
        """
        Override this method if you want to add initialization logic without
        writing a verbose __init__
        This method will be called by Weapon's __init__
        """
        ...

    def update(self):
        move_sprite_relative_to_parent(
            self.weapon_sprite, self.player.sprite, self.weapon_transform
        )

    def swap_out(self):
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

    def setup(self):
        self.beam_range = 500
        self.beam_projection: SpriteForBeam = SpriteForBeam(self)
        self.muzzle_transform = (20, 5, 0)
        self.beam_projection.properties["yeah_its_a_hack_come_at_me_bro"] = add_vec(
            self.weapon_transform, self.muzzle_transform[:2]
        )

    def update(self, delta_time):
        super().update()
        if self.input_button.pressed:
            self.shoot()
        if self.input_button.released and self.beam_projection in self.player.beam_list:
            self.player.beam_list.remove(self.beam_projection)

    def shoot(self):
        self.player.beam_list.append(self.beam_projection)

    def swap_out(self):
        if self.beam_projection in self.player.beam_list:
            self.player.beam_list.remove(self.beam_projection)


class RocketLauncher(Weapon):
    """
    Fires a projectile that is now independent of the ship and travels unil it reaches a designated distance
    """

    rocket_speed: float
    fire_rate: float
    weapon_icon = ROCKET_LAUNCHER

    def setup(self):
        self.rocket_speed = 300
        self.fire_rate = 0.5
        # the -45 degree angle in the offset corrects for rocket texture angled up 45 degrees
        self.muzzle_transform = (30, 2, math.radians(-45))

    def update(self, delta_time):
        super().update()
        if self.input_button.pressed:
            if self.time_since_shoot > 1 / self.fire_rate:
                self.shoot()
        self.time_since_shoot += delta_time

    def shoot(self):
        rocket: SpriteForRocket = SpriteForRocket(self)
        move_sprite_relative_to_parent(
            rocket, self.weapon_sprite, self.muzzle_transform
        )
        rocket.velocity = polar_to_cartesian(
            self.rocket_speed, self.weapon_sprite.radians
        )
        self.time_since_shoot = 0
        self.player.projectile_list.append(rocket)


class MachineGun(Weapon):
    """
    Fires many projectiles that move idependently from each other at a given fire rate
    """

    bullet_speed: float
    fire_rate: float
    weapon_icon = MACHINE_GUN

    def setup(self):
        self.bullet_speed = 500
        self.fire_rate = 10
        self.muzzle_transform = (20, 7, 0)

    def update(self, delta_time):
        super().update()
        if self.input_button.value and self.time_since_shoot > 1 / self.fire_rate:
            self.shoot()
        self.time_since_shoot += delta_time

    def shoot(self):
        bullet: SpriteForMachineGun = SpriteForMachineGun(self)
        move_sprite_relative_to_parent(
            bullet, self.weapon_sprite, self.muzzle_transform
        )
        bullet.velocity = polar_to_cartesian(
            self.bullet_speed, self.weapon_sprite.radians
        )
        self.time_since_shoot = 0
        self.player.projectile_list.append(bullet)


class SpriteForBeam(arcade.SpriteSolidColor):
    def __init__(self, laser_beam: LaserBeam):
        self.beam_range = laser_beam.beam_range
        super().__init__(self.beam_range, 5, arcade.color.RED)
        self.laser_beam = laser_beam


class SpriteForMachineGun(arcade.SpriteSolidColor):
    def __init__(self, machine_gun: MachineGun):
        super().__init__(10, 5, arcade.color.RED)
        self.machine_gun = machine_gun


class SpriteForRocket(arcade.Sprite):
    def __init__(self, rocket: RocketLauncher):
        super().__init__(texture=ROCKET, scale=2)
        self.rocket = rocket
