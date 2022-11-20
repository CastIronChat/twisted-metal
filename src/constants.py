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
