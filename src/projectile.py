from __future__ import annotations

import math
from typing import TYPE_CHECKING, List, Optional, Tuple, cast

import arcade

from arena.wall import Wall
from iron_math import (
    add_vec,
    move_sprite_polar,
    polar_to_cartesian,
    set_sprite_location,
    sprite_in_bounds,
)
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


class Projectile(Ordnance):
    """
    A Projectile is a type of Ordncance that is created by a weapon with a direction and speed, and then forgotten about by the weapon.
    When it collides with something, it activates its payload and is removed
    """

    damage: float
    speed: float
    angle_of_motion: float

    def __init__(
        self,
        sprite: LinkedSprite[Ordnance],
        sprite_lists: SpriteLists,
        payload_list: list[Ordnance],
        damage: float,
        muzzle_location: Tuple[float, float, float],
        speed: float,
        angle_of_motion: float,
        sprite_rotation_offet: float = 0,
    ):
        super().__init__(sprite, sprite_lists, payload_list)
        self.damage = damage
        self.speed = speed
        self.angle_of_motion = angle_of_motion
        self.sprite_rotation_offset = sprite_rotation_offet
        set_sprite_location(self.sprite, muzzle_location)
        self.sprite.radians += self.sprite_rotation_offset
        self.append_sprite()

    def update(self, delta_time: float):
        move_sprite_polar(self.sprite, self.speed * delta_time, self.angle_of_motion)
        # check if the projectile left the screen
        if not sprite_in_bounds(self.sprite):
            self.remove_sprite()

    def on_collision_with_wall(self, walls_touching_projectile: arcade.SpriteList):
        self.remove_sprite()
        self.activate_payload()

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        for player_sprite in players_touching_projectile:
            player_sprite: LinkedSprite[Player]
            player_sprite.owner.take_damage(self.damage)
        self.remove_sprite()
        self.activate_payload()


class Beam(Ordnance):
    """
    A Beam is a type of Ordncance that continues to be controlled by the weapon after it is created.
    When it collides with something, it shortens to stop at whatever it is colliding with
    """

    dps: float
    beam_range: float
    muzzle_location: Tuple[float, float, float]
    hit_location: Tuple[float, float, float]

    def __init__(
        self,
        sprite: LinkedSprite[Ordnance],
        sprite_lists: SpriteLists,
        payload_list: list[Ordnance],
        dps: float,
        beam_range: float,
    ):
        super().__init__(sprite, sprite_lists, payload_list)
        self.dps = dps
        self.beam_range = beam_range
        self.muzzle_location = (0, 0, 0)

    def update(self, delta_time: float):
        self.sprite.width = self.beam_range
        self._update_sprite_location()

    def on_collision_with_wall(
        self, walls_touching_projectile: list[LinkedSprite[Wall]]
    ):
        self._shorten_beam(walls_touching_projectile)

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        player: LinkedSprite[Player] = self._shorten_beam(players_touching_projectile)
        if player != None:
            player.owner.take_damage(self.dps * delta_time)

    def _shorten_beam(self, collision_list: list[LinkedSprite]):
        """
        Given a list of sprites the beam collided with, stop the beam at the first sprite it hits.
        Return that first sprite
        """
        collisions = arcade.SpriteList()
        closest_collision: Optional[LinkedSprite] = None
        for collision in collision_list:
            collisions.append(collision)
        point: Tuple[float, float] = self.muzzle_location[:2]
        point_vec: Tuple[float, float] = polar_to_cartesian(1, self.sprite.radians)
        for x in range(1, self.beam_range):
            if arcade.get_sprites_at_point(point, collisions):
                closest_collision = arcade.get_sprites_at_point(point, collisions)[0]
                self.sprite.width = x
                self.hit_location = (point[0], point[1], self.sprite.radians)
                break
            point = add_vec(point, point_vec)
        self._update_sprite_location()
        return closest_collision

    def _update_sprite_location(self):
        set_sprite_location(self.sprite, self.muzzle_location)
        move_sprite_polar(self.sprite, self.sprite.width / 2, self.muzzle_location[2])


class Explosion(Ordnance):
    damage: float
    explosion_rate: float
    explosion_radius: float
    current_radius: float
    players_hit: list[Player]

    def __init__(
        self,
        color: arcade.color,
        sprite_lists: SpriteLists,
        payload_list: list[Ordnance],
        damage: float,
        explosion_radius: float,
        explosion_rate: float,
    ):
        explosion_appearance = LinkedSpriteCircle[Explosion](
            explosion_radius, color, soft=False
        )
        super().__init__(explosion_appearance, sprite_lists, payload_list)
        self.sprite.visible = False
        self.color = color
        self.damage = damage
        self.explosion_radius = explosion_radius
        self.explosion_rate = explosion_rate
        self.current_radius = 1
        self.players_hit = []
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
            [],
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
        payload_list: list[Ordnance],
        damage: float,
        explosion: Explosion,
        explosion_rate: float,
        direction: float,
    ):
        super().__init__(sprite, sprite_lists, payload_list)
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

    def on_collision_with_player(
        self, delta_time: float, players_touching_projectile: list[LinkedSprite[Player]]
    ):
        for player_sprite in players_touching_projectile:
            if player_sprite.owner not in self.explosion.players_hit:
                player_sprite.owner.take_damage(self.damage)
                self.explosion.players_hit.append(player_sprite.owner)


def update_ordnance(
    delta_time: float,
    sprite_lists: SpriteLists,
):
    for ordnance_sprite in sprite_lists.ordnance:
        ordnance_sprite: LinkedSprite[Ordnance]
        ordnance_sprite.owner.update(delta_time)
