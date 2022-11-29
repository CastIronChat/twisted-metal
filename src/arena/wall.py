from arcade import SpriteSolidColor, color


class Wall:
    def __init__(self, x: int, y: int, width: int, height: int, angle=0.0) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._angle = angle
        self._sprite: SpriteForWall
        self.init_for_drawing()

    @property
    def sprite(self):
        return self._sprite

    def init_for_drawing(self):
        """
        call once all other attributes are set, to initialize graphical
        representation
        """

        self._sprite = SpriteForWall(self._width, self._height, color.BLACK)
        self._sprite.wall = self

        self._sprite.set_position(self._x, self._y)
        self._sprite.radians = self._angle


class SpriteForWall(SpriteSolidColor):
    wall: Wall
