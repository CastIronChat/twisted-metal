from __future__ import annotations


class RoundController:
    """
    A single `RoundController` is responsible for starting and ending each round
    of the game.

    For example, if there's a 3-2-1 countdown timer to start the round, the `RoundController`
    can handle that, locking everyone's controls and unlocking when it hits "Go"

    `RoundController` talks to `GameMode`.
    `GameMode` is responsible for deciding when the round ends.
    Once `GameMode` says the round is over, `RoundController` handles the flashy stuff:
    "Player X Wins!" graphics, camerawork, etc.
    """

    # Implementation TBD
