from __future__ import annotations

import pygame


class SoundList:
    engine_1 = "assets/audio/engine.ogg"


class TwistedSound:
    @property
    def sound(self):
        return self._sound

    @property
    def channel(self):
        return self._channel

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        self.channel.set_volume(self._volume)

    def __init__(self, selection, times=1):
        self._sound = pygame.mixer.Sound(selection)
        self._channel = pygame.mixer.find_channel()
        self.volume = 0.2

        self.play(times)

    def play(self, times):
        self.channel.play(self.sound, times)

    def stop(self):
        self.channel.stop()


pygame.mixer.init()
