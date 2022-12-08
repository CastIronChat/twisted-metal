from __future__ import annotations

import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "John Deer Clown School"

TICK_DURATION = 1 / 60
"Duration of a single update tick of the game, measured in seconds"

USE_DEBUGGER_TIMING_FIXES = os.environ.get("USE_DEBUGGER_TIMING_FIXES") == "true"
"""
Locks delta_time to exactly 1/60 of a second regardless of system clock,
to make pausing in the debugger feasible.
Also fixes known issue where, when pausing in debugger, update and draw each get
called twice back-to-back instead of alternating once per.
"""

START_WITH_ALTERNATE_CONTROLLER_LAYOUT = False
"""
Use alternate (Mario Kart-style?) controller layout where A/B are gas and brake,
and triggers are primary/secondary fire.  At this early stage of development,
this flag is meant for experimentation.
"""

PLAYER_COUNT = 4
KEYBOARD_PLAYER_INDEX = 0
KEYBOARD_PLAYER_ALSO_USES_A_CONTROLLER = True
"""
If false, keyboard player will be controlled by keyboard, *not* a controller.
Useful if you want to debug two players and you only have one controller.
"""

DRAW_INPUT_DEBUG_HUD = False
"""
Draw a text overlay listing the name and value of all controller inputs.
"""

START_FULLSCREEN = False
"""
Start the game in fullscreen mode.  Can also be toggled with F11 on keyboard.
"""
