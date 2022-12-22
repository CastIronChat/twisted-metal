from __future__ import annotations

import math
from typing import TYPE_CHECKING, Tuple

import arcade

from iron_math import get_transformed_location, move_sprite_relative_to_parent
from linked_sprite import LinkedSprite, LinkedSpriteCircle, LinkedSpriteSolidColor
from player_input import VirtualButton
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
        self.weapon_sprite = arcade.Sprite(texture=self.weapon_icon, scale=1)
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
