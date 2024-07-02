def rook_moves(board, x, y):
    color = board[x][y][0]

    moves = []

    # vertical moves
    for i in range(x + 1, 8):
        if board[i][y]:
            if board[i][y][0] != color:
                moves.append([i, y])
            break
        moves.append([i, y])

    for i in range(x - 1, -1, -1):
        if board[i][y]:
            if board[i][y][0] != color:
                moves.append([i, y])
            break
        moves.append([i, y])

    # horizontal moves
    for i in range(y + 1, 8):
        if board[x][i]:
            if board[x][i][0] != color:
                moves.append([x, i])
            break
        moves.append([x, i])

    for i in range(y - 1, -1, -1):
        if board[x][i]:
            if board[x][i][0] != color:
                moves.append([x, i])
            break
        moves.append([x, i])

    return moves


def knight_moves(board, x, y):
    color = board[x][y][0]

    l = [[x + 1, y + 2], [x - 1, y + 2], [x + 2, y + 1], [x - 2, y + 1],
         [x + 2, y - 1], [x - 2, y - 1], [x + 1, y - 2], [x - 1, y - 2]]

    moves = []

    for x_new, y_new in l:
        if (0 <= x_new < 8 and 0 <= y_new < 8) and ((not board[x_new][y_new]) or board[x_new][y_new][0] != color):
            moves.append([x_new, y_new])
    return moves


def king_moves(board, x, y):
    color = board[x][y][0]

    moves = []

    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (0 <= i < 8 and 0 <= j < 8) and (not board[i][j] or board[i][j][0] != color):
                moves.append([i, j])
    return moves


def bishop_moves(board, x, y):
    moves = []
    color = 'w' #board[x][y][0]

    for i in range(1, 8 - x):
        if y + i >= 8:
            break
        if board[x + i][y + i]:
            if board[x + i][y + i][0] != color:
                moves.append([x + i, y + i])
            break
        moves.append([x + i, y + i])

    for i in range(1, 8 - x):
        if y - i < 0:
            break
        if board[x + i][y - i]:
            if board[x + i][y - i][0] != color:
                moves.append([x + i, y - i])
            break
        moves.append([x + i, y - i])

    for i in range(-1, -x - 1, -1):
        if y - i < 0 or y - i >= 8:
            break
        if board[x + i][y - i]:
            if board[x + i][y - i][0] != color:
                moves.append([x + i, y - i])
            break
        moves.append([x + i, y - i])

    for i in range(-1, -x - 1, -1):
        if y + i < 0 or y + i >= 8:
            break
        if board[x + i][y + i]:
            if board[x + i][y + i][0] != color:
                moves.append([x + i, y + i])
            break
        moves.append([x + i, y + i])

    return moves


def queen_moves(board, x, y):
    return bishop_moves(board, x, y) + rook_moves(board, x, y)


def pawn_moves(board, x, y):
    color = board[x][y][0]
    moves = []

    if color == 'b' and (x + 1) < 8:
        if not board[x + 1][y]:
            moves.append([x + 1, y])
        if (y + 1) < 8 and board[x + 1][y + 1] and board[x + 1][y + 1][0] != color:
            moves.append([x + 1, y + 1])
        if (y - 1) >= 0 and board[x + 1][y - 1] and board[x + 1][y - 1][0] != color:
            moves.append([x + 1, y - 1])
        if x == 1 and not board[x + 1][y] and not board[x + 2][y]:
            moves.append([x + 2, y])
    elif (x - 1) >= 0:
        if not board[x - 1][y]:
            moves.append([x - 1, y])
        if (y + 1) < 8 and board[x - 1][y + 1] and board[x - 1][y + 1][0] != color:
            moves.append([x - 1, y + 1])
        if (y - 1) >= 0 and board[x - 1][y - 1] and board[x - 1][y - 1][0] != color:
            moves.append([x - 1, y - 1])
        if x == 6 and not board[x - 1][y] and not board[x - 2][y]:
            moves.append([x - 2, y])
    return moves


def moves(board, x, y):
    if board[x][y]:
        match board[x][y][1]:
            case 'P':
                return pawn_moves(board, x, y)
            case 'B':
                return bishop_moves(board, x, y)
            case 'N':
                return knight_moves(board, x, y)
            case 'R':
                return rook_moves(board, x, y)
            case 'Q':
                return queen_moves(board, x, y)
            case 'K':
                return king_moves(board, x, y)
    return []


def all_moves(board, white_turn=True):
    m = []

    for x in range(8):
        for y in range(8):
            if (board[x][y].startswith('w') and white_turn) or \
                    (board[x][y].startswith('b') and not white_turn):
                m += [[x, y, move[0], move[1]] for move in moves(board, x, y)]
    return m
