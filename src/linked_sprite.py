import arcade
import typing

T = typing.TypeVar("T")


class LinkedSprite(typing.Generic[T], arcade.Sprite):
    owner: T


class LinkedSpriteSolidColor(typing.Generic[T], arcade.SpriteSolidColor):
    owner: T


class LinkedSpriteCircle(typing.Generic[T], arcade.SpriteCircle):
    owner: T


AnyLinkedSprite = LinkedSprite[T] | LinkedSpriteSolidColor[T] | LinkedSpriteCircle[T]
