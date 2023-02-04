
from typing import TYPE_CHECKING, Optional

from arena.arena import Arena
from sprite_lists import SpriteLists
from rounds.game_modes.game_mode import GameMode
from player import Player
# from player_manager import PlayerManager

if TYPE_CHECKING:
    from player import Player


class EmptyGameMode(GameMode):


    def __init__(self, players: list[Player]):
        super().__init__()
        self.players = players



    def on_round_init(self, players: list[Player], arena: Arena, sprite_lists: SpriteLists):
        pass



    def on_round_start(self):
        pass

    def create_hud(self):
        pass

    def create_player_hud(self, player: Player):
        pass

    def update(self, delta_time: float):
        pass

    def on_player_death(self, player: Player):
        pass

    def get_winner(self) -> Optional[Player]:

        return None