import os
import threading
from time import perf_counter

from board_evaluation import evaluation
from chess_pieces_moves import *
from settings import *
from copy import deepcopy
import pygame


def to_notation(x, y):
    return f'{"abcdefgh"[y]}{8 - x}'


def play_move_sound():
    pygame.mixer.music.load('sounds/move.mp3')
    pygame.mixer.music.play(0)


def play_capture_sound():
    pygame.mixer.music.load('sounds/capture.mp3')
    pygame.mixer.music.play(0)


def make_move():
    global current_evaluation, last_move, board, time_for_move, white_turn, can_move
    t = perf_counter()
    current_evaluation, last_move = evaluation(board, r=recursion_depth, white_turn=False)

    if board[last_move[2]][last_move[3]]:
        play_capture_sound()
    else:
        play_move_sound()

    board[last_move[2]][last_move[3]] = board[last_move[0]][last_move[1]]
    board[last_move[0]][last_move[1]] = ''

    time_for_move = perf_counter() - t
    white_turn = True
    can_move = True
    return current_evaluation, last_move


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
can_move = True
running = True
time_for_move = None
current_evaluation = 0
font = pygame.font.Font(None, 24)

last_move = None

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
            elif selected and board[selected[1]][selected[0]] and can_move:
                if move_hints and (new[1], new[0]) in move_hints:
                    if board[new[1]][new[0]]:
                        play_capture_sound()
                    else:
                        play_move_sound()

                    board[new[1]][new[0]] = board[selected[1]][selected[0]]
                    board[selected[1]][selected[0]] = ''

                    white_turn = False
                    can_move = False
                    last_move = [selected[1], selected[0], new[1], new[0]]
                    bot_thread = threading.Thread(target=make_move)
                    bot_thread.start()

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

    # display check square
    for t in False, True:
        if king_pos := is_in_check(board, white_turn=t):
            pygame.draw.rect(screen, check_hint_color,
                             (indentX + square_size * king_pos[1], indentY + square_size * king_pos[0],
                              square_size, square_size))
            if sum(king_pos) % 2:
                color = black_square_color
            else:
                color = white_square_color
            pygame.draw.rect(screen, color, (indentX + square_size // 20 + square_size * king_pos[1],
                                             indentY + square_size // 20 + square_size * king_pos[0],
                                             square_size * 0.9, square_size * 0.9))

    # displaying last move
    if last_move is not None:
        for x, y in [last_move[:2], last_move[2:]]:
            if (x + y) % 2:
                color = last_move_black_color
            else:
                color = last_move_white_color

            pygame.draw.rect(screen, color, (indentX + y * square_size, indentY + x * square_size,
                                             square_size, square_size))

    # display pieces
    for x in range(8):
        for y in range(8):
            if board[x][y]:
                screen.blit(images[f'{board[x][y]}.png'], (indentX + y * square_size, indentY + x * square_size))

    # display move hints
    if selected and can_move and \
            ((white_turn and board[selected[1]][selected[0]].startswith('w')) or
             (not white_turn and board[selected[1]][selected[0]].startswith('b'))):
        move_hints = []
        for move in moves(board, selected[1], selected[0]):
            board1 = deepcopy(board)
            board1[move[0]][move[1]] = board1[selected[1]][selected[0]]
            board1[selected[1]][selected[0]] = ''

            if can_sacrifice_king or not bool(is_in_check(board1, white_turn=not white_turn)):
                move_hints.append(tuple(move))
    else:
        move_hints = None

    if move_hints and show_move_hints:
        for x, y in move_hints:
            pygame.draw.circle(screen, move_hint_color,
                               (indentX + y * square_size + square_size // 2,
                                indentY + x * square_size + square_size // 2), 10)

    # displaying digits 1-8
    for i in range(8):
        text = font.render(str(8 - i), True, text_color)
        screen.blit(text, (indentX - 20, indentY + (i + 0.5) * square_size))

    # displaying letters a-h
    for i, letter in enumerate('abcdefgh'):
        text = font.render(letter, True, text_color)
        screen.blit(text, (indentX + i * square_size + square_size // 2, 10 + indentY + 8 * square_size))

    board1 = tuple([tuple(line) for line in board])
    text = font.render(f"Evaluation:{'+' if current_evaluation > 0 else ''}{round(current_evaluation, 3)}", True,
                       text_color)
    screen.blit(text, (800, 100))

    text2 = font.render(f'time for move: {time_for_move}', True, text_color)
    screen.blit(text2, (800, 150))

    pygame.display.flip()

pygame.quit()
