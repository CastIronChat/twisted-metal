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
    primary_fire_button_held: bool

    def __init__(self, input: PlayerInput):
        self.sprite = arcade.Sprite("assets/vehicle/temp-art.png")
        self.input = input
        self.drive_speed = 100
        self.turn_speed = 100
        self.primary_fire_button_held = False
        self.sprite_added = None
        self.sprite_removed = None
        
    def update(self, delta_time: float):
        if self.input.x_axis.value < 0:
            self.sprite.angle -= delta_time * self.turn_speed
        if self.input.x_axis.value > 0:
            self.sprite.angle += delta_time * self.turn_speed
        if self.input.y_axis.value > 0:
            self.sprite.center_y += delta_time * self.drive_speed
        if self.input.y_axis.value < 0:
            self.sprite.center_y -= delta_time * self.drive_speed

        if self.input.primary_fire_button.value == True and self.primary_fire_button_held == False:
            self.shoot()
            self.primary_fire_button_held = True
        if self.input.primary_fire_button.value == False and self.primary_fire_button_held == True:
            self.sprite_removed = self.shoot_visual
            self.primary_fire_button_held = False
        
        added = self.sprite_added
        removed = self.sprite_removed
        self.sprite_added = None
        self.sprite_removed = None
        return (added,removed)
        

    def shoot(self):
        self.shoot_visual = arcade.SpriteSolidColor(1000, 10, arcade.color.RED)
        self.shoot_visual.height = 5
        self.shoot_visual.center_x = self.sprite.center_x
        self.shoot_visual.center_y = self.sprite.center_y
        self.shoot_visual.angle = self.sprite.angle
        self.sprite_added = self.shoot_visual
