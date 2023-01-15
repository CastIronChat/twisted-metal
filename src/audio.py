import pygame


class SoundList:
    engine_1 = "assets/audio/engine.ogg"


class TwistedSound:
    @property
    def mixer(self):
        return self._mixer

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
        self._mixer = pygame.mixer
        self.mixer.init()

        self._sound = self.mixer.Sound(selection)
        self._channel = self.mixer.find_channel()
        self.volume = 0.2

        self.play(times)

    def play(self, times):
        self.channel.play(self.sound, times)

    def stop(self):
        self.channel.stop()
