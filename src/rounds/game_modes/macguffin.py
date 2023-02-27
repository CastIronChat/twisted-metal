from __future__ import annotations

from typing import Optional, cast

import arcade

from arena.arena import Arena
from constants import GAME_MODE, STOCK_LIVES_PER_PLAYER
from player import Player
from player_manager import PlayerManager
from rounds.game_modes.game_mode import GameMode, GameModePlayerState
from sprite_lists import SpriteLists
from textures import MACGUFFIN, MACGUFFINS
from iron_math import get_transformed_location, move_sprite_relative_to_parent

class MacGuffinGameModePlayerState(GameModePlayerState):

    """
    State of a player relevant to MacGuffin game mode.
    """

    def __init__(self, player: Player, lives: int):
        self.player = player
        self.lives = lives
        """
        Equals 1 when player is playing their last life.
        Decrements at the moment of death, not at the moment of respawn.
        """
        # included if we want lives in this mode. May be removed if we want unlimited lives.

        # Need to include macguffin tracking

def _get_state(player: Player):
    "Convenience to get a player's state with type hinting"
    return cast(MacGuffinGameModePlayerState, player.game_mode_state)


class MacGuffinGameMode(GameMode):
    _lives_per_player: int
    _winner: Optional[Player]
    "None while the round is in progress, non-None as soon as some wins"

    sprite_lists: SpriteLists

    def __init__(self, players: list[Player], sprite_lists: SpriteLists, lives_per_player=STOCK_LIVES_PER_PLAYER):
        super().__init__()
        self._lives_per_player = lives_per_player

        self.players = players

        # Store number of lives on each player
        for player in players:
            player.game_mode_state = MacGuffinGameModePlayerState(
                player, lives=self._lives_per_player
            )

    def on_round_init(self, arena: Arena, sprite_lists: SpriteLists):
        super().on_round_init(arena, sprite_lists)

        self.sprite_lists = sprite_lists

        # z = 0
        # while z < 5:
        #     self.macguffins = (arcade.Sprite(texture=MACGUFFINS[z], scale=2))
        #     z += 1
        #     if z == 4:
        #         z = 0
        
        self.macguffins = arcade.Sprite(texture=MACGUFFINS[2], scale=2)

        # self.macguffin = arcade.Sprite(texture=MACGUFFIN, scale=2)
        self.macguffins.center_x = 56
        self.macguffins.center_y = 56
        sprite_lists.vehicle_attachments.append(self.macguffins)
        
        self._winner: Optional[Player] = None

        for player in self.players:
            _get_state(player).lives = self._lives_per_player

    def on_round_start(self):
        pass


    def update(self, delta_time: float):

        # z = 0
        # while z < 5:
        #     self.macguffins = (arcade.Sprite(texture=MACGUFFINS[z], scale=2))
        #     z += 1
        #     if z == 4:
        #         z = 0

        macguffin_hit_list = arcade.check_for_collision_with_list(self.macguffins, self.sprite_lists.vehicles)
        
        z = 0
        for player in macguffin_hit_list:
            move_sprite_relative_to_parent(self.macguffins, player, (-15, 0, 0))
            self.macguffins.texture = MACGUFFINS[z]
            z += 1
            if z == 4:
                z = 0
        # pass


    def on_player_death(self, player: Player):
        state = player.game_mode_state
        state.lives -= 1
        player.allowed_to_respawn = state.lives > 0

    def get_winner(self) -> Optional[Player]:

        return None

