import arcade

from player_input import PlayerInput


class Player:
    # TODO seems like the arcade engine wants us to subclass Sprite for all
    # our game entities.  Seems like composition would be better?
    sprite: arcade.Sprite
    shoot_visual: arcade.Sprite
    input: PlayerInput
    drive_speed: float
    turn_speed: float

    def __init__(self, input: PlayerInput):
        self.sprite = arcade.Sprite("assets/vehicle/temp-art.png")
        self.shoot_visual = arcade.SpriteSolidColor(1000, 1, arcade.color.RED)
        self.input = input
        self.drive_speed = 100
        self.turn_speed = 100
        
    def update(self, delta_time: float):
        if self.input.x_axis.value < 0:
            self.sprite.angle -= delta_time * self.turn_speed
        if self.input.x_axis.value > 0:
            self.sprite.angle += delta_time * self.turn_speed
        if self.input.y_axis.value > 0:
            self.sprite.center_y += delta_time * self.drive_speed
        if self.input.y_axis.value < 0:
            self.sprite.center_y -= delta_time * self.drive_speed
        if self.input.primary_fire_button.value == True:
            self.shoot()

    def shoot(self):
        self.shoot_visual.height = 5
        self.shoot_visual.center_x = self.sprite.center_x
        self.shoot_visual.center_y = self.sprite.center_y
        self.shoot_visual.angle = self.sprite.angle