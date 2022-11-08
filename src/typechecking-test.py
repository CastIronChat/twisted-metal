import arcade
from typing import TYPE_CHECKING

arcade.color.AERO_BLUE


class Zombie:

    shambling: bool
    max_health: int

    def __init__(self):
        self.shambling = True

    def take_hit(self):
        self.sambling = False


class MadZombie(Zombie):
    health: int

    def take_hit(self):
        self.sambling = False
        self.health += 1


z = Zombie()
z.foo = 123
print(z.foo)
