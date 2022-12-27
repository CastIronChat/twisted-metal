from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vehicle import Vehicle


class DriveMode:
    """
    Abstract class that tells a car how to drive around.
    """

    def __init__(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.input = self.vehicle.player.input
        self.name = "unnamed"
        self.setup()

    @property
    def input(self):
        return self.player.input

    def setup(self):
        ...

    def drive(self):
        ...
