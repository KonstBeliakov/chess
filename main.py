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
    global current_evaluation, last_move, board, time_for_move, white_turn, can_move, captured_white, captured_black
    global black_time, white_move_start_time
    current_evaluation, last_move = evaluation(board, r=recursion_depth, white_turn=False)

    if board[last_move[2]][last_move[3]]:
        captured_white.append(board[last_move[2]][last_move[3]])
        print(captured_white, captured_black)
        play_capture_sound()
    else:
        play_move_sound()

    board[last_move[2]][last_move[3]] = board[last_move[0]][last_move[1]]
    board[last_move[0]][last_move[1]] = ''

    time_for_move = perf_counter() - black_move_start_time
    black_time -= time_for_move
    white_move_start_time = perf_counter()
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
small_image_versions = {image_name: pygame.transform.scale(images[image_name], (captured_pieces_size, captured_pieces_size)) for image_name in images}

selected = None  # selected square of the board
move_hints = None
white_turn = True
can_move = True
running = True
time_for_move = None
current_evaluation = 0
font = pygame.font.Font(None, 24)

white_time = 10 * 60
black_time = 10 * 60

white_move_start_time = perf_counter()
black_move_start_time = None

last_move = None
captured_white = []
captured_black = []

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
                        captured_black.append(board[new[1]][new[0]])
                        play_capture_sound()
                    else:
                        play_move_sound()

                    board[new[1]][new[0]] = board[selected[1]][selected[0]]
                    board[selected[1]][selected[0]] = ''

                    white_turn = False
                    can_move = False

                    white_time -= perf_counter() - white_move_start_time

                    black_move_start_time = perf_counter()
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

    # display captured pieces
    pygame.draw.rect(screen, black_square_color,
                     (indentX, indentY - captured_pieces_size - 15, square_size * 8, captured_pieces_size + 10))
    text = font.render('Black captured:', True, text_color)
    screen.blit(text, (indentX + 2 * square_size - 140, indentY - captured_pieces_size - 10))
    for i, piece in enumerate(captured_white):
        img = small_image_versions[f'{piece}.png']
        screen.blit(img, (indentX + 2 * square_size + i * captured_pieces_size, indentY - captured_pieces_size - 15))

    if not white_turn:
        black_time2 = black_time - (perf_counter() - black_move_start_time)
    else:
        black_time2 = black_time

    m = int(black_time2 // 60)
    s = int(black_time2 % 60)
    time_text = font.render(f'Time: {m}:{str(s).rjust(2, "0")}', True, text_color)
    screen.blit(time_text, (indentX + 8 * square_size - 100, indentY - captured_pieces_size - 10))

    pygame.draw.rect(screen, black_square_color,
                     (indentX, indentY + captured_pieces_size + 5 + square_size * 8, square_size * 8, captured_pieces_size + 10))
    text = font.render('White captured:', True, text_color)
    screen.blit(text, (indentX + 2 * square_size - 140, indentY + square_size * 8 + captured_pieces_size + 10))
    for i, piece in enumerate(captured_black):
        img = small_image_versions[f'{piece}.png']
        screen.blit(img, (indentX + 2 * square_size + i * captured_pieces_size, indentY + captured_pieces_size + 5 + square_size * 8))

    if white_turn:
        white_time2 = white_time - (perf_counter() - white_move_start_time)
    else:
        white_time2 = white_time

    m = int(white_time2 // 60)
    s = int(white_time2 % 60)
    text = font.render(f'Time: {m}:{str(s).rjust(2, "0")}', True, text_color)
    screen.blit(text, (indentX + 8 * square_size - 100, indentY + square_size * 8 + captured_pieces_size + 10))

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
