import arcade

from player import Player
from playerhud import PlayerHud


class Hud:

    sprite: arcade.Sprite
    player_hud_startx: int = 100
    player_hud_starty: int = 575
    hud_sprite_list: list = []
    player_number_tracker: int = 0
    player_huds: list[PlayerHud]
    player_hud_avatars: list[arcade.Sprite]
    
    # generates Player Huds and stores each instance in player_huds.    
    def __init__(self, playerlist):
        
        self.player_huds = []
        self.player_hud_avatars = [arcade.Sprite("assets\hud\player1avatar.png"), arcade.Sprite("assets\hud\player2avatar.png")]
        
        for player in playerlist:
            self.sprite = PlayerHud(player, self.player_hud_startx, self.player_hud_starty, self.player_hud_avatars[self.player_number_tracker])
            self.player_huds.append(self.sprite) 
            
            self.hud_sprite_list.append(self.sprite.background_sprite)
            self.hud_sprite_list.append(self.sprite.health_sprite)
            self.hud_sprite_list.append(self.sprite.player_hud_avatar)
            
            self.player_hud_startx += 150
            self.player_number_tracker += 1
            


    def update(self):

         for player_hud in self.player_huds:
            
            player_hud.update()

            
