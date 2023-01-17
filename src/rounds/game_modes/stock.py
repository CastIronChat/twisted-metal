from __future__ import annotations

from arena.arena import Arena
from player import Player
from player_manager import PlayerManager
from rounds.game_modes.game_mode import GameMode
from sprite_lists import SpriteLists


class StockModePlayerState:
    """
    State of a player relevant in the Stock game mode.
    """

    def __init__(self, lives: int):
        self.lives = lives


# QUESTION: how do we render "lives" on screen?
# When does HUD decrement the number of lives you have?  When the respawn timer starts?  When your car re-appears?
# For this prototype, I'm opting for Smash Bros behavior:
# When you're playing on your last life, the hud shows a single stock icon
# when you lose a life, a hud icon immediately disappears.
# Thus lives = 1 means you are currently playing your last life, and will *not* respawn after you die.


class StockGameMode(GameMode):
    def __init__(self, lives_per_player=3):
        super().__init__()
        self.lives_per_player = lives_per_player

    def on_round_start(
        self, players: list[Player], arena: Arena, sprite_lists: SpriteLists
    ):
        super().on_round_start(players, arena, sprite_lists)

        # Create a mapping between each player and its number of lives
        self.player_states = dict[Player, StockModePlayerState]()
        for player in players:
            self.player_states[player] = StockModePlayerState(
                lives=self.lives_per_player - 1
            )

    def on_player_death(self, player: Player):
        self.player_states[player].lives -= 1
        self.check_if_we_have_a_winner()

    def check_if_we_have_a_winner(self):
        players_with_remaining_lives = 0
        for player_state in self.player_states.values():
            if player_state.lives > 0:
                players_with_remaining_lives += 1
        return players_with_remaining_lives <= 1

    def is_allowed_to_respawn(self, player: Player):
        return self.player_states[player].lives > 0
