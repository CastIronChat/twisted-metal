from arcade import Sprite, SpriteSolidColor, color


class Wall:
    def __init__(self, x: int, y: int, width: int, height: int, angle=0.0) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._angle = angle
        self._sprite: Sprite
        self.init_for_drawing()

    @property
    def sprite(self):
        return self._sprite

    def init_for_drawing(self):
        """
        call once all other attributes are set, to initialize graphical
        representation
        """
        self._sprite = SpriteSolidColor(self._width, self._height, color.BLACK)
        self._sprite.set_position(self._x, self._y)
        self._sprite.radians = self._angle
