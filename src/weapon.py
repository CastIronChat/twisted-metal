import arcade
import math
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
            self.update_active_weapon()
        if self.shooting == True and self.input.primary_fire_button.value == False:
            self.end_active_weapon()

        added = self.sprite_added
        removed = self.sprite_removed
        self.sprite_added = None
        self.sprite_removed = None
        return (added,removed)

    def shoot(self):
        self.shooting = True
        self.sprite_added = self.shoot_visual

    def update_active_weapon(self):
        self.shoot_visual.center_x = self.car.center_x
        self.shoot_visual.center_y = self.car.center_y
        self.shoot_visual.angle = self.car.angle

    def end_active_weapon(self):
        self.sprite_removed = self.shoot_visual
        self.shooting = False

class Rocket:
    input: PlayerInput
    car: arcade.Sprite
    shoot_visual: arcade.Sprite
    shooting: bool
    rocket_speed: float
    rocket_angle: float

    def __init__(self, input: PlayerInput, car: arcade.Sprite):
        self.input = input
        self.car = car
        self.shoot_visual = arcade.SpriteSolidColor(50, 30, arcade.color.ORANGE)
        self.shooting = False
        self.rocket_speed = 200
        self.sprite_added = None
        self.sprite_removed = None

    def update(self, delta_time: float):
        if self.shooting == False and self.input.secondary_fire_button.value == True:
            self.shoot()
        if self.shooting == True:
            self.update_active_weapon(delta_time)
            if self.shoot_visual.center_x > 500:
                self.end_active_weapon()

        added = self.sprite_added
        removed = self.sprite_removed
        self.sprite_added = None
        self.sprite_removed = None
        return (added,removed)

    def shoot(self):
        self.shoot_visual.center_x = self.car.center_x
        self.shoot_visual.center_y = self.car.center_y
        self.shoot_visual.angle = self.car.angle
        self.rocket_angle = math.radians(self.car.angle)
        self.shooting = True
        self.sprite_added = self.shoot_visual

    def update_active_weapon(self, delta_time: float):
        self.shoot_visual.center_x += delta_time * self.rocket_speed * math.cos(self.rocket_angle)
        self.shoot_visual.center_y += delta_time * self.rocket_speed * math.sin(self.rocket_angle)

    def end_active_weapon(self):
        self.sprite_removed = self.shoot_visual
        self.shooting = False