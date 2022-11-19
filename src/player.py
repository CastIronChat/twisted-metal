import arcade
import math

from player_input import PlayerInput
from weapon import Weapon, LaserBeam, Rocket, MachineGun


class Player:
    # TODO seems like the arcade engine wants us to subclass Sprite for all
    # our game entities.  Seems like composition would be better?
    sprite: arcade.Sprite
    weapons_list: list
    projectile_list: arcade.SpriteList
    beam_list: arcade.SpriteList
    input: PlayerInput
    drive_speed: float
    turn_speed: float
    primary_weapon: Weapon
    secondary_weapon: Weapon
    weapon_index: int
    player_health: int

    def __init__(self, input: PlayerInput):
        self.sprite = arcade.Sprite("assets/vehicle/red-car-top-view.png", 0.5)
        self.projectile_list = arcade.SpriteList()
        self.beam_list = arcade.SpriteList()
        self.sprite.center_x = 256
        self.sprite.center_y = 256
        self.input = input
        self.drive_speed = 200
        self.turn_speed = 100
        self.weapons_list = [
            LaserBeam,
            Rocket,
            MachineGun,
        ]
        self.primary_weapon = self.weapons_list[0](self.input.primary_fire_button, self.sprite)
        self.secondary_weapon = self.weapons_list[1](self.input.secondary_fire_button, self.sprite)
        self.weapon_index = 1
        self.player_health = 100

    def update(self, delta_time):
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
            self.swap_weapons()

    def swap_weapons(self):
        self.primary_weapon.swap_out(self.beam_list)
        self.secondary_weapon.swap_out(self.beam_list)
        self.primary_weapon = self.weapons_list[self.weapon_index](self.input.primary_fire_button, self.sprite)
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons_list):
            self.weapon_index = 0
        self.secondary_weapon = self.weapons_list[self.weapon_index](self.input.secondary_fire_button, self.sprite)


    def draw(self):
        self.projectile_list.draw()
        self.beam_list.draw()
