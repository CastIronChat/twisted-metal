from __future__ import annotations

import pygame

ENGINE_SOUND_1 = "assets/audio/engine.ogg"


def play_engine_sound(sound=ENGINE_SOUND_1):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(-1)


pygame.mixer.init()
play_engine_sound()
