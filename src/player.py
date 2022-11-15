import arcade

from player_input import PlayerInput
from weapon import Weapon, Beam, Rocket, MachineGun


class Player:
    # TODO seems like the arcade engine wants us to subclass Sprite for all
    # our game entities.  Seems like composition would be better?
    sprite: arcade.Sprite
    input: PlayerInput
    drive_speed: float
    turn_speed: float
    primary_weapon: Weapon
    secondary_weapon: Weapon
    player_health: int

    def __init__(self, input: PlayerInput):
        self.sprite = arcade.Sprite("assets/vehicle/temp-art.png")
        self.input = input
        self.drive_speed = 100
        self.turn_speed = 100
        self.primary_weapon = MachineGun(self.input.primary_fire_button, self.sprite)
        self.secondary_weapon = Rocket(self.input.secondary_fire_button, self.sprite)
        self.player_health = 100

    def update(self, delta_time):
        if self.input.x_axis.value < 0:
            self.sprite.angle -= self.turn_speed * delta_time
        if self.input.x_axis.value > 0:
            self.sprite.angle += self.turn_speed * delta_time
        if self.input.y_axis.value > 0:
            self.sprite.center_y += self.drive_speed * delta_time
        if self.input.y_axis.value < 0:
            self.sprite.center_y -= self.drive_speed * delta_time
        self.primary_weapon.update(delta_time)
        self.secondary_weapon.update(delta_time)

    def draw(self):
        self.primary_weapon.draw()
        self.secondary_weapon.draw()
