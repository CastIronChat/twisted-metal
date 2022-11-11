import arcade

from player_input import PlayerInput
from weapon import Laser


class Player:
    # TODO seems like the arcade engine wants us to subclass Sprite for all
    # our game entities.  Seems like composition would be better?
    sprite: arcade.Sprite
    input: PlayerInput
    drive_speed: float
    turn_speed: float
    primary_weapon: Laser

    def __init__(self, input: PlayerInput):
        self.sprite = arcade.Sprite("assets/vehicle/temp-art.png")
        self.input = input
        self.drive_speed = 100
        self.turn_speed = 100
        self.primary_weapon = Laser(self.input, self.sprite)
        
    def update(self, delta_time: float):
        if self.input.x_axis.value < 0:
            self.sprite.angle -= delta_time * self.turn_speed
        if self.input.x_axis.value > 0:
            self.sprite.angle += delta_time * self.turn_speed
        if self.input.y_axis.value > 0:
            self.sprite.center_y += delta_time * self.drive_speed
        if self.input.y_axis.value < 0:
            self.sprite.center_y -= delta_time * self.drive_speed

        (added,removed) = self.primary_weapon.update(delta_time)
        return (added,removed)
