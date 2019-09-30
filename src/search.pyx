# cython: language_level=3
# distutils: language = c++

"""
file: search.py

description: contains code for the search implementation.
"""

import typing

import board

INFINITY: int = 1 << 31
MOVES_LOOKUP = {
    1 << i: 3 - abs(3 - (i // 7)) for i in range(49)
}

TRANSPOSITION_TABLE: typing.Dict[(typing.Tuple[int, int], int)] = {}


def order_moves(moves_list: typing.Iterable) -> list:
    return sorted(moves_list, key=lambda m: MOVES_LOOKUP[m], reverse=True)


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

    key = (b.yellow_bitboard, b.red_bitboard)

    try:
        return TRANSPOSITION_TABLE[key]
    except KeyError:
        pass

    if not d or b.is_game_over():
        return_value = e(b) * c, [], 1
        TRANSPOSITION_TABLE[key] = return_value
        return return_value

    score: int = -INFINITY
    best_move: int = 0
    nodes: int = 0
    legal_moves = board.split_bitboard(b.get_legal_moves())
    for move in order_moves(legal_moves):
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

    TRANSPOSITION_TABLE[key] = score, pv, 1

    return score, [best_move] + pv, nodes


def search(b: board.Board, e: typing.Callable, d: int) -> (int, typing.List[int]):
    global TRANSPOSITION_TABLE
    TRANSPOSITION_TABLE = {}

    return _negamax(b, e, d, c=b.turn)
