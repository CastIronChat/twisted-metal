import arcade

from player import Player


class Hud:

    sprite: arcade.Sprite
    sprite2: arcade.Sprite
    health: Player
    width: int = 80
    height: int = 4
    full_color: arcade.Color = arcade.color.GREEN
    background_color: arcade.Color = arcade.color.RED
    player1startx: int = 100
    player1starty: int = 575
    player2startx: int = 700
    player2starty: int = 575

    
    

    def __init__(self, health: Player):

        self.health = health.playerhealth
        self.sprite = arcade.SpriteSolidColor(self.width, self.height, self.background_color)
        self.sprite.center_x = self.player1startx
        self.sprite.center_y = self.player1starty
        
        self.sprite2 = arcade.SpriteSolidColor(self.width, self.height, self.background_color)
        self.sprite2.center_x = self.player2startx
        self.sprite2.center_y = self.player2starty
