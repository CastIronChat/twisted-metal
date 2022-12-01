import arcade
from typing import List
from driving.drifty_car import DriftyCar
from linked_sprite import LinkedSprite
from player_input import PlayerInput
from weapon import Weapon, LaserBeam, RocketLauncher, MachineGun
from textures import RED_CAR


class Player:
    def __init__(
        self,
        input: PlayerInput,
        projectile_sprite_list: arcade.SpriteList,
        beam_sprite_list: arcade.SpriteList,
    ):
        self.sprite = LinkedSprite[Player](texture=RED_CAR, scale=0.2)
        self.sprite.owner = self
        self.sprite.center_x = 256
        self.sprite.center_y = 256
        self.input = input
        self.primary_weapon_transform = (15, 5, 0)
        self.secondary_weapon_transform = (15, -5, 0)
        # Weapons
        self.projectile_sprite_list = projectile_sprite_list
        self.beam_sprite_list = beam_sprite_list
        self.weapons_list: List[Weapon] = [
            LaserBeam,
            RocketLauncher,
            MachineGun,
        ]
        self.weapon_index = 0
        self.primary_weapon: Weapon
        self.secondary_weapon: Weapon
        self.primary_weapon_sprite: arcade.Sprite
        self.secondary_weapon_sprite: arcade.Sprite
        self._swap_in_weapons()
        self.player_health = 100

        self.drive_mode_index = 0
        self.drive_modes = [DriftyCar(self)]

    def update(self, delta_time: float):
        if self.input.debug_2.pressed:
            self._swap_drive_mode()

        self.drive_modes[self.drive_mode_index].update(delta_time)
        self.primary_weapon.update(delta_time)
        self.secondary_weapon.update(delta_time)
        if self.input.swap_weapons_button.pressed:
            self._swap_weapons()

    def _swap_drive_mode(self):
        self.drive_mode_index += 1
        if self.drive_mode_index >= len(self.drive_modes):
            self.drive_mode_index = 0

    def _swap_weapons(self):
        # Moves the current secondary weapon to the primary weapon slot and the next weapon on the list becomes the secondary weapon
        self._swap_out_weapons()
        self._swap_in_weapons()

    def _swap_out_weapons(self):
        self.primary_weapon.swap_out()
        self.secondary_weapon.swap_out()

    def _swap_in_weapons(self):
        self.primary_weapon = self.weapons_list[self.weapon_index](
            self,
            self.input.primary_fire_button,
            self.primary_weapon_transform,
        )
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons_list):
            self.weapon_index = 0
        self.secondary_weapon = self.weapons_list[self.weapon_index](
            self,
            self.input.secondary_fire_button,
            self.secondary_weapon_transform,
        )

    def draw(self):
        self.primary_weapon.draw()
        self.secondary_weapon.draw()
