from __future__ import annotations

import pygame

SOUND_ENGINE_1 = "assets/audio/engine.ogg"


class TwistedSound:
    @property
    def sound(self):
        return self._sound

    @property
    def channel(self):
        return self._channel

    def __init__(self, selection):
        self._sound = pygame.mixer.Sound(selection)
        self._channel = pygame.mixer.find_channel()

    def play(self, times=1):
        self._channel.play(self._sound, times)

    def stop(self):
        self._channel.stop()


pygame.mixer.init()
