from __future__ import annotations

import math

from arena.arena import Arena
from constants import PLAYER_ON_PATROL_LOOP
from iron_math import add_vec, scale_vec, subtract_vec
from player_manager import PlayerManager


class DebugPatrolLoop:
    def __init__(self, player_manager: PlayerManager, arena: Arena):
        self.player_manager = player_manager
        self.arena = arena
        self.patrol_timer = 0.0

    def update(self, delta_time: float):
        # skip if not enabled
        if PLAYER_ON_PATROL_LOOP is None:
            return
        self.patrol_timer += delta_time
        if self.patrol_timer >= self.arena._patrol_loop.max_time:
            self.patrol_timer = self.arena._patrol_loop.min_time
        player = self.player_manager.players[PLAYER_ON_PATROL_LOOP]
        position = self.arena._patrol_loop.sample(self.patrol_timer)
        position_soon = self.arena._patrol_loop.sample(self.patrol_timer + 0.2)
        heading_vec = subtract_vec(position_soon, position)
        heading_radians = math.atan2(heading_vec[1], heading_vec[0])
        player.location = (position[0], position[1], heading_radians)
