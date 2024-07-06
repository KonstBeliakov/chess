import threading
from copy import deepcopy
from os import listdir
from time import perf_counter

from settings import *
from board_evaluation import *
from chess_pieces_moves import *
from utils import *


class Board:
    def __init__(self):
        self.images = {name: pygame.image.load(f"textures/{name}") for name in listdir('textures')}
        self.small_image_versions = {
            image_name: pygame.transform.scale(self.images[image_name], (captured_pieces_size, captured_pieces_size))
            for image_name in self.images}

        self.selected = None  # selected square of the board
        self.move_hints = None
        self.white_turn = True
        self.can_move = True
        self.running = True
        self.time_for_move = None
        self.current_evaluation = 0
        self.font = pygame.font.Font(None, 24)

        self.white_time = 10 * 60
        self.black_time = 10 * 60

        self.white_move_start_time = perf_counter()
        self.black_move_start_time = None

        self.last_move = None
        self.captured_white = []
        self.captured_black = []

        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

    def draw(self, screen):
        self.display_board(screen)
        self.display_selected_square(screen)
        self.display_check_square(screen)
        self.display_last_move(screen)
        self.display_pieces(screen)
        self.display_captured_pieces(screen)
        self.display_move_hints(screen)
        self.display_board_numbers(screen)

        text = self.font.render(
            f"Evaluation:{'+' if self.current_evaluation > 0 else ''}{round(self.current_evaluation, 3)}", True,
            text_color)
        screen.blit(text, (800, 100))

        text2 = self.font.render(f'time for move: {self.time_for_move}', True, text_color)
        screen.blit(text2, (800, 150))

    def display_board(self, screen):
        for x in range(8):
            for y in range(8):
                if (x + y) % 2:
                    color = black_square_color
                else:
                    color = white_square_color

                pygame.draw.rect(screen, color,
                                 (indentX + x * square_size, indentY + y * square_size, square_size, square_size))

    def display_selected_square(self, screen):
        if self.selected is not None:
            pygame.draw.rect(screen, move_hint_color,
                             (indentX + square_size * self.selected[0], indentY + square_size * self.selected[1],
                              square_size, square_size))
            if sum(self.selected) % 2:
                color = black_square_color
            else:
                color = white_square_color
            pygame.draw.rect(screen, color, (indentX + square_size // 20 + square_size * self.selected[0],
                                             indentY + square_size // 20 + square_size * self.selected[1],
                                             square_size * 0.9, square_size * 0.9))

    def display_check_square(self, screen):
        for t in False, True:
            if king_pos := is_in_check(self.board, white_turn=t):
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

    def display_last_move(self, screen):
        if self.last_move is not None:
            for x, y in [self.last_move[:2], self.last_move[2:]]:
                if (x + y) % 2:
                    color = last_move_black_color
                else:
                    color = last_move_white_color

                pygame.draw.rect(screen, color, (indentX + y * square_size, indentY + x * square_size,
                                                 square_size, square_size))

    def display_pieces(self, screen):
        for x in range(8):
            for y in range(8):
                if self.board[x][y]:
                    screen.blit(self.images[f'{self.board[x][y]}.png'],
                                (indentX + y * square_size, indentY + x * square_size))

    def display_captured_pieces(self, screen):
        pygame.draw.rect(screen, black_square_color,
                         (indentX, indentY - captured_pieces_size - 15, square_size * 8, captured_pieces_size + 10))
        text = self.font.render('Black captured:', True, text_color)
        screen.blit(text, (indentX + 2 * square_size - 140, indentY - captured_pieces_size - 10))
        for i, piece in enumerate(self.captured_white):
            img = self.small_image_versions[f'{piece}.png']
            screen.blit(img,
                        (indentX + 2 * square_size + i * captured_pieces_size, indentY - captured_pieces_size - 15))

        if not self.white_turn:
            black_time2 = self.black_time - (perf_counter() - self.black_move_start_time)
        else:
            black_time2 = self.black_time

        m = int(black_time2 // 60)
        s = int(black_time2 % 60)
        time_text = self.font.render(f'Time: {m}:{str(s).rjust(2, "0")}', True, text_color)
        screen.blit(time_text, (indentX + 8 * square_size - 100, indentY - captured_pieces_size - 10))

        pygame.draw.rect(screen, black_square_color,
                         (indentX, indentY + captured_pieces_size + 5 + square_size * 8, square_size * 8,
                          captured_pieces_size + 10))
        text = self.font.render('White captured:', True, text_color)
        screen.blit(text, (indentX + 2 * square_size - 140, indentY + square_size * 8 + captured_pieces_size + 10))
        for i, piece in enumerate(self.captured_black):
            img = self.small_image_versions[f'{piece}.png']
            screen.blit(img, (
                indentX + 2 * square_size + i * captured_pieces_size,
                indentY + captured_pieces_size + 5 + square_size * 8))

        if self.white_turn:
            white_time2 = self.white_time - (perf_counter() - self.white_move_start_time)
        else:
            white_time2 = self.white_time

        m = int(white_time2 // 60)
        s = int(white_time2 % 60)
        text = self.font.render(f'Time: {m}:{str(s).rjust(2, "0")}', True, text_color)
        screen.blit(text, (indentX + 8 * square_size - 100, indentY + square_size * 8 + captured_pieces_size + 10))

    def display_move_hints(self, screen):
        if self.selected and self.can_move and \
                ((self.white_turn and self.board[self.selected[1]][self.selected[0]].startswith('w')) or
                 (not self.white_turn and self.board[self.selected[1]][self.selected[0]].startswith('b'))):
            self.move_hints = []
            for move in moves(self.board, self.selected[1], self.selected[0]):
                board1 = deepcopy(self.board)
                board1[move[0]][move[1]] = board1[self.selected[1]][self.selected[0]]
                board1[self.selected[1]][self.selected[0]] = ''

                if can_sacrifice_king or not bool(is_in_check(board1, white_turn=not self.white_turn)):
                    self.move_hints.append(tuple(move))

            if self.white_turn and white_can_castle(self.board) and self.board[self.selected[1]][self.selected[0]] == 'wK':
                self.move_hints.append((7, 6))
        else:
            self.move_hints = None

        if self.move_hints and show_move_hints:
            for x, y in self.move_hints:
                pygame.draw.circle(screen, move_hint_color,
                                   (indentX + y * square_size + square_size // 2,
                                    indentY + x * square_size + square_size // 2), 10)

    def display_board_numbers(self, screen):
        # displaying digits 1-8
        for i in range(8):
            text = self.font.render(str(8 - i), True, text_color)
            screen.blit(text, (indentX - 20, indentY + (i + 0.5) * square_size))

        # displaying letters a-h
        for i, letter in enumerate('abcdefgh'):
            text = self.font.render(letter, True, text_color)
            screen.blit(text, (indentX + i * square_size + square_size // 2, 10 + indentY + 8 * square_size))

    def update(self, event):
        mouseX, mouseY = event.pos
        new = ((mouseX - indentX) // square_size, (mouseY - indentY) // square_size)  # new square of the board

        if not (0 <= new[0] < 8 and 0 <= new[1] < 8):
            self.selected = None
        elif self.selected and new[0] == self.selected[0] and new[1] == self.selected[1]:
            self.selected = None
        elif self.selected and self.board[self.selected[1]][self.selected[0]] and self.can_move:
            if not self.move_hints or (new[1], new[0]) not in self.move_hints:
                self.selected = new
            else:
                if self.board[new[1]][new[0]]:
                    self.captured_black.append(self.board[new[1]][new[0]])
                    play_capture_sound()
                else:
                    play_move_sound()

                make_move_on_board((self.selected[1], self.selected[0], new[1], new[0]), self.board)

                self.white_turn = False
                self.can_move = False

                self.white_time -= perf_counter() - self.white_move_start_time
                self.black_move_start_time = perf_counter()

                self.last_move = [self.selected[1], self.selected[0], new[1], new[0]]
                bot_thread = threading.Thread(target=self.make_move)
                bot_thread.start()

                self.selected = None
        else:
            self.selected = new

    def make_move(self):
        self.current_evaluation, self.last_move = evaluation(self.board, r=recursion_depth, white_turn=False)

        make_move_on_board(self.last_move, self.board)

        if self.last_move in ['wO-O', 'bO-O']:
            play_move_sound()
        elif self.board[self.last_move[2]][self.last_move[3]]:
            self.captured_white.append(self.board[self.last_move[2]][self.last_move[3]])
            play_capture_sound()
        else:
            play_move_sound()

        self.time_for_move = perf_counter() - self.black_move_start_time
        self.black_time -= self.time_for_move
        self.white_move_start_time = perf_counter()

        self.white_turn = True
        self.can_move = True

        return self.current_evaluation, self.last_move
