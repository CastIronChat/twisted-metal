from __future__ import annotations

import arcade

from iron_math import get_transformed_location, move_sprite_relative_to_parent
from linked_sprite import LinkedSpriteSolidColor
from ordnances.ordnance import Ordnance
from ordnances.projectile import Projectile
from textures import MACHINE_GUN
from weapons.weapon import Weapon


class MachineGun(Weapon):
    """
    Fires many projectiles that move idependently from each other at a given fire rate
    """

    bullet_speed: float
    bullet_damage: float
    fire_rate: float
    weapon_icon = MACHINE_GUN

    def setup(self):
        self.bullet_speed = 800
        self.bullet_damage = 10
        self.fire_rate = 8
        self.muzzle_transform = (7, 2, 0)

    def update(self, delta_time: float):
        if self.input_button.value and self.time_since_shoot > 1 / self.fire_rate:
            self.shoot()
        self.time_since_shoot += delta_time

    def shoot(self):
        bullet_appearance = LinkedSpriteSolidColor[Ordnance](8, 3, arcade.color.RED)
        bullet = Projectile(
            bullet_appearance,
            self.sprite_lists,
            self.bullet_damage,
            get_transformed_location(self.weapon_sprite, self.muzzle_transform),
            self.bullet_speed,
            self.weapon_sprite.radians,
        )
        self.twisted_sound.play(self.twisted_sound.machine_gun1)
        self.time_since_shoot = 0
