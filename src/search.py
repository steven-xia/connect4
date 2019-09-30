"""
file: search.py

description: contains code for the search implementation.
"""

import typing

import board

INFINITY: int = 1 << 31

TRANSPOSITION_TABLE: typing.Dict[(typing.Tuple[int, int], int)] = {}


def _negamax(b: board.Board, e: typing.Callable, d: int,
             alpha: int = -INFINITY, beta: int = INFINITY,
             c: int = board.YELLOW) -> (int, typing.List[int]):
    """
    implementation of negamax search algorithm with alpha-beta pruning.
    :param b: board to search
    :param e: evaluation function
    :param d: depth to search to
    :param alpha: parameter for alpha-beta pruning
    :param beta: parameter for alpha-beta pruning
    :param c: perspective to search by
    :return: (score, best moves, nodes)
    """

    try:
        return TRANSPOSITION_TABLE[(b.yellow_bitboard, b.red_bitboard)]
    except KeyError:
        pass

    if not d or b.is_game_over():
        return e(b) * c, [], 1

    score: int = -INFINITY
    best_move: int = 0
    nodes: int = 0
    for move in board.split_bitboard(b.get_legal_moves()):
        b.make_move(move)
        child_score, child_pv, child_nodes = _negamax(
            b, e, d - 1, -beta, -alpha, -c
        )
        b.undo_move()

        nodes += child_nodes
        child_score *= -1

        if child_score > score:
            score = child_score
            best_move = move
            pv = child_pv

            alpha = child_score
            if alpha >= beta:
                break

    TRANSPOSITION_TABLE[(b.yellow_bitboard, b.red_bitboard)] = score, pv, 1

    return score, [best_move] + pv, nodes


def search(b: board.Board, e: typing.Callable, d: int) -> (int, typing.List[int]):
    global TRANSPOSITION_TABLE
    TRANSPOSITION_TABLE = {}

    return _negamax(b, e, d, c=b.turn)
