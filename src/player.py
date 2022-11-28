import arcade
import math
from typing import List
from linked_sprite import LinkedSprite
from player_input import PlayerInput
from weapon import Weapon, LaserBeam, RocketLauncher, MachineGun
from textures import RED_CAR


class Player:
    def __init__(
        self,
        input: PlayerInput,
        projectile_spritelist: arcade.SpriteList,
        beam_spritelist: arcade.SpriteList,
    ):
        # self.sprite: SpriteForPlayer = SpriteForPlayer(self)
        self.sprite = LinkedSprite[Player](texture=RED_CAR, scale=0.5)
        self.sprite.owner = self
        self.sprite.center_x = 256
        self.sprite.center_y = 256
        self.input = input
        self.drive_speed = 200
        self.turn_speed = 100
        self.primary_weapon_transform = (50, 20, 0)
        self.secondary_weapon_transform = (50, -20, 0)
        # Weapons
        self.projectile_spritelist = projectile_spritelist
        self.beam_spritelist = beam_spritelist
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

    def update(self, delta_time: float):
        if self.input.accelerate_axis.value > 0:
            self.sprite.angle -= self.turn_speed * delta_time * self.input.x_axis.value
            self.sprite.center_x += (
                self.drive_speed
                * self.input.accelerate_axis.value
                * math.cos(self.sprite.radians)
                * delta_time
            )
            self.sprite.center_y += (
                self.drive_speed
                * self.input.accelerate_axis.value
                * math.sin(self.sprite.radians)
                * delta_time
            )
        if self.input.brake_axis.value > 0:
            self.sprite.angle += self.turn_speed * delta_time * self.input.x_axis.value
            self.sprite.center_x -= (
                self.drive_speed
                * self.input.brake_axis.value
                * math.cos(self.sprite.radians)
                * delta_time
            )
            self.sprite.center_y -= (
                self.drive_speed
                * self.input.brake_axis.value
                * math.sin(self.sprite.radians)
                * delta_time
            )

        self.primary_weapon.update(delta_time)
        self.secondary_weapon.update(delta_time)
        if self.input.swap_weapons_button.pressed:
            self._swap_weapons()

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
