import arcade
from player_input import PlayerInput

class Laser:
    input: PlayerInput
    car: arcade.Sprite
    shoot_visual: arcade.Sprite
    shooting: bool

    def __init__(self, input: PlayerInput, car: arcade.Sprite):
        self.input = input
        self.car = car
        self.shoot_visual = arcade.SpriteSolidColor(1000, 5, arcade.color.RED)
        self.shooting = False
        self.sprite_added = None
        self.sprite_removed = None

    def update(self, delta_time: float):
        if self.shooting == False and self.input.primary_fire_button.value == True:
            self.shoot()
        if self.shooting == True:
            self.shoot_visual.center_x = self.car.center_x
            self.shoot_visual.center_y = self.car.center_y
            self.shoot_visual.angle = self.car.angle
        if self.shooting == True and self.input.primary_fire_button.value == False:
            self.sprite_removed = self.shoot_visual
            self.shooting = False

        added = self.sprite_added
        removed = self.sprite_removed
        self.sprite_added = None
        self.sprite_removed = None
        return (added,removed)

    def shoot(self):
        self.shooting = True
        self.sprite_added = self.shoot_visual