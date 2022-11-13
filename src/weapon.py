import arcade
import math

from player_input import VirtualButton


class Weapon:
    """
    Slotted into player's car and behaves according to it's subclass weapon type
    """

    input_button: VirtualButton
    car: arcade.Sprite
    shoot_visual: arcade.Sprite
    bullet_list: arcade.SpriteList
    shooting: bool
    sprite_added: arcade.Sprite
    sprite_removed: arcade.Sprite

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        self.input_button = input_button
        self.car = car
        self.shooting = False
        self.sprite_added = None
        self.sprite_removed = None

    def update(self, delta_time: float):
        ...

    def send_to_spritelist(self):
        added = self.sprite_added
        removed = self.sprite_removed
        self.sprite_added = None
        self.sprite_removed = None
        return (added, removed)


class Beam(Weapon):
    """
    stays on while button is pressed and moved with the ship
    """

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        super().__init__(input_button, car)
        self.shoot_visual = arcade.SpriteSolidColor(1000, 5, arcade.color.RED)

    def update(self, delta_time: float):
        if not self.shooting and self.input_button.value:
            self.shoot()
        if self.shooting:
            self.update_active_weapon()
            if not self.input_button.value:
                self.end_active_weapon()
        return super().send_to_spritelist()

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


class Rocket(Weapon):
    """
    Fires a projectile that is now independent of the ship and travels unil it reaches a designated distance
    """

    rocket_speed: float
    rocket_angle: float

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        super().__init__(input_button, car)
        self.shoot_visual = arcade.SpriteSolidColor(50, 30, arcade.color.ORANGE)
        self.rocket_speed = 200

    def update(self, delta_time: float):
        if not self.shooting and self.input_button.value:
            self.shoot()
        if self.shooting:
            self.update_active_weapon(delta_time)
            if self.shoot_visual.center_x > 500:
                self.end_active_weapon()
        return super().send_to_spritelist()

    def shoot(self):
        self.shoot_visual.center_x = self.car.center_x
        self.shoot_visual.center_y = self.car.center_y
        self.shoot_visual.angle = self.car.angle
        self.rocket_angle = math.radians(self.car.angle)
        self.shooting = True
        self.sprite_added = self.shoot_visual

    def update_active_weapon(self, delta_time: float):
        self.shoot_visual.center_x += (
            delta_time * self.rocket_speed * math.cos(self.rocket_angle)
        )
        self.shoot_visual.center_y += (
            delta_time * self.rocket_speed * math.sin(self.rocket_angle)
        )

    def end_active_weapon(self):
        self.sprite_removed = self.shoot_visual
        self.shooting = False


class MachineGun(Weapon):
    """
    Fires a projectile that is now independent of the ship and travels unil it reaches a designated distance
    """

    bullet_speed: float

    def __init__(self, input_button: VirtualButton, car: arcade.Sprite):
        super().__init__(input_button, car)
        self.bullet_speed = 300
        self.bullet_list = arcade.SpriteList()

    def update(self, delta_time: float):
        if not self.shooting and self.input_button.value:
            self.shoot(delta_time)
        if self.shooting and not self.input_button.value:
            self.shooting = False

        return super().send_to_spritelist()

    def shoot(self, delta_time: float):
        bullet = arcade.SpriteSolidColor(10, 5, arcade.color.RED)
        bullet.center_x = self.car.center_x
        bullet.center_y = self.car.center_y
        bullet.angle = self.car.angle
        bullet_angle = math.radians(self.car.angle)
        bullet.change_x = delta_time * self.bullet_speed * math.cos(bullet_angle)
        bullet.change_y = delta_time * self.bullet_speed * math.sin(bullet_angle)
        self.shooting = True
        self.bullet_list.append(bullet)
