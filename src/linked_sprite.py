from __future__ import annotations

import typing

import arcade

T = typing.TypeVar("T")


class LinkedSprite(typing.Generic[T], arcade.Sprite):
    owner: T


class LinkedSpriteSolidColor(typing.Generic[T], arcade.SpriteSolidColor):
    owner: T


class LinkedSpriteCircle(typing.Generic[T], arcade.SpriteCircle):
    owner: T
