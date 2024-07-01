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