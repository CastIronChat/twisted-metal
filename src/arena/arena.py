from __future__ import annotations

from collections.abc import Sequence
from typing import List, cast

from arcade import SpriteList

from arena.spawn_point import SpawnPoint
from arena.wall import Wall
from path import Path
from sprite_lists import SpriteLists


class Arena:
    def __init__(self) -> None:
        self._walls: List[Wall] = []
        self._spawn_points: List[SpawnPoint] = []
        self._initial_spawn_points: List[SpawnPoint] = [None, None, None, None]
        self.patrol_loop: Path

    @property
    def walls(self) -> Sequence[Wall]:
        return self._walls

    @property
    def spawn_points(self) -> Sequence[SpawnPoint]:
        return self._spawn_points

    @property
    def initial_spawn_points(self) -> Sequence[SpawnPoint]:
        return self._initial_spawn_points

    def init_for_drawing(self, sprite_lists: SpriteLists):
        """
        One-time initialization to prepare for rendering
        """
        for wall in self.walls:
            wall.init_for_drawing()
            sprite_lists.walls.append(wall.sprite)
