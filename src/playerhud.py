
import arcade
from player import Player


class PlayerHud:
    width: int = 100
    health_width: int = 100
    height: int = 4
    background_sprite: arcade.Sprite
    health_sprite: arcade.Sprite
    full_color: arcade.Color = arcade.color.GREEN
    background_color: arcade.Color = arcade.color.RED
    player: Player
    hud_x: int
    hud_y: int
    player_hud_avatar: arcade.Sprite
    

    def __init__(self, player: Player, hud_x: int, hud_y: int, player_hud_avatar: arcade.Sprite):
        self.player = player
        self.hud_x = hud_x
        self.hud_y = hud_y
        
        self.background_sprite = arcade.SpriteSolidColor(self.width, self.height, self.background_color)
        self.background_sprite.center_x = hud_x
        self.background_sprite.center_y = hud_y
        
        self.player_hud_avatar = player_hud_avatar
        self.player_hud_avatar.center_x = hud_x
        self.player_hud_avatar.center_y = hud_y - 30
       
        self.health_sprite = arcade.SpriteSolidColor(self.width, self.height, self.full_color)
        self.health_sprite.center_x = hud_x
        self.health_sprite.center_y = hud_y
        
    def update(self):

        #changes healthbar length based on current ratio and left sets healthbar
        if self.player.player_health >= 0:
            ratio = self.player.player_health / 100
            self.health_sprite.width = self.health_width * ratio
            self.health_sprite.left = self.hud_x - (self.health_width // 2)
        
    


    