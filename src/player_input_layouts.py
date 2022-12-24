from __future__ import annotations

import arcade

from player_input import PlayerInput


def set_controller_layout(player_input: PlayerInput, alternate: bool):
    if alternate:
        set_alternate_controller_layout(player_input)
    else:
        set_default_controller_layout(player_input)


def _set_common_controller_layout(player_input: PlayerInput):
    # A few controls must be reset when switching between layouts
    player_input.accelerate_axis.button_positive = None
    player_input.brake_axis.button_positive = None
    player_input.accelerate_axis.axis = None
    player_input.brake_axis.axis = None

    # These bindings are common to both layouts
    player_input.x_axis.axis = "leftx"
    player_input.y_axis.axis = "lefty"
    player_input.rx_axis.axis = "rightx"
    player_input.ry_axis.axis = "righty"
    player_input.swap_weapons_button.button = "y"
    player_input.reload_button.button = "x"
    player_input.debug_1.button = "dpup"
    player_input.debug_2.button = "dpdown"
    player_input.debug_3.button = "dpleft"
    player_input.debug_4.button = "dpright"


def set_default_controller_layout(player_input: PlayerInput):
    player_input.layout_name = "Default"
    _set_common_controller_layout(player_input)
    # Drive with triggers
    player_input.accelerate_axis.axis = "righttrigger"
    player_input.brake_axis.axis = "lefttrigger"
    # Shoot with A/B
    player_input.primary_fire_button.button = "a"
    player_input.secondary_fire_button.button = "b"


def set_alternate_controller_layout(player_input: PlayerInput):
    player_input.layout_name = "Alternate"
    _set_common_controller_layout(player_input)
    # Drive with A/B
    player_input.accelerate_axis.button_positive = "a"
    player_input.brake_axis.button_positive = "b"
    # Shoot with triggers
    player_input.primary_fire_button.button = "righttrigger"
    player_input.secondary_fire_button.button = "lefttrigger"


def bind_to_keyboard(player_input: PlayerInput):
    player_input.x_axis.key_negative = arcade.key.A
    player_input.x_axis.key_positive = arcade.key.D
    player_input.y_axis.key_negative = arcade.key.DOWN
    player_input.y_axis.key_positive = arcade.key.UP
    player_input.rx_axis.key_negative = arcade.key.J
    player_input.rx_axis.key_positive = arcade.key.L
    player_input.ry_axis.key_negative = arcade.key.K
    player_input.ry_axis.key_positive = arcade.key.I
    player_input.accelerate_axis.key_positive = arcade.key.W
    player_input.brake_axis.key_positive = arcade.key.S
    player_input.primary_fire_button.key = arcade.key.SPACE
    player_input.secondary_fire_button.key = arcade.key.LCTRL
    player_input.swap_weapons_button.key = arcade.key.Q
    player_input.reload_button.key = arcade.key.R
    player_input.debug_1.key = arcade.key.KEY_1
    player_input.debug_2.key = arcade.key.KEY_2
    player_input.debug_3.key = arcade.key.KEY_3
    player_input.debug_4.key = arcade.key.KEY_4
