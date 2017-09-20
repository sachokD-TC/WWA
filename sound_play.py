import pygame

SOUNDS_OVER_WAV = 'sounds/over.wav'

SOUNDS_HIT_WAV = 'sounds/hit.wav'

SOUNDS_PICK_WAV = 'sounds/pick.wav'


class Sound_play():
    def __init__(self, sound_on):
        self.sound_on = sound_on
        self.pick_sound = pygame.mixer.Sound(SOUNDS_PICK_WAV)
        self.hit_sound = pygame.mixer.Sound(SOUNDS_HIT_WAV)
        self.over_sound = pygame.mixer.Sound(SOUNDS_OVER_WAV)

    def play_pick_sound(self):
        if self.sound_on:
            self.pick_sound.play()

    def play_hit_sound(self):
        if self.sound_on:
            self.hit_sound.play()

    def play_game_over_sound(self):
        if self.sound_on:
            self.over_sound.play()
