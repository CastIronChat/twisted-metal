from typing import List, cast
from collections.abc import Sequence

from arcade import SpriteList

from arena.wall import Wall


class Arena:
    def __init__(self) -> None:
        self._walls: List[Wall] = []
        self._sprite_list: SpriteList

    @property
    def walls(self) -> Sequence[Wall]:
        return self._walls

    def init_for_drawing(self):
        """
        One-time initialization to prepare for rendering
        """
        self._sprite_list = SpriteList()
        for wall in self.walls:
            wall.init_for_drawing()
            self._sprite_list.append(wall.sprite)

    def draw(self):
        self._sprite_list.draw()