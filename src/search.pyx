# cython: language_level=3
# distutils: language = c++

"""
file: search.py

description: contains code for the search implementation.
"""

cimport board

import typing

# set utility constants
cdef int INFINITY = 1 << 15
cdef dict MOVES_LOOKUP = {
    board.ONE << i: 3 - abs(3 - (i // 7)) for i in range(49)
}

cdef dict TRANSPOSITION_TABLE = {}

cdef list order_moves(list moves_list):
    return sorted(moves_list, key=lambda m: MOVES_LOOKUP[m], reverse=True)

cdef tuple _negamax(board.Board b, object e, int d,
                    int alpha = -INFINITY, int beta = INFINITY,
                    int c = board.YELLOW):
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

    cdef tuple key = (b.yellow_bitboard, b.red_bitboard)

    try:
        return TRANSPOSITION_TABLE[key]
    except KeyError:
        pass

    if not d or b.is_game_over():
        return_value = e(b) * c, [], 1
        TRANSPOSITION_TABLE[key] = return_value
        return return_value

    cdef int score = -INFINITY
    cdef board.bitboard best_move = 0
    cdef int nodes = 0
    cdef list legal_moves = board.split_bitboard(b.get_legal_moves())

    cdef int child_score, child_nodes
    cdef list child_pv
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

cpdef search(board.Board b, e: typing.Callable, d: int):
    global TRANSPOSITION_TABLE
    TRANSPOSITION_TABLE = {}

    return _negamax(b, e, d, c=b.turn, alpha=-INFINITY, beta=INFINITY)
