from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple, cast

import arcade
from arena.wall import Wall
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from iron_math import move_sprite_polar, set_sprite_location
from linked_sprite import LinkedSprite
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
# Weapon will never create and instance of Player
if TYPE_CHECKING:
    from player import Player


class Projectile:
    """
    A projectile can be anything that is created by a weapon or another projectile included beams, rockets, etc.
    It stores the characteristics of the projectile and is responible the associated sprite
    """

    sprite: LinkedSprite[Projectile]
    sprite_lists: SpriteLists
    damage: float
    speed: float
    radians: float
    sprite_rotation_offset: float
    exists: bool
    beam: bool
    beam_range: float
    explodes: bool

    def __init__(
        self,
        sprite: LinkedSprite[Projectile],
        sprite_lists: SpriteLists,
        speed: float,
        radians: float,
        damage: float,
    ):
        self.sprite = sprite
        sprite.owner = self
        self.sprite_lists = sprite_lists
        self.speed = speed
        self.radians = radians
        self.damage = damage
        self.beam = False
        self.beam_range = 0
        self.explodes = False
        self.sprite_rotation_offset = 0
        self.append_sprite()

    def update(self, delta_time: float):
        move_sprite_polar(self.sprite, self.speed * delta_time, self.radians)
        #check if the projectile left the screen
        if (
            self.sprite.center_x < 0
            or self.sprite.center_x > SCREEN_WIDTH
            or self.sprite.center_y < 0
            or self.sprite.center_y > SCREEN_HEIGHT
        ):
            if not self.beam:
                self.remove_sprite()

    def set_location(self, location: Tuple[float, float, float]):
        set_sprite_location(self.sprite, location)
        self.sprite.radians += self.sprite_rotation_offset

    def set_beam(self, range: float):
        self.beam = True
        self.beam_range = range

    def set_sprite_rotation_offset(self, radians: float):
        self.sprite_rotation_offset = radians

    def set_explodes(self):
        self.explodes = True
    
    def append_sprite(self):
        self.sprite_lists.projectiles.append(self.sprite)
        self.exists = True

    def remove_sprite(self):
        self.sprite_lists.projectiles.remove(self.sprite)
        self.exists = False

    def on_collision_with_wall(self, walls_touching_projectile: arcade.SpriteList):
        if not self.beam:    
            self.remove_sprite()
        
    def on_collision_with_player(self, delta_time, players_touching_projectile: arcade.SpriteList):
        for player in players_touching_projectile:
            player: LinkedSprite[Player]
            if self.beam:
                player.owner.player_health -= self.damage * delta_time
            else:
                player.owner.player_health -= self.damage
        if not self.beam: 
            self.remove_sprite()



def update_projectiles(
    delta_time: float,
    sprite_lists: SpriteLists,
):
    for projectile_sprite in sprite_lists.projectiles:
        projectile_sprite: LinkedSprite[Projectile]
        projectile_sprite.owner.update(delta_time)
        
