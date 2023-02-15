import pygame
import os
import platform

# Windows misses the dll directory for pygame
# The below patch fixes it
if platform.system() == 'Windows':
    os.add_dll_directory(
        os.path.dirname(pygame.__file__)
    )

MASTER = pygame.mixer
MASTER.init()


# This class is intended to be used as a controller
# that controls a universal mixer.
# The interface allows devs to add sounds as objects
# with some control over volume without blocking other sounds.
class TwistedSound:
    machine_gun1 = "assets/audio/machine_gun1.ogg"

    # channel.play
    # channel.stop
    # channel.pause
    # channel.unpause
    @property
    def channel(self):
        return self._channel

    @property
    def volume(self):
        return self._volume

    # A value of 1 is very loud
    @volume.setter
    def volume(self, value):
        self._volume = value
        self.channel.set_volume(self._volume)

    def __init__(self):
        self._channel = MASTER.find_channel()
        self.volume = 0.05
        self.sound = None

    def play(self, times=1):
        self.channel.play(self.sound, times - 1)

    def stop(self):
        self.channel.stop()

    def select(self, selection):
        self.sound = MASTER.Sound(selection)
