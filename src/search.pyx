# cython: language_level=3
# distutils: language = c++

"""
file: search.py

description: contains code for the search implementation.
"""

from libcpp.algorithm cimport sort
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector

cimport board
cimport evaluate

import random

# define typedefs
cdef struct tt_value:
    int score
    board.bitboard best_move
    int nodes

# set utility constants
cdef int INFINITY = 1 << 15
cdef unordered_map[board.bitboard, int] MOVES_LOOKUP = {
    board.ONE << i: 3 - abs(3 - (i // 7)) for i in range(49)
}

cdef unordered_map[unsigned long long, tt_value] TRANSPOSITION_TABLE
TRANSPOSITION_TABLE.clear()

# set zobrist hashing tables
cdef set past_hashes = set()
cdef unsigned long long max_long = 18446744073709551615
cdef vector[board.bit_list] hashing_tables = []
hashing_tables.reserve(49)
cdef board.bitboard first_hash, second_hash, temp_hash
for i in range(49):
    while True:
        temp_hash = int(random.random() * max_long)
        if temp_hash not in past_hashes:
            past_hashes.add(temp_hash)
            first_hash = temp_hash
            break

    while True:
        temp_hash = int(random.random() * max_long)
        if temp_hash not in past_hashes:
            past_hashes.add(temp_hash)
            second_hash = temp_hash
            break

    hashing_tables.push_back([
        first_hash, second_hash
    ])

cdef unsigned long long hash_key(const board.bitboard& ybb,
                                 const board.bitboard& rbb) nogil:
    cdef unsigned long long h = 0
    cdef board.bitboard p = ybb | rbb

    cdef int i = 0
    cdef board.bitboard b
    for b in board.BIT_LIST:
        if b & ybb:
            h ^= hashing_tables[i][0]
        elif b & rbb:
            h ^= hashing_tables[i][1]
        i += 1

    return h

cdef int sort_comp(const board.bitboard& b1, const board.bitboard& b2) nogil:
    return MOVES_LOOKUP[b1] > MOVES_LOOKUP[b2]

cdef void order_moves(board.bit_list& moves_list) nogil:
    sort(moves_list.begin(), moves_list.end(), sort_comp)

cdef tt_value _negamax(board.Board b, const int& d,
                       int alpha = -INFINITY, int beta = INFINITY,
                       int c = board.YELLOW) nogil:
    """
    implementation of negamax search algorithm with alpha-beta pruning.
    :param b: board to search
    :param d: depth to search to
    :param alpha: parameter for alpha-beta pruning
    :param beta: parameter for alpha-beta pruning
    :param c: perspective to search by
    :return: (score, best move, nodes)
    """

    cdef unsigned long long key = hash_key(b.yellow_bitboard, b.red_bitboard)

    if TRANSPOSITION_TABLE.find(key) != TRANSPOSITION_TABLE.end():
        return TRANSPOSITION_TABLE[key]

    cdef tt_value return_value
    if not d or b.cis_game_over():
        return_value.score = evaluate.evaluate(b) * c
        return_value.nodes = 0
        TRANSPOSITION_TABLE[key] = return_value
        return_value.nodes = 1
        return return_value

    return_value.score = -INFINITY
    return_value.nodes = 0
    cdef board.bit_list legal_moves = board.split_bitboard(b.cget_legal_moves())
    order_moves(legal_moves)

    cdef int move_index
    cdef board.bitboard move
    cdef int child_score
    cdef tt_value child_return_value
    for move_index in range(legal_moves.size()):
        move = legal_moves[move_index]

        b.cmake_move(move)
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
    child_return_value.nodes = 0
    TRANSPOSITION_TABLE[key] = child_return_value

    return return_value

cpdef tuple search(board.Board b, int d):
    global TRANSPOSITION_TABLE
    TRANSPOSITION_TABLE.clear()

    xD = _negamax(b, d, c=b.turn, alpha=-INFINITY, beta=INFINITY)
    return xD["score"], xD["best_move"], xD["nodes"]
