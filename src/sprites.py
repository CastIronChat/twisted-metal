import arcade
from collections.abc import Sequence


class PresentationalSprite:
    """
    Wrapper class for Sprites which appear on the screen, but do not represent objects
    which interact on screen
    """

    _sprite: arcade.Sprite

    def __init__(self, texture: any = None, scale: int = 1):
        self._sprite = arcade.Sprite(texture, scale)

    def draw(self):
        self._sprite.draw()

    @property
    def radians(self):
        return self._sprite.radians

    @property
    def arcade_sprite(self):
        return self._sprite


class InteractionalSprite(PresentationalSprite):
    """
    Wrapper class for Sprites which interact with other sprites in the arena
    """

    def __init__(self, texture: any = None, scale: int = 1):
        super(self).__init__(self, texture, scale)

    def check_for_collision_with_list(self, sprite_list: Sequence[InteractionalSprite]):
        arcade_sprite_list = [s.arcade_sprite for s in sprite_list]
        return arcade.check_for_collision_with_list(
            self.arcade_sprite, arcade_sprite_list
        )
