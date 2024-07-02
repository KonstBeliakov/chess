import os
from chess_pieces_moves import *
from copy import deepcopy
from settings import *
import pygame


def show_board(board, moves=None):
    board1 = deepcopy(board)

    if moves is not None:
        for x, y in moves:
            board1[x][y] = 'x'

    print(*range(9), sep='  ')

    for x, line in enumerate(board1):
        print('abcdefgh'[x], end=' ')
        for i in line:
            print(i.rjust(2), end=' ')
        print()


def pos_to_notation(x, y):
    return f'{"abcdefgh"[x]}{y + 1}'


board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', 'bK', '', ''],
    ['', 'wB', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

moves = moves(board, 3, 5)
print(*[pos_to_notation(*i) for i in moves])
show_board(board, moves)

pygame.init()

screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Chess")

images = {name: pygame.image.load(f"textures/{name}") for name in os.listdir('textures')}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bg_color)

    # display board
    for x in range(8):
        for y in range(8):
            if (x + y) % 2:
                color = black_square_color
            else:
                color = white_square_color

            pygame.draw.rect(screen, color, (indentX + x * square_size, indentY + y * square_size, square_size, square_size))

    # display pieces
    for x in range(8):
        for y in range(8):
            if board[x][y]:
                screen.blit(images[f'{board[x][y]}.png'], (indentX + y * square_size, indentY + x * square_size))

    # display move hints
    if moves is not None and show_move_hints:
        for x, y in moves:
            pygame.draw.circle(screen, move_hint_color,
                               (indentX + y * square_size + square_size // 2,
                                indentY + x * square_size + square_size // 2), 10)


    pygame.display.flip()

pygame.quit()
