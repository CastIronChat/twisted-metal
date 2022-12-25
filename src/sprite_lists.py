from __future__ import annotations

import arcade


class SpriteLists:
    """
    Structure that contains SpriteLists
    """

    vehicles: arcade.SpriteList
    weapons: arcade.SpriteList
    ordnance: arcade.SpriteList
    beams: arcade.SpriteList
    walls: arcade.SpriteList
    huds: arcade.SpriteList

    def __init__(self):
        self.vehicles = arcade.SpriteList()
        self.weapons = arcade.SpriteList()
        self.ordnance = arcade.SpriteList()
        self.beams = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.huds = arcade.SpriteList()

    def draw(self):
        self.walls.draw()
        self.vehicles.draw()
        self.weapons.draw()
        self.ordnance.draw()
        self.beams.draw()
        self.huds.draw()
