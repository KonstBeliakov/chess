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

pygame.init()

screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Chess")

images = {name: pygame.image.load(f"textures/{name}") for name in os.listdir('textures')}

selected_square = None
move_hints = None

white_turn = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            new_square = ((mouseX - indentX) // square_size, (mouseY - indentY) // square_size)

            if new_square[0] >= 8 or new_square[0] < 0 or new_square[1] >= 8 or new_square[1] < 0:
                selected_square = None
            elif selected_square is not None and new_square[0] == selected_square[0] and new_square[1] == selected_square[1]:
                selected_square = None
            elif selected_square and board[selected_square[1]][selected_square[0]]:
                if move_hints and any([new_square[1] == move[0] and new_square[0] == move[1] for move in move_hints]):
                    board[new_square[1]][new_square[0]] = board[selected_square[1]][selected_square[0]]
                    board[selected_square[1]][selected_square[0]] = ''
                    white_turn = not white_turn
                    selected_square = None
                else:
                    selected_square = new_square
            else:
                selected_square = new_square

    screen.fill(bg_color)

    # display board
    for x in range(8):
        for y in range(8):
            if (x + y) % 2:
                color = black_square_color
            else:
                color = white_square_color

            pygame.draw.rect(screen, color,
                             (indentX + x * square_size, indentY + y * square_size, square_size, square_size))

    # display selected square
    if selected_square is not None:
        pygame.draw.rect(screen, move_hint_color, (indentX + square_size * selected_square[0],
                                                   indentY + square_size * selected_square[1],
                                                   square_size, square_size))
        if sum(selected_square) % 2:
            color = black_square_color
        else:
            color = white_square_color
        pygame.draw.rect(screen, color, (indentX + square_size // 20 + square_size * selected_square[0],
                                         indentY + square_size // 20 + square_size * selected_square[1],
                                         square_size * 0.9, square_size * 0.9))

    # display pieces
    for x in range(8):
        for y in range(8):
            if board[x][y]:
                screen.blit(images[f'{board[x][y]}.png'], (indentX + y * square_size, indentY + x * square_size))

    # display move hints
    if selected_square is not None and \
            ((white_turn and board[selected_square[1]][selected_square[0]].startswith('w')) or
             (not white_turn and board[selected_square[1]][selected_square[0]].startswith('b'))):
        move_hints = moves(board, selected_square[1], selected_square[0])
    else:
        move_hints = None

    if (move_hints is not None) and show_move_hints:
        for x, y in move_hints:
            pygame.draw.circle(screen, move_hint_color,
                               (indentX + y * square_size + square_size // 2,
                                indentY + x * square_size + square_size // 2), 10)

    pygame.display.flip()

pygame.quit()
