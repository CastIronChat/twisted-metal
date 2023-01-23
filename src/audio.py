import pygame

# This is a WIP and may not look anything like the solution
# The problem is as follows:
# Play an audio clip/synth with loopless playback/infinitely sends a tone that can be pitch shifted up and down


class TwistedSound:
    engine_1 = "assets/audio/engine.ogg"

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
        self.mixer = pygame.mixer
        self.mixer.init()

        self._sound = self.mixer.Sound(selection)
        self._channel = self.mixer.find_channel()
        self.volume = 0.2

        self.play(times)

    def play(self, times):
        self.channel.play(self.sound, times)

    def stop(self):
        self.channel.stop()
