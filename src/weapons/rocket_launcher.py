from __future__ import annotations

import math

import arcade

from iron_math import get_transformed_location, move_sprite_relative_to_parent
from linked_sprite import LinkedSprite
from ordnances.explosion import Explosion
from ordnances.ordnance import Ordnance
from ordnances.projectile import Projectile
from textures import ROCKET, ROCKET_LAUNCHER
from weapons.weapon import Weapon


class RocketLauncher(Weapon):
    """
    Fires a projectile that is now independent of the ship and travels unil it reaches a designated distance
    """

    rocket_speed: float
    impact_damage: float
    explosion_damage: float
    fire_rate: float
    explosion_radius: float
    explosion_rate: float
    weapon_icon = ROCKET_LAUNCHER

    def setup(self):
        self.rocket_speed = 550
        self.impact_damage = 0
        self.explosion_damage = 80
        self.fire_rate = 0.5
        self.muzzle_transform = (12, 0, 0)
        self.explosion_radius = 75
        self.explosion_rate = 200

    def update(self, delta_time: float):
        if self.input_button.pressed:
            if self.time_since_shoot > 1 / self.fire_rate:
                self.shoot()
        self.time_since_shoot += delta_time

    def shoot(self):
        # Create the explosion that will be stored in the payload of the rocket
        explosion = Explosion(
            arcade.color.ORANGE_RED,
            self.sprite_lists,
            [],
            self.explosion_damage,
            self.explosion_radius,
            self.explosion_rate,
        )
        # Create the rocket
        rocket_appearance = LinkedSprite[Ordnance](texture=ROCKET, scale=1)
        rocket = Projectile(
            rocket_appearance,
            self.sprite_lists,
            [explosion],
            self.impact_damage,
            get_transformed_location(self.weapon_sprite, self.muzzle_transform),
            self.rocket_speed,
            self.weapon_sprite.radians,
            sprite_rotation_offet=math.radians(-45),
        )
        # ROCKET texture appears at 45 degree angle. Sprite_rotation_offset compensates for this
        self.time_since_shoot = 0
