import arcade
from player_input import VirtualButton
import weapon
import random

class Target:

    def __init__(self, input_button: VirtualButton):

        self.target_list = arcade.SpriteList()
        self.input_button = input_button
        self.button_held = False
        
    def update(self, delta_time):
        if not self.button_held and self.input_button.value:
            self.button_held = True
            self.spawn_target()
        if self.button_held and not self.input_button.value:
            self.button_held = False
        self.target_hit_detection_action

    def spawn_target(self):
        self.target_sprite = arcade.Sprite("assets/targets/target1.png")
        self.target_sprite.center_x = random.randint(1, 800)
        self.target_sprite.center_y = random.randint(1, 600)
        self.target_list.append(self.target_sprite)

    def target_hit_detection_action(self):
        
        


    def draw(self):
        self.target_list.draw()



        
