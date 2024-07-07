"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    maxPlayer = 0
    minPlayer = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                maxPlayer += 1
            if board[i][j] == O:
                minPlayer += 1

    if maxPlayer <= minPlayer:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActs = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possibleActs.add((i, j))

    return possibleActs


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    localeBoard = copy.deepcopy(board)
    localeBoard[action[0]][action[1]] = player(board)
    return localeBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winCases = {
        1: ((0, 0), (0, 1), (0, 2)),
        2: ((1, 0), (1, 1), (1, 2)),
        3: ((2, 0), (2, 1), (2, 2)),
        4: ((0, 0), (1, 0), (2, 0)),
        5: ((0, 1), (1, 1), (2, 1)),
        6: ((0, 2), (1, 2), (2, 2)),
        7: ((0, 0), (1, 1), (2, 2)),
        8: ((2, 0), (1, 1), (0, 2))
    }
    for case in winCases.values():
        # Extract the coordinates of the three positions in this case
        (x1, y1), (x2, y2), (x3, y3) = case

        # Check if all three positions are occupied by 'X'
        if board[x1][y1] == board[x2][y2] == board[x3][y3] == 'X':
            return X

        # Check if all three positions are occupied by 'O'
        if board[x1][y1] == board[x2][y2] == board[x3][y3] == 'O':
            return O

        # If no winner is found, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    isEmpty = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                isEmpty = False

    if isEmpty:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)

    def max_value(board):
        if terminal(board):
            return utility(board), None
        v = -math.inf
        best_action = None
        for action in actions(board):
            min_val, _ = min_value(result(board, action))
            if min_val > v:
                v = min_val
                best_action = action
        return v, best_action

    def min_value(board):
        if terminal(board):
            return utility(board), None
        v = math.inf
        best_action = None
        for action in actions(board):
            max_val, _ = max_value(result(board, action))
            if max_val < v:
                v = max_val
                best_action = action
        return v, best_action

    if current_player == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)

    return action
