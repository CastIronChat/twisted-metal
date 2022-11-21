import arcade
import math
from typing import List
from iron_math import add_vec2, rotate_vec2
from player_input import PlayerInput
from weapon import Weapon, LaserBeam, Rocket, MachineGun
from movement_controls import MovementControls

from textures import RED_CAR


class Player:
    def __init__(self, input: PlayerInput):
        self.sprite = arcade.Sprite(texture=RED_CAR, scale=0.5)
        self.sprite.center_x = 256
        self.sprite.center_y = 256
        self.input = input
        self.drive_speed = 200
        self.turn_speed = 100
        self.primary_weapon_sprite_offset = (50, 20)
        self.secondary_weapon_sprite_offset = (50, -20)
        # Weapons
        self.projectile_list = arcade.SpriteList()
        self.beam_list = arcade.SpriteList()
        self.weapons_list: List[Weapon] = [
            LaserBeam,
            Rocket,
            MachineGun,
        ]
        self.weapon_index = 0
        self.primary_weapon: Weapon
        self.secondary_weapon: Weapon
        self.primary_weapon_sprite: arcade.Sprite
        self.secondary_weapon_sprite: arcade.Sprite
        self._swap_in_weapons()
        self.player_health = 100
        self.vehicle = MovementControls()

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
        self.primary_weapon.update(delta_time, self.projectile_list, self.beam_list)
        self.secondary_weapon.update(delta_time, self.projectile_list, self.beam_list)
        if self.input.swap_weapons_button.pressed:
            self._swap_weapons()
        # The vehicle updates its intended velocity and rotation
        self.vehicle.drive_input(delta_time,self.input,self.sprite)
        # TODO: Collision and bullet logic to check if the vehicle is able to move
        self.vehicle.move(self.sprite)


    def _swap_weapons(self):
        # Moves the current secondary weapon to the primary weapon slot and the next weapon on the list becomes the secondary weapon
        self._swap_out_weapons()
        self._swap_in_weapons()

    def _swap_out_weapons(self):
        self.primary_weapon.swap_out(self.beam_list)
        self.secondary_weapon.swap_out(self.beam_list)

    def _swap_in_weapons(self):
        self.primary_weapon = self.weapons_list[self.weapon_index](
            self.input.primary_fire_button,
            self.sprite,
            self.primary_weapon_sprite_offset,
        )
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons_list):
            self.weapon_index = 0
        self.secondary_weapon = self.weapons_list[self.weapon_index](
            self.input.secondary_fire_button,
            self.sprite,
            self.secondary_weapon_sprite_offset,
        )

    def draw(self):
        self.projectile_list.draw()
        self.beam_list.draw()
        self.primary_weapon.draw()
        self.secondary_weapon.draw()

