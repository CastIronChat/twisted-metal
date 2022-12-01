import arcade



class SpriteLists:
    """
    Structure that contains SpriteLists
    """

    player_sprite_list: arcade.SpriteList
    projectile_sprite_list: arcade.SpriteList
    beam_sprite_list: arcade.SpriteList
    wall_sprite_list: arcade.SpriteList

    def __init__(self):
        self.player_sprite_list = arcade.SpriteList()
        self.projectile_sprite_list = arcade.SpriteList()
        self.beam_sprite_list = arcade.SpriteList()
        self.wall_sprite_list = arcade.SpriteList()

    def draw(self):
        self.player_sprite_list.draw()
        self.projectile_sprite_list.draw()
        self.beam_sprite_list.draw()



