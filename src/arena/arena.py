from typing import List, cast
from collections.abc import Sequence

from arcade import SpriteList
from arena.spawn_point import SpawnPoint

from arena.wall import Wall


class Arena:
    def __init__(self) -> None:
        self._walls: List[Wall] = []
        self._sprite_list: SpriteList
        self._spawn_points: List[SpawnPoint] = []
        self._initial_spawn_points: List[SpawnPoint] = [None, None, None, None]

    @property
    def walls(self) -> Sequence[Wall]:
        return self._walls

    @property
    def wall_sprite_list(self) -> SpriteList:
        return self._sprite_list

    @property
    def spawn_points(self) -> Sequence[SpawnPoint]:
        return self._spawn_points

    @property
    def initial_spawn_points(self) -> Sequence[SpawnPoint]:
        return self._initial_spawn_points

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
