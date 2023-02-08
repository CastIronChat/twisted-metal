from __future__ import annotations

from typing import Optional, cast

from arena.arena import Arena
from constants import STOCK_LIVES_PER_PLAYER
from player import Player
from player_manager import PlayerManager
from rounds.game_modes.game_mode import GameMode, GameModePlayerState
from sprite_lists import SpriteLists


class StockGameModePlayerState(GameModePlayerState):
    """
    State of a player relevant in the Stock game mode.
    """

    def __init__(self, player: Player, lives: int):
        self.lives = lives
        """
        Equals 1 when player is playing their last life.
        Decrements at the moment of death, not at the moment of respawn.
        """


def _get_state(player: Player):
    "Convenience to get a player's state with type hinting"
    return cast(StockGameModePlayerState, player.game_mode_state)


# QUESTION: how do we render "lives" on screen?
# When does HUD decrement the number of lives you have?  When the respawn timer starts?  When your car re-appears?
# For this prototype, I'm opting for Smash Bros behavior:
# When you're playing on your last life, the hud shows a single stock icon
# when you lose a life, a hud icon immediately disappears.
# Thus lives = 1 means you are currently playing your last life, and will *not* respawn after you die.


class StockGameMode(GameMode):
    _lives_per_player: int
    _winner: Optional[Player]
    "None while the round is in progress, non-None as soon as someone wins"

    def __init__(self, players: list[Player], lives_per_player=STOCK_LIVES_PER_PLAYER):
        super().__init__()
        self._lives_per_player = lives_per_player

        self.players = players

        # Store number of lives on each player
        for player in players:
            player.game_mode_state = StockGameModePlayerState(
                player, lives=self._lives_per_player
            )

    def on_round_init(
        self, players: list[Player], arena: Arena, sprite_lists: SpriteLists
    ):
        super().on_round_init(players, arena, sprite_lists)

        self._winner: Optional[Player] = None

        for player in players:
            _get_state(player).lives = self._lives_per_player

    def on_player_death(self, player: Player):
        state = _get_state(player)
        state.lives -= 1
        player.allowed_to_respawn = state.lives > 0
        # Once we have a winner, future deaths should not revoke victory.
        # E.g. maybe it's fun to kill self during victory dance.
        if self._winner is None:
            self._winner = self._check_if_we_have_a_winner()

    def _check_if_we_have_a_winner(self):
        players_with_remaining_lives: list[Player] = []
        for player in self.players:
            player_state = _get_state(player)
            if player_state.lives > 0:
                players_with_remaining_lives.append(player)
        if len(players_with_remaining_lives) == 1:
            return players_with_remaining_lives[0]
        if len(players_with_remaining_lives) == 0:
            raise Exception(
                "Everyone died at once; this is not implemented yet.  Should be declared a draw?"
            )
        return None

    def get_winner(self):
        return self._winner
