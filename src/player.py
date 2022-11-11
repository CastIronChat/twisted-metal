import arcade

from player_input import PlayerInput
from weapon import Weapon, Laser, Rocket


class Player:
    # TODO seems like the arcade engine wants us to subclass Sprite for all
    # our game entities.  Seems like composition would be better?
    sprite: arcade.Sprite
    input: PlayerInput
    drive_speed: float
    turn_speed: float
    primary_weapon: Weapon
    secondary_weapon: Weapon

    def __init__(self, input: PlayerInput):
        self.sprite = arcade.Sprite("assets/vehicle/temp-art.png")
        self.input = input
        self.drive_speed = 100
        self.turn_speed = 100
        self.primary_weapon = Laser(self.input.primary_fire_button, self.sprite)
        self.secondary_weapon = Rocket(self.input.secondary_fire_button, self.sprite)

    def update(self, delta_time: float):
        if self.input.x_axis.value < 0:
            self.sprite.angle -= delta_time * self.turn_speed
        if self.input.x_axis.value > 0:
            self.sprite.angle += delta_time * self.turn_speed
        if self.input.y_axis.value > 0:
            self.sprite.center_y += delta_time * self.drive_speed
        if self.input.y_axis.value < 0:
            self.sprite.center_y -= delta_time * self.drive_speed

        (added1, removed1) = self.primary_weapon.update(delta_time)
        (added2, removed2) = self.secondary_weapon.update(delta_time)
        return (added1, removed1, added2, removed2)
