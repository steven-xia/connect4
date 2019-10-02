# cython: language_level=3
# distutils: language = c++

"""
file: evaluate.py

description: contains code for evaluating a game position.
"""

from libcpp.vector cimport vector

cimport board

# define datatypes
cdef struct bits_score_pair:
    board.bitboard bits
    int score

# define piece square table
cdef list _piece_table = [
    0, 23, 31,  49,  49, 31, 23,
    0, 31, 43,  61,  61, 43, 31,
    0, 49, 61,  88,  88, 61, 49,
    0, 81, 93, 120, 120, 93, 81,
    0, 49, 61,  88,  88, 61, 49,
    0, 31, 43,  61,  61, 43, 31,
    0, 23, 31,  49,  49, 31, 23,
]

cdef set _piece_table_values = set(_piece_table)

cdef dict _temp_piece_table = {s: 0 for s in _piece_table_values}
for i in range(49):
    _temp_piece_table[_piece_table[i]] += (board.ONE << i)

cdef vector[bits_score_pair] PIECE_TABLE = []
cdef bits_score_pair pair
for k, v in _temp_piece_table.items():
    if k == 0:
        continue
    pair.bits = v
    pair.score = k
    PIECE_TABLE.push_back(pair)


# define utility functions here.
cdef int popcount(board.bitboard b):
    """
    counts the number of bits in bitboard `b`.
    :param b: bitboard to count
    :return: number of bits
    """

    cdef int n = 0
    while b:
        b &= b - 1
        n += 1
    return n


# main evaluation function
cpdef int evaluate(b: board.Board):
    if b.game_result != board.UNKNOWN:
        return b.game_result * 4200

    cdef int score = 0

    cdef int s
    cdef board.bitboard bits
    cdef bits_score_pair pair
    for pair in PIECE_TABLE:
        score += popcount(b.yellow_bitboard & pair.bits) * pair.score
        score -= popcount(b.red_bitboard & pair.bits) * pair.score

    return score
