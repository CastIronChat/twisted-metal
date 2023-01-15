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

    def __init__(self, selection, times=1):
        self._sound = pygame.mixer.Sound(selection)
        self._channel = pygame.mixer.find_channel()

        self._channel.set_volume(0.2)
        self.play(times)

    def play(self, times):
        self._channel.play(self._sound, times)

    def stop(self):
        self._channel.stop()


pygame.mixer.init()
