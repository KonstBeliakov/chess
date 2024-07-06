from settings import *
from board import Board
import pygame


def to_notation(x, y):
    return f'{"abcdefgh"[y]}{8 - x}'


pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Chess")

board = Board()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.update(event)

    screen.fill(bg_color)
    board.draw(screen)
    pygame.display.flip()

pygame.quit()
