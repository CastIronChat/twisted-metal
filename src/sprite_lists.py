from __future__ import annotations

import arcade


class SpriteLists:
    """
    Structure that contains SpriteLists
    """

    players: arcade.SpriteList
    projectiles: arcade.SpriteList
    beams: arcade.SpriteList
    walls: arcade.SpriteList
    huds: arcade.SpriteList

    def __init__(self):
        self.players = arcade.SpriteList()
        self.projectiles = arcade.SpriteList()
        self.beams = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.huds = arcade.SpriteList()

    def draw(self):
        self.walls.draw()
        self.players.draw()
        self.projectiles.draw()
        self.beams.draw()
        self.huds.draw()
