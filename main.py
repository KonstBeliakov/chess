import os
from random import choice

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


def evaluation(board):
    s = 0
    piece_values = {'bP': -1, 'bB': -3, 'bN': -3, 'bR': -5, 'bQ': -9, 'bK': -200,
                    'wP': 1, 'wB': 3, 'wN': 3, 'wR': 5, 'wQ': 9, 'wK': 200,
                    '': 0}
    for x in range(8):
        for y in range(8):
            s += piece_values[board[y][x]]

    return s


def make_move(board):  # makes random move for black
    m = all_moves(board, False)
    move = choice(m)

    board[move[2]][move[3]] = board[move[0]][move[1]]
    board[move[0]][move[1]] = ''


board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Chess")

images = {name: pygame.image.load(f"textures/{name}") for name in os.listdir('textures')}

selected = None  # selected square of the board
move_hints = None
white_turn = True
running = True

font = pygame.font.Font(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            new = ((mouseX - indentX) // square_size, (mouseY - indentY) // square_size)  # new square of the board

            if not (0 <= new[0] < 8 and 0 <= new[1] < 8):
                selected = None
            elif selected and new[0] == selected[0] and new[1] == selected[1]:
                selected = None
            elif selected and board[selected[1]][selected[0]]:
                if move_hints and (new[1], new[0]) in move_hints:
                    board[new[1]][new[0]] = board[selected[1]][selected[0]]
                    board[selected[1]][selected[0]] = ''
                    #white_turn = not white_turn
                    make_move(board)
                    selected = None
                else:
                    selected = new
            else:
                selected = new

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
    if selected is not None:
        pygame.draw.rect(screen, move_hint_color,
                         (indentX + square_size * selected[0], indentY + square_size * selected[1],
                          square_size, square_size))
        if sum(selected) % 2:
            color = black_square_color
        else:
            color = white_square_color
        pygame.draw.rect(screen, color, (indentX + square_size // 20 + square_size * selected[0],
                                         indentY + square_size // 20 + square_size * selected[1],
                                         square_size * 0.9, square_size * 0.9))

    # display pieces
    for x in range(8):
        for y in range(8):
            if board[x][y]:
                screen.blit(images[f'{board[x][y]}.png'], (indentX + y * square_size, indentY + x * square_size))

    # display move hints
    if selected and \
            ((white_turn and board[selected[1]][selected[0]].startswith('w')) or
             (not white_turn and board[selected[1]][selected[0]].startswith('b'))):
        move_hints = [tuple(move) for move in moves(board, selected[1], selected[0])]
    else:
        move_hints = None

    if move_hints and show_move_hints:
        for x, y in move_hints:
            pygame.draw.circle(screen, move_hint_color,
                               (indentX + y * square_size + square_size // 2,
                                indentY + x * square_size + square_size // 2), 10)

    e = evaluation(board)
    text = font.render(f"Evaluation:{'+' if e > 0 else ''}{e}", True, text_color)

    text_rect = text.get_rect()
    text_rect.center = (800, 100)

    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
