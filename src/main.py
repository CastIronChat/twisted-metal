from __future__ import annotations

import arcade

from arena.arena import Arena
from arena.arena_loader import load_arena_by_name
from collision import projectile_hits_player, projectile_hits_wall
from constants import (
    ARENA,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    TICK_DURATION,
    USE_DEBUGGER_TIMING_FIXES,
)
from fullscreen import FullscreenController
from global_input import GlobalInput, bind_global_inputs_to_keyboard
from hud import Hud
from input_debug_hud import DebugHud
from player_manager import PlayerManager
from projectile import update_projectiles
from sprite_lists import SpriteLists


class MyGame(arcade.Window):
    # Declare class members; enables tab-completion
    input_debug_hud: DebugHud = None
    sprite_lists: SpriteLists

    def __init__(self, width: int, height: int, title: str):
        super().__init__(
            width, height, title, enable_polling=True, update_rate=TICK_DURATION
        )
        self.physics_engine = None
        arcade.set_background_color(arcade.color.AMAZON)
        self.player_manager = PlayerManager(self.keyboard)
        self.global_input = GlobalInput(self.keyboard, None)
        bind_global_inputs_to_keyboard(self.global_input)
        self.sprite_lists = SpriteLists()
        self.arena: Arena
        self.fullscreen_controller = FullscreenController(self, self.global_input)

    def setup(self):
        self.projectile_sprite_list = arcade.SpriteList()

        # Arena
        self.arena = load_arena_by_name(ARENA)
        self.arena.init_for_drawing(self.sprite_lists)

        # Players
        self.player_manager.setup(
            self.sprite_lists,
            self.arena,
        )

        # Debug UI for input handling
        self.input_debug_hud = DebugHud(self.player_manager.players)

        # Player Huds
        self.hud = Hud(self.player_manager.players, self.sprite_lists)
        self.patrol_timer = 0.0

    def on_update(self, delta_time):
        # Arcade engine has a quirk where, in the debugger, it calls `on_update` twice back-to-back,
        # then `on_draw` twice, and so on.
        # We avoid this bug by ignoring the `on_update()` call from arcade, instead calling it ourselves
        # from `on_draw`
        if not USE_DEBUGGER_TIMING_FIXES:
            self.our_update(delta_time)

    def our_update(self, delta_time: float):
        # Pretty sure this does animation updates, in case any of the sprites
        # Have animations
        self.global_input.update()
        self.fullscreen_controller.update()
        self.player_manager.update_inputs()
        for player in self.player_manager.players:
            player.update(delta_time)
        update_projectiles(
            delta_time,
            self.sprite_lists,
        )
        projectile_hits_wall(self.sprite_lists)
        projectile_hits_player(delta_time, self.sprite_lists)
        self.patrol_timer += delta_time
        if self.patrol_timer >= self.arena._patrol_loop.max_time:
            self.patrol_timer = self.arena._patrol_loop.min_time
        self.player_manager.players[1].sprite.position = self.arena._patrol_loop.sample(
            self.patrol_timer
        )
        self.hud.update()

    def on_draw(self):
        if USE_DEBUGGER_TIMING_FIXES:
            self.our_update(TICK_DURATION)

        # clear screen
        self.clear()
        self.sprite_lists.draw()
        for player in self.player_manager.players:
            player.draw()
        self.input_debug_hud.draw()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
