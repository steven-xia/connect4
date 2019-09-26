"""
file: evaluate.py

description: contains code for evaluating a game position.
"""

import board

# define piece square table
_piece_table: list = [
    0, 23, 31,  49,  49, 31, 23,
    0, 31, 43,  61,  61, 43, 31,
    0, 49, 61,  88,  88, 61, 49,
    0, 81, 93, 120, 120, 93, 81,
    0, 49, 61,  88,  88, 61, 49,
    0, 31, 43,  61,  61, 43, 31,
    0, 23, 31,  49,  49, 31, 23,
]

_piece_table_values: set = set(_piece_table)

_temp_piece_table: dict = {s: 0 for s in _piece_table_values}
for i in range(49):
    _temp_piece_table[_piece_table[i]] += (1 << i)

PIECE_TABLE: list = [
    (v, k) for k, v in _temp_piece_table.items()
]


# define utility functions here.
def popcount(b: int) -> int:
    """
    counts the number of bits in bitboard `b`.
    :param b: bitboard to count
    :return: number of bits
    """

    n: int = 0
    while b:
        b &= b - 1
        n += 1
    return n


def evaluate(b: board.Board) -> int:
    score: int = 0
    for bits, s in PIECE_TABLE:
        score += popcount(b.yellow_bitboard & bits) * s
        score -= popcount(b.red_bitboard & bits) * s
    return score
