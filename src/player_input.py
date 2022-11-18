"""
Responsible for interpreting raw inputs from keyboard, mouse, gamepad, whatever
into a set of "virtual" inputs that more closely match what the gameplay
requires.

In the future, will allow different players to be bound to different keys or
different gamepads, and gameplay logic won't need to be littered with
hardcoded gamepad IDs, etc.
"""

from __future__ import annotations
from tokenize import String
import arcade
from pyglet.input import Controller
from pyglet.window.key import KeyStateHandler


class PlayerInput:

    # Left stick
    x_axis: VirtualAxis
    y_axis: VirtualAxis

    # Right stick
    rx_axis: VirtualAxis
    ry_axis: VirtualAxis

    # Buttons
    accelerate_button: VirtualButton
    brake_button: VirtualButton
    primary_fire_button: VirtualButton
    secondary_fire_button: VirtualButton

    def __init__(self, keys: KeyStateHandler, controller: Controller) -> None:
        self.x_axis = VirtualAxis(keys, controller)
        self.y_axis = VirtualAxis(keys, controller)
        self.rx_axis = VirtualAxis(keys, controller)
        self.ry_axis = VirtualAxis(keys, controller)
        self.accelerate_button = VirtualButton(keys, controller)
        self.brake_button = VirtualButton(keys, controller)
        self.primary_fire_button = VirtualButton(keys, controller)
        self.secondary_fire_button = VirtualButton(keys, controller)
        self.spawn_target = VirtualButton(keys, controller)


class VirtualAxis:
    key_negative: str = None
    key_positive: str = None
    button_positive: int = None
    button_negative: int = None
    axis: str = None

    value: float

    __keys: KeyStateHandler = None
    __controller: Controller = None

    def __init__(self, keys: KeyStateHandler, controller: Controller):
        self.__keys = keys
        self.__controller = controller

    @property
    def value(self) -> float:
        neg_pressed = (
            self.key_negative != None and self.__keys[self.key_negative]
        ) or (
            self.button_negative != None
            and self.__controller
            and self.__controller.buttons[self.button_negative]
        )
        pos_pressed = (
            self.key_positive != None and self.__keys[self.key_positive]
        ) or (
            self.button_positive != None
            and self.__controller
            and self.__controller.buttons[self.button_positive]
        )
        axis_value_from_buttons = 0
        if neg_pressed and not pos_pressed:
            axis_value_from_buttons = -1
        if pos_pressed and not neg_pressed:
            axis_value_from_buttons = 1

        axis_value_from_analog = 0
        if self.__controller:
            axis_value_from_analog = getattr(self.__controller, self.axis)
        if abs(axis_value_from_analog) < 0.1:
            axis_value_from_analog = 0

        # Combine keyboard/button/stick values, and clamp
        return min(max(axis_value_from_analog + axis_value_from_buttons, -1), 1)


class VirtualButton:
    key: str = None
    button: str = None
    __keys: KeyStateHandler
    __controller: Controller

    value: bool

    def __init__(self, keys: KeyStateHandler, controller: Controller):
        self.__keys = keys
        self.__controller = controller

    @property
    def value(self) -> bool:
        key_pressed = self.key != None and self.__keys[self.key]
        button_pressed = (
            self.__controller != None
            and self.button != None
            and getattr(self.__controller, self.button)
        )
        return key_pressed or button_pressed


def set_default_controller_layout(player_input: PlayerInput):
    player_input.x_axis.axis = "leftx"
    player_input.y_axis.axis = "lefty"
    player_input.rx_axis.axis = "rightx"
    player_input.ry_axis.axis = "righty"
    player_input.accelerate_button.button = "righttrigger"
    player_input.brake_button.button = "lefttrigger"
    player_input.primary_fire_button.button = "a"
    player_input.secondary_fire_button.button = "b"


def bind_to_keyboard(player_input: PlayerInput):
    player_input.x_axis.key_negative = arcade.key.A
    player_input.x_axis.key_positive = arcade.key.D
    player_input.y_axis.key_negative = arcade.key.S
    player_input.y_axis.key_positive = arcade.key.W
    player_input.rx_axis.key_negative = arcade.key.J
    player_input.rx_axis.key_positive = arcade.key.L
    player_input.ry_axis.key_negative = arcade.key.K
    player_input.ry_axis.key_positive = arcade.key.I
    player_input.accelerate_button.key = arcade.key.UP
    player_input.brake_button.key = arcade.key.DOWN
    player_input.primary_fire_button.key = arcade.key.SPACE
    player_input.secondary_fire_button.key = arcade.key.LCTRL
    player_input.spawn_target.key = arcade.key.BACKSPACE
