from pygame import mixer

# This class is intended to be used as a controller
# that controls a universal mixer.
# The interface allows devs to add sounds as objects
# with some control over volume without blocking other sounds.

MASTER = mixer
MASTER.init()


class TwistedSound:
    engine_1 = "assets/audio/engine.ogg"

    # channel.play
    # channel.stop
    # channel.pause
    # channel.unpause
    @property
    def channel(self):
        return self._channel

    @property
    def sound(self):
        return self._sound

    @property
    def volume(self):
        return self._volume

    # A value of 1 is very loud
    @volume.setter
    def volume(self, value):
        self._volume = value
        self.channel.set_volume(self._volume)

    def __init__(self, selection, times=1):
        self._sound = MASTER.Sound(selection)
        self._channel = MASTER.find_channel()
        self._channel.set_volume(0.1)
        self.play(times)

    def play(self, times):
        self.channel.play(self.sound, times)

    def stop(self):
        self.channel.stop()
