from __future__ import annotations

from typing import Optional, Tuple


class SpawnPoint:
    def __init__(
        self,
        transform: Tuple[float, float, float],
        initial_spawn_for_player: Optional[int],
    ):
        self.initial_spawn_for_player = initial_spawn_for_player
        "If an int, is the zero-indexed initial spawn point for a player.  0 == initial spawn point for player 1.  Defaults to None"
        self.transform = transform
