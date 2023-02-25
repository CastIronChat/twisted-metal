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
MASTER.set_num_channels(128)

# This class is intended to be used as a controller
# that controls a universal mixer.
# The interface allows devs to add sounds as objects
# with some control over volume without blocking other sounds.
class TwistedSound:
    machine_gun1 = "assets/audio/machine_gun1.ogg"

    sound = None
    channel = None

    def play(self, times=1, volume=0.05):
        self.channel = MASTER.find_channel()
        self.channel.set_volume(volume)
        self.channel.play(self.sound, times - 1)

    def stop(self):
        self.channel.stop()

    def select(self, selection):
        self.sound = MASTER.Sound(selection)
