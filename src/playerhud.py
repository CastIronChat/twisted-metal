
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
    hudx: int
    hudy: int
    health_ratio: float
    playerhud_list: list = []
    player_hud_avatar: arcade.Sprite
    

    def __init__(self, player: Player, hudx: int, hudy: int, player_hud_avatar: arcade.Sprite):
        self.player = player
        self.hudx = hudx
        self.hudy = hudy
        
        self.background_sprite = arcade.SpriteSolidColor(self.width, self.height, self.background_color)
        self.background_sprite.center_x = hudx
        self.background_sprite.center_y = hudy
        
        self.player_hud_avatar = player_hud_avatar
        self.player_hud_avatar.center_x = hudx
        self.player_hud_avatar.center_y = hudy - 30
       
        self.health_sprite = arcade.SpriteSolidColor(self.width, self.height, self.full_color)
        self.health_sprite.center_x = hudx
        self.health_sprite.center_y = hudy
        
    def update(self):

        #changes healthbar length based on current ratio and left sets healthbar
        ratio = self.player.player_health / 100
        self.health_sprite.width = self.health_sprite.width * ratio
        self.health_sprite.boundary_left
        self.health_sprite.left = self.hudx - (self.health_width // 2)
        
    


    