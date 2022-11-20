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
from typing import Optional
import arcade
from pyglet.input import Controller
from pyglet.window.key import KeyStateHandler


class PlayerInput:
    def __init__(self, keys: KeyStateHandler, controller: Controller) -> None:
        # Left stick
        self.x_axis = VirtualAxis(keys, controller)
        self.y_axis = VirtualAxis(keys, controller)

        # Right stick
        self.rx_axis = VirtualAxis(keys, controller)
        self.ry_axis = VirtualAxis(keys, controller)

        # Accelerate/brake
        self.accelerate_axis = VirtualAxis(keys, controller)
        self.brake_axis = VirtualAxis(keys, controller)

        # Buttons
        self.primary_fire_button = VirtualButton(keys, controller)
        self.secondary_fire_button = VirtualButton(keys, controller)
        self.swap_weapons_button = VirtualButton(keys, controller)
        self.reload_button = VirtualButton(keys, controller)

    def update(self):
        self.primary_fire_button._update()
        self.secondary_fire_button._update()
        self.swap_weapons_button._update()
        self.reload_button._update()


class VirtualAxis:
    __keys: KeyStateHandler = None
    __controller: Controller = None

    def __init__(self, keys: KeyStateHandler, controller: Controller):
        self.__keys = keys
        self.__controller = controller

        self.key_negative: Optional[str] = None
        self.key_positive: Optional[str] = None
        self.button_positive: Optional[int] = None
        self.button_negative: Optional[int] = None
        self.axis: Optional[str] = None

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
    def __init__(self, keys: KeyStateHandler, controller: Controller):
        self.__keys = keys
        self.__controller = controller
        self.key: Optional[str] = None
        self.button: Optional[str] = None
        self._value: bool = False
        self._value_last_frame: bool = False
        self._pressed: bool
        self._released: bool

    @property
    def value(self):
        return self._value

    @property
    def pressed(self):
        """
        True of the button was pressed on this frame, meaning it is held now but was not last frame.
        """
        return self._pressed

    @property
    def released(self):
        """
        True of the button was released on this frame, meaning it was held last frame but is not any more.
        """
        return self._released

    def _get_value(self) -> bool:
        key_pressed = self.key != None and self.__keys[self.key]
        button_pressed = (
            self.__controller != None
            and self.button != None
            and getattr(self.__controller, self.button)
        )
        return key_pressed or button_pressed

    def _update(self):
        value_last_frame = self._value_last_frame = self._value
        value_this_frame = self._value = self._get_value()
        self._pressed = False
        self._released = False
        if value_this_frame and not value_last_frame:
            self._pressed = True
        if not value_this_frame and value_last_frame:
            self._released = True


def set_default_controller_layout(player_input: PlayerInput):
    player_input.x_axis.axis = "leftx"
    player_input.y_axis.axis = "lefty"
    player_input.rx_axis.axis = "rightx"
    player_input.ry_axis.axis = "righty"
    player_input.accelerate_axis.axis = "righttrigger"
    player_input.brake_axis.axis = "lefttrigger"
    player_input.primary_fire_button.button = "a"
    player_input.secondary_fire_button.button = "b"
    player_input.swap_weapons_button.button = "y"
    player_input.reload_button.button = "x"


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
