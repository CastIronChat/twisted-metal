from __future__ import annotations

import math
from typing import TYPE_CHECKING, List, Optional, Tuple, cast

import arcade

from arena.wall import Wall
from iron_math import move_sprite_polar
from linked_sprite import LinkedSprite, LinkedSpriteCircle
from ordnances.ordnance import Ordnance
from sprite_lists import SpriteLists

# This allows a circular import only for the purposes of type hints
if TYPE_CHECKING:
    from vehicle import Vehicle


class Explosion(Ordnance):
    damage: float
    explosion_rate: float
    explosion_radius: float
    current_radius: float
    vehicles_hit: list[Vehicle]

    def __init__(
        self,
        color: arcade.color,
        sprite_lists: SpriteLists,
        damage: float,
        explosion_radius: float,
        explosion_rate: float,
    ):
        explosion_appearance = LinkedSpriteCircle[Explosion](
            explosion_radius, color, soft=False
        )
        super().__init__(explosion_appearance, sprite_lists)
        self.sprite.visible = False
        self.color = color
        self.damage = damage
        self.explosion_radius = explosion_radius
        self.explosion_rate = explosion_rate
        self.current_radius = 1
        self.vehicles_hit = []
        # Make a list of all directions in radians in pi/16 (11.25 degree) increments
        directions = [x * (math.pi / 16) for x in range(-16, 16)]
        for direction in directions:
            self.payload_list.append(self.create_sub_explosion(direction))

    def update(self, delta_time: float):
        self.current_radius += delta_time * self.explosion_rate
        if self.current_radius > self.explosion_radius:
            for payload in self.payload_list:
                if payload.exists:
                    payload.remove_sprite()
            self.remove_sprite()

    def create_sub_explosion(self, direction: float):
        sub_explosion_appearance = LinkedSpriteCircle[SubExplosion](
            self.explosion_radius, self.color, soft=False
        )
        sub_explosion = SubExplosion(
            sub_explosion_appearance,
            self.sprite_lists,
            self.damage,
            self,
            self.explosion_rate,
            direction,
        )
        return sub_explosion

    def activate(self, start_location: Tuple[float, float, float]):
        super().activate(start_location)
        self.activate_payload()


class SubExplosion(Ordnance):
    damage: float
    explosion: Explosion
    explosion_rate: float
    direction: float

    def __init__(
        self,
        sprite: LinkedSprite[Ordnance],
        sprite_lists: SpriteLists,
        damage: float,
        explosion: Explosion,
        explosion_rate: float,
        direction: float,
    ):
        super().__init__(sprite, sprite_lists)
        self.damage = damage
        self.explosion = explosion
        self.explosion_rate = explosion_rate
        self.direction = direction
        self.sprite.height = 1
        self.sprite.width = 1

    def update(self, delta_time: float):
        move_sprite_polar(
            self.sprite, self.explosion_rate * 0.8 * delta_time, self.direction
        )
        self.sprite.height += self.explosion_rate * 2 * 0.2 * delta_time
        self.sprite.width += self.explosion_rate * 2 * 0.2 * delta_time

    def on_collision_with_wall(
        self, walls_touching_projectile: list[LinkedSprite[Wall]]
    ):
        self.explosion_rate = 0

    def on_collision_with_vehicle(
        self,
        delta_time: float,
        vehicles_touching_projectile: list[LinkedSprite[Vehicle]],
    ):
        for vehicle_sprite in vehicles_touching_projectile:
            if vehicle_sprite.owner not in self.explosion.vehicles_hit:
                vehicle_sprite.owner.apply_damage(self.damage)
                vehicle_sprite.owner.movement.hit_by_explosion(self.direction)
                self.explosion.vehicles_hit.append(vehicle_sprite.owner)
