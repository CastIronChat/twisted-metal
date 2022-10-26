"""
Responsible for interpreting raw inputs from keyboard, mouse, gamepad, whatever
into a set of "virtual" inputs that more closely match what the gameplay
requires.

In the future, will allow different players to be bound to different keys or
different gamepads, and gameplay logic won't need to be littered with
hardcoded gamepad IDs, etc.
"""

class PlayerInput:
    left: bool
    right: bool
    up: bool
    down: bool

    def __init__(self) -> None:
        self.left = False
        self.right = False
        self.up = False
        self.down = False
