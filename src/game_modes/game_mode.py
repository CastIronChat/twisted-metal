from __future__ import annotations

from typing import Protocol

from arena.arena import Arena
from player import Player
from sprite_lists import SpriteLists


# QUESTION: rename to WinCondition?
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

    def on_round_start(
        self, players: list[Player], arena: Arena, sprite_lists: SpriteLists
    ):
        """
        Called once when the round starts to do any setup.
        TBD what this method accepts, probably references to the player manager, arena, sprite_list, hud?

        For example, in a CTF mode, this may spawn the flags.
        """
        pass

    def create_mode_specific_player_hud(self):
        pass

    def create_mode_specific_hud(self):
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

    # QUESTION: Potentially confusing: when is this called?  When the respawn happens, or immediately upon death?
    # Should be immediately upon death to prevent the respawn timer from appearing.
    # But if that's the case, should we collapse into on_player_death?  Return value of on_player_death?
    def is_player_allowed_to_respawn(self, player: Player) -> bool:
        """
        Called by the game to ask if a player is allowed to respawn anymore.
        For example, game modes may return False if this player has run out of
        lives.
        """
        return True
