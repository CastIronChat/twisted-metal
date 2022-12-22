from __future__ import annotations

import arcade

from weapons.weapon import Weapon
from iron_math import get_transformed_location, move_sprite_relative_to_parent
from linked_sprite import LinkedSpriteSolidColor
from ordnances.ordnance import Ordnance
from ordnances.beam import Beam
from textures import LASER_PISTOL

class LaserBeam(Weapon):
    """
    stays on while button is pressed and moved with the ship
    """

    beam: Beam
    beam_range: float
    dps: float
    # Is a class attribute, not instance attribute
    weapon_icon = LASER_PISTOL

    def setup(self):
        self.beam_range = 400
        self.dps = 20
        self.muzzle_transform = (7, 2, 0)
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
        beam_appearance = LinkedSpriteSolidColor[Ordnance](
            self.beam_range, 3, arcade.color.RED
        )
        self.beam = Beam(
            beam_appearance, self.sprite_lists, [], self.dps, self.beam_range
        )

    def aim_beam(self):
        if self.beam.exists:
            self.beam.muzzle_location = get_transformed_location(
                self.weapon_sprite, self.muzzle_transform
            )