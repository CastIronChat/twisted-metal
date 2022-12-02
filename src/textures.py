from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from arcade import load_spritesheet, load_texture


class SpriteSheet:
    def __init__(
        self,
        file_name: Union[str, Path],
        sprite_width: int,
        sprite_height: int,
        columns: int,
        count: int,
        margin: int = 0,
        hit_box_algorithm: Optional[str] = "Simple",
        hit_box_detail: float = 4.5,
    ):
        self.columns = columns
        self.spritesheet = load_spritesheet(
            file_name,
            sprite_width,
            sprite_height,
            columns,
            count,
            margin,
            hit_box_algorithm,
            hit_box_detail,
        )

    def get_texture(self, x: int, y: int):
        return self.spritesheet[x + y * self.columns]


kenney_sheet_1bit = SpriteSheet(
    "assets/spritesheets/colored-transparent.png",
    16,
    16,
    columns=49,
    count=1078,
    margin=1,
    hit_box_algorithm="None",
)


PISTOL = kenney_sheet_1bit.get_texture(37, 9)
LASER_PISTOL = kenney_sheet_1bit.get_texture(38, 9)
SHOTGUN = kenney_sheet_1bit.get_texture(39, 9)
MACHINE_GUN = kenney_sheet_1bit.get_texture(40, 9)
UZI = kenney_sheet_1bit.get_texture(41, 9)
RIFLE = kenney_sheet_1bit.get_texture(42, 9)
ROCKET_LAUNCHER = kenney_sheet_1bit.get_texture(43, 9)
AMMO_CASE = kenney_sheet_1bit.get_texture(43, 9)
ROCKET = kenney_sheet_1bit.get_texture(33, 21)

RED_CAR = load_texture("assets/vehicle/red-car-top-view.png")

PLAYER_AVATARS = [
    load_texture(f"assets/hud/player{index}avatar.png") for index in range(1, 5)
]
