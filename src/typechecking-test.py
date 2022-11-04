import arcade


class Foo(arcade.Window):
    sprite: arcade.Sprite
    sprite_list: arcade.SpriteList

    def __init__(self):
        super().__init__()
        self.sprite = arcade.Sprite()
        self.sprite_list = arcade.SpriteList()

    def foo(self):
        self.sprite.drawwww()  # Good; we get a typechecking error
        self.sprite_list.drawwww()  # Bad; we do not get a typechecking error
