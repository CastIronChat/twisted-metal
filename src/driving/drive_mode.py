from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from player import Player


class DriveMode:
    """
    Abstract class that tells a car how to drive around.
    """

    def __init__(self, player: Player):
        self.player = player
        self.input = self.player.input
        self.setup()

    def setup(self):
        ...

    def drive(self):
        ...
