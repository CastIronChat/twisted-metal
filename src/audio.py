import pygame
import os
import platform
from typing import Optional

# Windows misses the dll directory for pygame
# The below patch fixes it
if platform.system() == 'Windows':
    os.add_dll_directory(
        os.path.dirname(pygame.__file__)
    )

MASTER = pygame.mixer
MASTER.init()
MASTER.set_num_channels(128)

# This class is intended to be used as a controller
# that controls a universal mixer.
# The interface allows devs to add sounds as properties on objects
# with some control over volume without blocking other sounds.
class TwistedSound:
    EXPLOSION1 = "assets/audio/explosion1.ogg"
    MACHINE_GUN1 = "assets/audio/machine_gun1.ogg"
    COUNTDOWN1 = "assets/audio/countdown1.ogg"
    COUNTDOWN2 = "assets/audio/countdown2.ogg"

    sound: Optional[MASTER.Sound] = None
    channel: Optional[MASTER.Channel] = None

    def play(self, selection, volume=0.05, times=1):
        self.select(selection)
        self.channel = MASTER.find_channel(force=True)
        self.channel.set_volume(volume)
        self.channel.play(self.sound, times - 1)

    def stop(self):
        self.channel.stop()

    def select(self, selection: str):
        self.sound = MASTER.Sound(selection)
