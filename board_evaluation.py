from functools import lru_cache
from chess_pieces_moves import all_moves
from settings import *


knight_value = [[2.5, 2.7, 2.8, 2.8, 2.8, 2.8, 2.7, 2.5],
                [2.7, 2.8, 2.9, 2.9, 2.9, 2.9, 2.8, 2.7],
                [2.8, 2.9, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8],
                [2.8, 2.9, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8],
                [2.8, 2.9, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8],
                [2.8, 2.9, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8],
                [2.7, 2.8, 2.9, 2.9, 2.9, 2.9, 2.8, 2.7],
                [2.5, 2.7, 2.8, 2.8, 2.8, 2.8, 2.7, 2.5]]

bishop_value = [[2.7, 2.85, 2.85, 2.85, 2.85, 2.85, 2.85, 2.7],
                [2.85, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.85],
                [2.85, 3.0, 3.05, 3.05, 3.05, 3.05, 3.0, 2.85],
                [2.85, 3.0, 3.05, 3.1, 3.1, 3.05, 3.0, 2.85],
                [2.85, 3.0, 3.05, 3.1, 3.1, 3.05, 3.0, 2.85],
                [2.85, 3.0, 3.05, 3.05, 3.05, 3.05, 3.0, 2.85],
                [2.85, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.85],
                [2.7, 2.85, 2.85, 2.85, 2.85, 2.85, 2.85, 2.7]]

pawn_value = [[1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1.05, 1.05, 1, 1, 1],
              [1, 1, 1, 1.35, 1.35, 1, 1, 1],
              [1, 1, 1, 1.35, 1.35, 1, 1, 1],
              [1, 1, 1, 1.05, 1.05, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1]]

piece_values = {'bP': -1, 'bB': -3, 'bN': -3, 'bR': -5, 'bQ': -9, 'bK': -200,
                'wP': 1, 'wB': 3, 'wN': 3, 'wR': 5, 'wQ': 9, 'wK': 200,
                '': 0}


@lru_cache(None)
def evaluation_no_recursion(board: tuple):
    s = 0
    for x in range(8):
        for y in range(8):
            match board[x][y]:
                case '':
                    pass
                case 'wP':
                    s += pawn_value[x][y]
                case 'bP':
                    s -= pawn_value[x][y]
                case 'wN':
                    s += knight_value[x][y]
                case 'bN':
                    s -= knight_value[x][y]
                case 'wB':
                    s += bishop_value[x][y]
                case 'bB':
                    s -= bishop_value[x][y]
                case _:
                    s += piece_values[board[x][y]]
    return s, None


def evaluation(board: tuple, r=0, white_turn=False, current_max=-300, current_min=300):
    if r == 0:
        return evaluation_no_recursion(board)
    else:
        m = all_moves(board, white_turn=white_turn)

        if not white_turn:
            value = 300
        else:
            value = -300

        right_move = None

        for move in m:
            board1 = [[i for i in line] for line in board]
            board1[move[2]][move[3]] = board1[move[0]][move[1]]
            board1[move[0]][move[1]] = ''

            board1 = tuple([tuple(line) for line in board1])

            if not white_turn:
                t = evaluation(board1, r=r - 1, white_turn=not white_turn, current_min=value)[0]
                if t < value:
                    value = t
                    right_move = move
                if value < current_max:
                    return value, right_move
            else:
                t = evaluation(board1, r=r - 1, white_turn=not white_turn, current_max=value)[0]
                if t > value:
                    value = t
                    right_move = move
                if value > current_min:
                    return value, right_move

        return value, right_move
