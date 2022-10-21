import arcade

from player_input import PlayerInput


class Player:
    # TODO seems like the arcade engine wants us to subclass Sprite for all
    # our game entities.  Seems like composition would be better?
    sprite: arcade.Sprite
    input: PlayerInput
    drive_speed: float
    turn_speed: float

    def __init__(self, input: PlayerInput):
        self.sprite = arcade.Sprite("assets/vehicle/temp-art.png")
        self.input = input
        self.drive_speed = 100
        self.turn_speed = 100

    def update(self, delta_time: float):
        if self.input.left:
            self.sprite.angle -= delta_time * self.turn_speed
        if self.input.right:
            self.sprite.angle += delta_time * self.turn_speed
        if self.input.up:
            self.sprite.center_y += delta_time * self.drive_speed
        if self.input.down:
            self.sprite.center_y -= delta_time * self.drive_speed
