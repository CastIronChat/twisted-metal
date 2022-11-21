import arcade
import math

from player_input import PlayerInput
from weapon import Weapon, LaserBeam, Rocket, MachineGun
from movement_controls import MovementControls

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
    vehicle: MovementControls

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
        self.vehicle = MovementControls()

    def update(self, delta_time):
        

        self.primary_weapon.update(delta_time, self.projectile_list, self.beam_list)
        self.secondary_weapon.update(delta_time, self.projectile_list, self.beam_list)
        if self.input.swap_weapons_button.pressed:
            self.swap_weapons()

        # The vehicle updates its intended velocity and rotation
        self.vehicle.drive_input(delta_time,self.input,self.sprite)
        # TODO: Collision and bullet logic to check if the vehicle is able to move
        self.vehicle.move(self.sprite)

    def swap_weapons(self):
        #Moves the current secondary weapon to the primary weapon slot and the next weapon on the list becomes the secondary weapon
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

