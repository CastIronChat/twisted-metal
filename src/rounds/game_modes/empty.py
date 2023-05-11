from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from arena.arena import Arena
from player import Player
from rounds.game_modes.game_mode import GameMode
from sprite_lists import SpriteLists

if TYPE_CHECKING:
    from player import Player


class EmptyGameModePlayerState:
    def __init__(self, player: Player, lives: int):
        self.lives = lives
        # self.player = player


class EmptyGameMode(GameMode):
    def __init__(self, players: list[Player]):
        super().__init__()
        self.players = players

        for player in players:
            player.game_mode_state = EmptyGameModePlayerState(player, lives=1)

    def on_round_init(self, arena: Arena, sprite_lists: SpriteLists):

        super().on_round_init(arena, sprite_lists)

    def on_round_start(self):
        pass

    def update(self, delta_time: float):
        pass

    # def on_player_death(self, player: Player):
    #     state = player.game_mode_state
    #     state.lives = 1
    #     player.allowed_to_respawn = state.lives > 0
