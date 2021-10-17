"""
Connect 4 Player
"""


import math
import copy
import random
import numpy as np
from scipy.signal import convolve2d

red = "red"
blue = "blue"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    R_count = 0
    B_count = 0
    for i in range(len(board)):
        for j in range(6):
            if board[i][j] == red:
                R_count += 1
            elif board[i][j] == blue:
                B_count += 1
            else:
                continue
    if R_count == B_count:
        return red
    else:
        return blue


def neighbors(board, action):
    score = 0
    high_score = None
    for i in range(action[0] - 1, action[0] + 2):
        for j in range(action[1] - 1, action[1] + 2):
            if 0 <= i < 5 and 0 <= j < 6:
                if board[i][j] is None:
                    new_action = (i, j)
                    if terminal(result(board, new_action)):
                        return utility(board)
                    if player(board) == red:
                        score = score_board_red(result(board, new_action))
                    else:
                        score = score_board_blue(result(board, new_action))
            high_score = 0
            if abs(score) > high_score:
                high_score = score
    return high_score


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    Possible_Actions = set()
    for i in range(len(board)):
        for j in range(6):
            if i < 4:
                if board[i][j] is None and board[i + 1][j] is not None:
                    Possible_Actions.add((i, j))
            else:
                if board[i][j] is None:
                    Possible_Actions.add((i, j))

    return Possible_Actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn = player(board)
    copy_of_board = copy.deepcopy(board)

    if action in actions(board):
        for i in range(len(copy_of_board)):
            for j in range(6):
                if i == action[0] and j == action[1]:
                    if turn == red:
                        copy_of_board[i][j] = red
                    else:
                        copy_of_board[i][j] = blue
                    return copy_of_board


def score_board_red(board):
    """
    Scores the board for the red player.
    """
    copy_of_board = copy.deepcopy(board)
    for i in range(len(copy_of_board)):
        for j in range(6):
            if copy_of_board[i][j] == red:
                copy_of_board[i][j] = 1
            elif copy_of_board[i][j] == blue:
                copy_of_board[i][j] = 0
            else:
                copy_of_board[i][j] = 0

    x = np.array([np.array(xi) for xi in copy_of_board])
    score = 0
    in_a_row = in_a_row_checker()

    for item in in_a_row:
        if(convolve2d(x, item, mode="valid") == 3).any():
            score = 60
            return score
        elif (convolve2d(x, item, mode="valid") == 2).any():
            if score < 30:
                score = 30
        else:
            score += 0

    return score


def score_board_blue(board):
    """
    Scores the board for the blue player.
    """
    copy_of_board = copy.deepcopy(board)
    for i in range(len(copy_of_board)):
        for j in range(6):
            if copy_of_board[i][j] == red:
                copy_of_board[i][j] = 0
            elif copy_of_board[i][j] == blue:
                copy_of_board[i][j] = 1
            else:
                copy_of_board[i][j] = 0

    x = np.array([np.array(xi) for xi in copy_of_board])
    in_a_row = in_a_row_checker()
    score = 0

    for item in in_a_row:
        if (convolve2d(x, item, mode="valid") == 3).any():
            score = -60
            return score
        elif (convolve2d(x, item, mode="valid") == 2).any():
            if score > -30:
                score = -30
        else:
            score += 0

    return score


def in_a_row_checker():
    """
    Returns the possible winning scenarios (across, up/down, and diagonals).
    """
    horizontal_kernel = np.array([[1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)

    detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
    return detection_kernels


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    R_count = 0
    B_count = 0
    copy_of_board = copy.deepcopy(board)
    if player(board) == blue:
        for i in range(len(copy_of_board)):
            for j in range(6):
                if copy_of_board[i][j] == red:
                    R_count += 1
                    copy_of_board[i][j] = 1
                elif copy_of_board[i][j] == blue:
                    B_count += 1
                    copy_of_board[i][j] = 0
                else:
                    copy_of_board[i][j] = 0
    else:
        for i in range(len(copy_of_board)):
            for j in range(6):
                if copy_of_board[i][j] == red:
                    R_count += 1
                    copy_of_board[i][j] = 0
                elif copy_of_board[i][j] == blue:
                    B_count += 1
                    copy_of_board[i][j] = 1
                else:
                    copy_of_board[i][j] = 0
    x = np.array([np.array(xi) for xi in copy_of_board])
    possible_wins = in_a_row_checker()

    for item in possible_wins:
        if(convolve2d(x, item, mode="valid") >= 4).any():
            if R_count == B_count:
                return blue
            else:
                return red
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # IF NO WINNER, CHECK IF BOARD IS FULL. IF BOARD IS FULL AND NO WINNER, BOARD IS TERMINAL (TIE).
    # ELSE WE HAVE A WINNER, RETURN THAT WINNER.
    victor = winner(board)
    if victor is None:
        isfull = []
        for i in range(len(board)):
            for j in range(6):
                isfull.append(board[i][j])
        if None in isfull:
            return False
        else:
            return True
    else:
        return True


def utility(board):
    """
    Returns 100 if red has won the game, -100 if blue has won, 0 otherwise.
    """
    # RETURN UTILITY VALUE BASED ON GAME OUTCOME.
    if winner(board) == red:
        return 100
    elif winner(board) == blue:
        return -100
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    optimal_move = None

    if board == initial_state():
        action = random.choice(tuple(actions(board)))
        return action
    else:
        counter = 0
        turn = player(board)
        if turn == red:
            i = -math.inf
            for action in actions(board):
                j = min_value(result(board, action), counter)
                if j > i:
                    i = j
                    optimal_move = action
        else:
            i = math.inf
            for action in actions(board):
                j = max_value(result(board, action), counter)
                if j < i:
                    i = j
                    optimal_move = action

        return optimal_move


def max_value(board, counter):
    """
    returns v, maximum value that the max player can achieve, given what the min player will try to do.
    """
    counter += 1
    while True:
        if terminal(board):
            return utility(board)
        if counter == 5:
            return score_board_red(board)

        i = -math.inf
        for action in actions(board):
            i = max(i, min_value(result(board, action), counter))
        return i


def min_value(board, counter):
    """
    returns v, min value that the minimum player can achieve, given what the max player is trying to do.
    """
    counter += 1
    while True:
        if terminal(board):
            return utility(board)
        if counter == 5:
            return score_board_blue(board)

        i = math.inf
        for action in actions(board):
            i = min(i, max_value(result(board, action), counter))
        return i
