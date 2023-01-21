from __future__ import annotations

import arcade


class SpriteLists:
    """
    Structure that contains SpriteLists
    """

    vehicles: arcade.SpriteList
    vehicle_attachments: arcade.SpriteList
    ordnance: arcade.SpriteList
    walls: arcade.SpriteList
    huds: arcade.SpriteList

    def __init__(self):
        self.vehicles = arcade.SpriteList()
        self.vehicle_attachments = arcade.SpriteList()
        self.ordnance = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.huds = arcade.SpriteList()

    def draw(self):
        self.walls.draw()
        self.vehicles.draw()
        self.vehicle_attachments.draw()
        self.ordnance.draw()
        self.huds.draw()
