from typing import Tuple
from arcade import color
from iron_math import set_sprite_location

from linked_sprite import LinkedSprite, LinkedSpriteSolidColor


class Wall:
    def __init__(
        self, transform: Tuple[float, float, float], size: Tuple[float, float]
    ) -> None:
        self._transform = transform
        self._size = size
        self._sprite: LinkedSprite[Wall]
        self.init_for_drawing()

    @property
    def sprite(self):
        return self._sprite

    def init_for_drawing(self):
        """
        call once all other attributes are set, to initialize graphical
        representation
        """

        self._sprite = LinkedSpriteSolidColor[Wall](
            int(self._size[0]), int(self._size[1]), color.BLACK
        )
        self._sprite.owner = self

        set_sprite_location(self._sprite, self._transform)
