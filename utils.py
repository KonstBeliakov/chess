import pygame


def play_move_sound():
    pygame.mixer.music.load('sounds/move.mp3')
    pygame.mixer.music.play(0)


def play_capture_sound():
    pygame.mixer.music.load('sounds/capture.mp3')
    pygame.mixer.music.play(0)