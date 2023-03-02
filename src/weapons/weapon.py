from __future__ import annotations

from typing import Tuple

import arcade

from player_input import VirtualButton
from sprite_lists import SpriteLists
from audio import TwistedSound


class Weapon:
    """
    Slotted into a vehicle and behaves according to it's subclass weapon type
    """

    input_button: VirtualButton
    sprite_lists: SpriteLists
    time_since_shoot: float
    weapon_icon: arcade.texture
    muzzle_transform: Tuple[float, float, float]

    def __init__(
        self,
        sprite_lists: SpriteLists,
        input_button: VirtualButton,
        weapon_transform: Tuple[float, float, float],
    ):
        self.input_button = input_button
        self.sprite_lists = sprite_lists
        self.weapon_transform = weapon_transform
        self.time_since_shoot = 100
        self.weapon_sprite = arcade.Sprite(texture=self.weapon_icon, scale=1)
        self.sprite_lists.vehicle_attachments.append(self.weapon_sprite)
        self.twisted_sound = TwistedSound()
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
        self.sprite_lists.vehicle_attachments.remove(self.weapon_sprite)

    def deactivate(self):
        ...
