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
import pyglet
from pyglet.input import Joystick
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

    __controller: Joystick
    # __handlers: ControllerHandlers

    def __init__(self, keys: KeyStateHandler) -> None:
        self.x_axis = VirtualAxis(keys)
        self.y_axis = VirtualAxis(keys)
        self.rx_axis = VirtualAxis(keys)
        self.ry_axis = VirtualAxis(keys)
        self.accelerate_button = VirtualButton(keys)
        self.brake_button = VirtualButton(keys)
        self.primary_fire_button = VirtualButton(keys)
        self.secondary_fire_button = VirtualButton(keys)

    # TODO unclear on best API here, going with numbers 1 through 4 for now
    # matches XBox / XInput player 1-4
    def bind_to_controller(self, controller_num: int):
        controllers = pyglet.input.get_controllers()
        controller = controllers[controller_num - 1]
        controller.open()
        self.__controller = controller


#         self.__handlers = ControllerHandlers(self)
#         self.__controller.push_handlers(self.__handlers)


# class ControllerHandlers:
#     __input: PlayerInput

#     def __init__(self, player_input: PlayerInput):
#         self.__input = player_input

#     def on_joybutton_press(self, joystick: Joystick, button: int):
#         print(button)


class VirtualAxis:
    key_negative: String = None
    key_positive: String = None
    button_positive: int = None
    button_negative: int = None
    __axis: int = None

    value: float

    __keys: KeyStateHandler = None
    __controller: Joystick = None
    __controller_axis_control: Any

    def __init__(self, keys: KeyStateHandler):
        self.__keys = keys

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
        if neg_pressed and pos_pressed:
            return 0
        if neg_pressed:
            return -1
        if pos_pressed:
            return 1
        return 0


class VirtualButton:
    key: String = None
    __button: int = None
    __keys: KeyStateHandler

    value: bool

    def __init__(self, keys: KeyStateHandler):
        self.__keys = keys

    @property
    def value(self) -> bool:
        key_pressed = self.key != None and self.__keys[self.key]
        button_pressed = False
        return key_pressed or button_pressed

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
    player_input.secondary_fire_button.key = arcade.key.MOD_CTRL
