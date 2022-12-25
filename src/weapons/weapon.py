from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import arcade

from iron_math import move_sprite_relative_to_parent
from player_input import VirtualButton
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
if TYPE_CHECKING:
    from vehicle import Vehicle


class Weapon:
    """
    Slotted into a vehicle and behaves according to it's subclass weapon type
    """

    input_button: VirtualButton
    vehicle: Vehicle
    sprite_lists: SpriteLists
    time_since_shoot: float
    weapon_icon: arcade.texture
    muzzle_transform: Tuple[float, float, float]

    def __init__(
        self,
        vehicle: Vehicle,
        input_button: VirtualButton,
        weapon_transform: Tuple[float, float, float],
    ):
        self.input_button = input_button
        self.vehicle = vehicle
        self.sprite_lists = vehicle.sprite_lists
        self.weapon_transform = weapon_transform
        self.time_since_shoot = 100
        self.weapon_sprite = arcade.Sprite(texture=self.weapon_icon, scale=1)
        self.sprite_lists.weapons.append(self.weapon_sprite)
        self.setup()

    def setup(self):
        """
        Override this method if you want to add initialization logic without
        writing a verbose __init__
        This method will be called by Weapon's __init__
        """
        ...

    def update(self):
        ...

    def swap_out(self):
        self.sprite_lists.weapons.remove(self.weapon_sprite)
