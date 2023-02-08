from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Protocol

from arena.arena import Arena
from sprite_lists import SpriteLists

if TYPE_CHECKING:
    from player import Player


class GameModePlayerState:
    """
    If a game mode must store player-specific information, it can subclass this
    class.  A state object can be attached to each player by the game mode.
    """


class GameMode:
    """
    Subclass GameMode to implement each mode.

    Examples: stock battle, timed battle, capture-the-flag, etc.

    Each GameMode subclass tracks whatever mode-specific stats need to be tracked, and it tells the
    game when players can no longer respawn, and when someone has won.

    To implement a gamemode, subclass this class.  Then override the methods
    that are relevant.

    Gameplay code is given a reference to the current gamemode, without knowing
    which one it is.  It will call the methods where appropriate.
    """

    def on_round_init(
        self, players: list[Player], arena: Arena, sprite_lists: SpriteLists
    ):
        """
        Called once when the round 3-2-1 timer starts, to do any setup.

        For example, in a CTF mode, this may spawn the flags.
        """
        pass

    def on_round_start(self):
        """
        Called once when the round 3-2-1 timer hits GO.
        """
        pass

    def create_hud(self):
        """
        Create a HUD object -- interface TBD -- that shows mode-specific info.
        """
        pass

    def create_player_hud(self, player: Player):
        """
        Create a HUD object for a single player -- interface TBD -- that shows
        mode-specific info about that player.
        """
        pass

    def update(self, delta_time: float):
        """
        Called once per frame for whatever update logic the mode may require.
        """
        pass

    def on_player_death(self, player: Player):
        """
        Called when a player dies, since game modes may use this info to decide
        who wins.
        """
        pass

    def get_winner(self) -> Optional[Player]:
        """
        Return a `Player` to crown a winner, `None` if game is not over yet.

        Will be called every frame by `RoundController`.
        """
        return None
