"""
Responsible for interpreting raw inputs from keyboard, mouse, gamepad, whatever
into a set of "virtual" inputs that more closely match what the gameplay
requires.

In the future, will allow different players to be bound to different keys or
different gamepads, and gameplay logic won't need to be littered with
hardcoded gamepad IDs, etc.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

# The server imports this file but does not have pyglet
if TYPE_CHECKING:
    from pyglet.input import Controller
    from pyglet.window.key import KeyStateHandler

from constants import FRAMES_OF_INPUT_DELAY


class PlayerInput:
    def __init__(self, keys: KeyStateHandler, controller: Controller) -> None:
        self.layout_name = ""
        "Name of current control scheme, for diagnostic purposes"

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

        # Debugging
        self.debug_1 = VirtualButton(keys, controller)
        self.debug_2 = VirtualButton(keys, controller)
        self.debug_3 = VirtualButton(keys, controller)
        self.debug_4 = VirtualButton(keys, controller)

    def update(self):
        self.x_axis._update()
        self.y_axis._update()
        self.rx_axis._update()
        self.ry_axis._update()
        self.accelerate_axis._update()
        self.brake_axis._update()
        self.primary_fire_button._update()
        self.secondary_fire_button._update()
        self.swap_weapons_button._update()
        self.reload_button._update()
        self.debug_1._update()
        self.debug_2._update()
        self.debug_3._update()
        self.debug_4._update()

    def update_from_snapshot(self, snapshot: PlayerInputSnapshot):
        self.x_axis._update_from_snapshot(snapshot.x_axis)
        self.y_axis._update_from_snapshot(snapshot.y_axis)
        self.rx_axis._update_from_snapshot(snapshot.rx_axis)
        self.ry_axis._update_from_snapshot(snapshot.ry_axis)
        self.accelerate_axis._update_from_snapshot(snapshot.accelerate_axis)
        self.brake_axis._update_from_snapshot(snapshot.brake_axis)
        self.primary_fire_button._update_from_snapshot(snapshot.primary_fire_button)
        self.secondary_fire_button._update_from_snapshot(snapshot.secondary_fire_button)
        self.swap_weapons_button._update_from_snapshot(snapshot.swap_weapons_button)
        self.reload_button._update_from_snapshot(snapshot.reload_button)
        self.debug_1._update_from_snapshot(snapshot.debug_1)
        self.debug_2._update_from_snapshot(snapshot.debug_2)
        self.debug_3._update_from_snapshot(snapshot.debug_3)
        self.debug_4._update_from_snapshot(snapshot.debug_4)

    def capture_physical_inputs(self):
        snapshot = PlayerInputSnapshot()
        snapshot.x_axis = self.x_axis._read_physical_input()
        snapshot.y_axis = self.y_axis._read_physical_input()
        snapshot.rx_axis = self.rx_axis._read_physical_input()
        snapshot.ry_axis = self.ry_axis._read_physical_input()
        snapshot.accelerate_axis = self.accelerate_axis._read_physical_input()
        snapshot.brake_axis = self.brake_axis._read_physical_input()
        snapshot.primary_fire_button = self.primary_fire_button._read_physical_input()
        snapshot.secondary_fire_button = (
            self.secondary_fire_button._read_physical_input()
        )
        snapshot.swap_weapons_button = self.swap_weapons_button._read_physical_input()
        snapshot.reload_button = self.reload_button._read_physical_input()
        snapshot.debug_1 = self.debug_1._read_physical_input()
        snapshot.debug_2 = self.debug_2._read_physical_input()
        snapshot.debug_3 = self.debug_3._read_physical_input()
        snapshot.debug_4 = self.debug_4._read_physical_input()
        return snapshot


class PlayerInputSnapshot:
    def __init__(self):
        # Left stick
        self.x_axis = 0.0
        self.y_axis = 0.0

        # Right stick
        self.rx_axis = 0.0
        self.ry_axis = 0.0

        # Accelerate/brake
        self.accelerate_axis = 0.0
        self.brake_axis = 0.0

        # Buttons
        self.primary_fire_button = False
        self.secondary_fire_button = False
        self.swap_weapons_button = False
        self.reload_button = False

        # Debugging
        self.debug_1 = False
        self.debug_2 = False
        self.debug_3 = False
        self.debug_4 = False


EMPTY_INPUT_SNAPSHOT = PlayerInputSnapshot()


class VirtualAxis:
    _keys: KeyStateHandler = None
    _controller: Controller = None
    _value_buffer: list[float]

    def __init__(self, keys: KeyStateHandler, controller: Controller):
        self._keys = keys
        self._controller = controller

        self.key_negative: Optional[int] = None
        self.key_positive: Optional[int] = None
        self.button_positive: Optional[int] = None
        self.button_negative: Optional[int] = None
        self.axis: Optional[str] = None

    @property
    def value(self) -> float:
        return self._value

    def _update(self):
        self._update_from_snapshot(self, self._read_physical_input())

    def _update_from_snapshot(self, new_value: float):
        self._value = new_value

    def _read_physical_input(self):
        neg_pressed = (
            self.key_negative is not None and self._keys[self.key_negative]
        ) or (
            self.button_negative is not None
            and self._controller
            and getattr(self._controller, self.button_negative)
        )
        pos_pressed = (
            self.key_positive is not None and self._keys[self.key_positive]
        ) or (
            self.button_positive is not None
            and self._controller
            and getattr(self._controller, self.button_positive)
        )
        axis_value_from_buttons = 0
        if neg_pressed and not pos_pressed:
            axis_value_from_buttons = -1
        if pos_pressed and not neg_pressed:
            axis_value_from_buttons = 1

        axis_value_from_analog = 0
        if self._controller and self.axis is not None:
            axis_value_from_analog = getattr(self._controller, self.axis)
        if abs(axis_value_from_analog) < 0.1:
            axis_value_from_analog = 0

        # Combine keyboard/button/stick values, and clamp
        return min(max(axis_value_from_analog + axis_value_from_buttons, -1), 1)


class VirtualButton:
    def __init__(self, keys: KeyStateHandler, controller: Controller):
        self._keys = keys
        self._controller = controller
        self.key: Optional[int] = None
        self.button: Optional[str] = None
        self._value: bool = False
        self._value_last_frame: bool = False
        self._pressed: bool
        self._released: bool
        self.toggle: bool = False
        """
        Every time the button is pressed, this toggles between true to false. May be useful for switching debug
        features on and off; should probably not be used for gameplay.

        Debug logic is permitted to write to this value, in case it makes sense to reset it.
        """

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

    def _read_physical_input(self) -> bool:
        key_pressed = self.key is not None and self._keys[self.key]
        button_pressed = (
            self._controller is not None
            and self.button is not None
            and getattr(self._controller, self.button)
        )
        return key_pressed or button_pressed

    def _update(self):
        self._update_from_snapshot(self._read_physical_input())

    def _update_from_snapshot(self, new_value: bool):
        value_last_frame = self._value_last_frame = self._value
        value_this_frame = self._value = new_value
        self._pressed = False
        self._released = False
        if value_this_frame and not value_last_frame:
            self._pressed = True
            self.toggle = not self.toggle
        if not value_this_frame and value_last_frame:
            self._released = True
