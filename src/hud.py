import arcade

from player import Player


class Hud:

    sprite: arcade.Sprite
    sprite2: arcade.Sprite
    health: Player
    
    

    def __init__(self, health: Player):

        self.health = health.playerhealth
        self.sprite = arcade.SpriteSolidColor(80, 10, arcade.color.RED)
        self.sprite.center_x = 100
        self.sprite.center_y = 575
        
        self.sprite2 = arcade.SpriteSolidColor(80, 10, arcade.color.RED)
        self.sprite2.center_x = 700
        self.sprite2.center_y = 575
