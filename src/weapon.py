from __future__ import annotations

import math
from typing import TYPE_CHECKING, Tuple

import arcade

from iron_math import get_transformed_location, move_sprite_relative_to_parent
from linked_sprite import LinkedSprite, LinkedSpriteSolidColor
from player_input import VirtualButton
from projectile import Beam, Projectile
from sprite_lists import SpriteLists
from textures import LASER_PISTOL, MACHINE_GUN, ROCKET, ROCKET_LAUNCHER

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

    beam: Projectile
    beam_range: float
    dps: float
    # Is a class attribute, not instance attribute
    weapon_icon = LASER_PISTOL

    def setup(self):
        self.beam_range = 400
        self.dps = 20
        self.muzzle_transform = (20, 5, 0)
        self.create_beam()

    def update(self, delta_time: float):
        super().update()
        if self.input_button.pressed:
            self.shoot()
        if self.input_button.released:
            self.remove_beam()
        self.aim_beam()

    def shoot(self):
        self.beam.append_sprite()

    def swap_out(self):
        self.remove_beam()

    def remove_beam(self):
        if self.beam.exists:
            self.beam.remove_sprite()

    def create_beam(self):
        beam_appearance = LinkedSpriteSolidColor[Projectile](
            self.beam_range, 5, arcade.color.RED
        )
        self.beam = Beam(beam_appearance, self.sprite_lists, self.dps)
        self.beam.setup(self.beam_range)

    def aim_beam(self):
        if self.beam.exists:
            self.beam.muzzle_location = get_transformed_location(
                self.weapon_sprite, self.muzzle_transform
            )


class RocketLauncher(Weapon):
    """
    Fires a projectile that is now independent of the ship and travels unil it reaches a designated distance
    """

    rocket_speed: float
    rocket_damage: float
    fire_rate: float
    weapon_icon = ROCKET_LAUNCHER

    def setup(self):
        self.rocket_speed = 300
        self.rocket_damage = 80
        self.fire_rate = 0.5
        self.muzzle_transform = (30, 2, 0)

    def update(self, delta_time: float):
        super().update()
        if self.input_button.pressed:
            if self.time_since_shoot > 1 / self.fire_rate:
                self.shoot()
        self.time_since_shoot += delta_time

    def shoot(self):
        rocket_appearance = LinkedSprite[Projectile](texture=ROCKET, scale=2)
        rocket = Projectile(
            rocket_appearance,
            self.sprite_lists,
            self.rocket_damage,
        )
        # ROCKET texture appears at 45 degree angle. Sprite_rotation_offset compensates for this
        rocket.setup(
            get_transformed_location(self.weapon_sprite, self.muzzle_transform),
            self.rocket_speed,
            self.weapon_sprite.radians,
            sprite_rotation_offet=math.radians(-45),
            explodes=True,
        )
        self.time_since_shoot = 0


class MachineGun(Weapon):
    """
    Fires many projectiles that move idependently from each other at a given fire rate
    """

    bullet_speed: float
    bullet_damage: float
    fire_rate: float
    weapon_icon = MACHINE_GUN

    def setup(self):
        self.bullet_speed = 500
        self.bullet_damage = 10
        self.fire_rate = 10
        self.muzzle_transform = (20, 7, 0)

    def update(self, delta_time: float):
        super().update()
        if self.input_button.value and self.time_since_shoot > 1 / self.fire_rate:
            self.shoot()
        self.time_since_shoot += delta_time

    def shoot(self):
        bullet_appearance = LinkedSpriteSolidColor[Projectile](10, 5, arcade.color.RED)
        bullet = Projectile(
            bullet_appearance,
            self.sprite_lists,
            self.bullet_damage,
        )
        bullet.setup(
            get_transformed_location(self.weapon_sprite, self.muzzle_transform),
            self.bullet_speed,
            self.weapon_sprite.radians,
        )
        self.time_since_shoot = 0
