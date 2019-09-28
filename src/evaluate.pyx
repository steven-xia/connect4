# cython: language_level=3
# distutils: language = c++

"""
file: evaluate.py

description: contains code for evaluating a game position.
"""

import board

# set utility constants
ctypedef unsigned long long bitboard
cdef bitboard ONE = 1

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
    _temp_piece_table[_piece_table[i]] += (ONE << i)

cdef list PIECE_TABLE = [
    (v, k) for k, v in _temp_piece_table.items()
]


# define utility functions here.
cdef int popcount(bitboard b):
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
    cdef int score = 0

    cdef int s
    cdef bitboard bits
    for bits, s in PIECE_TABLE:
        score += popcount(b.yellow_bitboard & bits) * s
        score -= popcount(b.red_bitboard & bits) * s

    return score
