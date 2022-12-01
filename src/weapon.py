from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Tuple
import math
from bullet import Projectile, Beam
import arcade
from sprite_lists import SpriteLists
from linked_sprite import LinkedSprite, LinkedSpriteSolidColor
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
    sprite_lists: SpriteLists  
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
        self.sprite_lists = player.sprite_lists
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

    my_beam_sprite: arcade.Sprite
    beam_range: float
    dps: float
    # Is a class attribute, not instance attribute
    weapon_icon = LASER_PISTOL

    def setup(self):
        self.beam_range = 500
        self.dps = 5
        self.muzzle_transform = (20 + self.beam_range / 2, 5, 0)
        self.my_beam_sprite = None

    def update(self, delta_time: float):
        super().update()
        if self.input_button.pressed:
            self.shoot()
        if self.input_button.released:
            self.remove_beam()

    def shoot(self):
        beam_appearance = LinkedSpriteSolidColor[Beam](
            self.beam_range, 5, arcade.color.RED
        )
        beam = Beam(beam_appearance, self.sprite_lists.beam_sprite_list, self)
        beam.dps = self.dps
        self.my_beam_sprite = beam.sprite

    def swap_out(self):
        self.remove_beam()

    def remove_beam(self):
        if self.my_beam_sprite in self.sprite_lists.beam_sprite_list:
            self.sprite_lists.beam_sprite_list.remove(self.my_beam_sprite)


class RocketLauncher(Weapon):
    """
    Fires a projectile that is now independent of the ship and travels unil it reaches a designated distance
    """

    rocket_speed: float
    fire_rate: float
    damage: float
    weapon_icon = ROCKET_LAUNCHER

    def setup(self):
        self.rocket_speed = 300
        self.fire_rate = 0.5
        self.damage = 80
        # the -45 degree angle in the offset corrects for rocket texture angled up 45 degrees
        self.muzzle_transform = (30, 2, math.radians(-45))

    def update(self, delta_time: float):
        super().update()
        if self.input_button.pressed:
            if self.time_since_shoot > 1 / self.fire_rate:
                self.shoot()
        self.time_since_shoot += delta_time

    def shoot(self):
        rocket_appearance = LinkedSprite[Projectile](texture=ROCKET, scale=2)
        rocket = Projectile(rocket_appearance, self.sprite_lists.projectile_sprite_list)
        rocket.damage = self.damage
        move_sprite_relative_to_parent(
            rocket.sprite, self.weapon_sprite, self.muzzle_transform
        )
        rocket.sprite.velocity = polar_to_cartesian(
            self.rocket_speed, self.weapon_sprite.radians
        )
        self.time_since_shoot = 0


class MachineGun(Weapon):
    """
    Fires many projectiles that move idependently from each other at a given fire rate
    """

    bullet_speed: float
    fire_rate: float
    damage: float
    weapon_icon = MACHINE_GUN

    def setup(self):
        self.bullet_speed = 500
        self.fire_rate = 10
        self.damage = 10
        self.muzzle_transform = (20, 7, 0)

    def update(self, delta_time):
        super().update()
        if self.input_button.value and self.time_since_shoot > 1 / self.fire_rate:
            self.shoot()
        self.time_since_shoot += delta_time

    def shoot(self):
        bullet_appearance = LinkedSpriteSolidColor[Projectile](10, 5, arcade.color.RED)
        bullet = Projectile(bullet_appearance, self.sprite_lists.projectile_sprite_list)
        bullet.damage = self.damage
        move_sprite_relative_to_parent(
            bullet.sprite, self.weapon_sprite, self.muzzle_transform
        )
        bullet.sprite.velocity = polar_to_cartesian(
            self.bullet_speed, self.weapon_sprite.radians
        )
        self.time_since_shoot = 0
