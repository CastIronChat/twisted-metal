from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple, cast

import arcade

from arena.wall import Wall
from iron_math import set_sprite_location
from linked_sprite import LinkedSprite, LinkedSpriteCircle
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
# Weapon will never create and instance of Player
if TYPE_CHECKING:
    from player import Player


class Ordnance:
    """
    An ordnance can be anything that is created by a weapon or another ordnance included beams, rockets, explosions, etc.
    Ordnace can be conatined in the payload of another ordance to be later activated under the right conditions
    Although by definition, the term ordnance includes weapons as well, this class does not contain the weapons themselves
    """

    sprite: LinkedSprite[Ordnance]
    sprite_lists: SpriteLists
    payload_list: list[Ordnance]
    """
    List of Ordnance that are spawned when this Ordnance collides with something. This could be explosions, hit indicators, more rockets that go in every direction, etc.
    """
    sprite_rotation_offset: float
    exists: bool
    """
    Ordnance is visible and can be collided with.  Used for long-lived projectile objects that are repeatedly added to/removed from the world over time, such as laser beams.
    """

    def __init__(
        self,
        sprite: LinkedSprite[Ordnance],
        sprite_lists: SpriteLists,
        payload_list: list[Ordnance],
    ):
        self.sprite = sprite
        sprite.owner = self
        self.sprite_lists = sprite_lists
        self.payload_list = payload_list
        self.sprite_rotation_offset = 0
        self.exists = False

    @property
    def location(self) -> Tuple[float, float, float]:
        return (
            self.sprite.center_x,
            self.sprite.center_y,
            self.sprite.radians - self.sprite_rotation_offset,
        )

    def append_sprite(self):
        self.sprite_lists.ordnance.append(self.sprite)
        self.exists = True

    def remove_sprite(self):
        self.sprite_lists.ordnance.remove(self.sprite)
        self.exists = False

    def activate_payload(self):
        for payload in self.payload_list:
            payload.activate(self.location)

    def activate(self, spawn_location: Tuple[float, float, float]):
        set_sprite_location(self.sprite, spawn_location)
        self.append_sprite()

    def update(self, delta_time: float):
        ...

    def on_collision_with_wall(self, walls_touching_projectile: arcade.SpriteList):
        ...

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        ...


def update_ordnance(
    delta_time: float,
    sprite_lists: SpriteLists,
):
    for ordnance_sprite in sprite_lists.ordnance:
        ordnance_sprite: LinkedSprite[Ordnance]
        ordnance_sprite.owner.update(delta_time)
