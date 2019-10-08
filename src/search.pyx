# cython: language_level=3
# distutils: language = c++

"""
file: search.py

description: contains code for the search implementation.
"""

from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map

cimport board
cimport evaluate

# define typedefs
cdef struct tt_key:
    board.bitboard yellow_bitboard
    board.bitboard red_bitboard

cdef struct tt_value:
    int score
    board.bitboard best_move
    int nodes

# set utility constants
cdef int INFINITY = 1 << 15
cdef unordered_map[board.bitboard, int] MOVES_LOOKUP = {
    board.ONE << i: 3 - abs(3 - (i // 7)) for i in range(49)
}

cdef dict TRANSPOSITION_TABLE = {}

cdef list order_moves(list moves_list):
    return sorted(moves_list, key=lambda m: MOVES_LOOKUP[m], reverse=True)

cdef tt_value _negamax(board.Board b, int d,
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
    :return: (score, best move, nodes)
    """

    cdef tuple key = (b.yellow_bitboard, b.red_bitboard)

    try:
        return TRANSPOSITION_TABLE[key]
    except KeyError:
        pass

    cdef tt_value return_value
    if not d or b.is_game_over():
        return_value.score = evaluate.evaluate(b) * c
        return_value.nodes = 1
        TRANSPOSITION_TABLE[key] = return_value
        return return_value

    return_value.score = -INFINITY
    return_value.best_move = 0
    return_value.nodes = 0
    cdef list legal_moves = board.split_bitboard(b.get_legal_moves())

    cdef int child_score
    cdef tt_value child_return_value
    for move in order_moves(legal_moves):
        b.make_move(move)
        child_return_value = _negamax(b, d - 1, -beta, -alpha, -c)
        b.undo_move()

        child_score = -child_return_value.score
        return_value.nodes += child_return_value.nodes

        if child_score > return_value.score:
            return_value.score = child_score
            return_value.best_move = move

            alpha = child_score
            if alpha >= beta:
                break

    child_return_value.score = return_value.score
    child_return_value.best_move = return_value.best_move
    child_return_value.nodes = 1
    TRANSPOSITION_TABLE[key] = child_return_value

    return return_value

cpdef tuple search(board.Board b, d: int):
    global TRANSPOSITION_TABLE
    TRANSPOSITION_TABLE = {}

    xD = _negamax(b, d, c=b.turn, alpha=-INFINITY, beta=INFINITY)
    return xD["score"], xD["best_move"], xD["nodes"]
