from __future__ import annotations

from typing import TYPE_CHECKING

from driving.drifty_car import drifty_car, mike_drifty_car, scaled_down_drifty_car

if TYPE_CHECKING:
    from player import Player


def create_drive_modes(player: Player):
    return [drifty_car(player), scaled_down_drifty_car(player), mike_drifty_car(player)]
