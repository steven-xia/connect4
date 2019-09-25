import board


_piece_table: list = [
    0, 23, 31,  49,  49, 31, 23,
    0, 31, 43,  61,  61, 43, 31,
    0, 49, 61,  88,  88, 61, 49,
    0, 81, 93, 120, 120, 93, 81,
    0, 49, 61,  88,  88, 61, 49,
    0, 31, 43,  61,  61, 43, 31,
    0, 23, 31,  49,  49, 31, 23,
]

PIECE_TABLE: list = [
    (1 << i, _piece_table[i]) for i in range(49) if i % 7
]


def evaluate(b: board.Board) -> int:
    score: int = 0
    for bit, s in PIECE_TABLE:
        score += (b.yellow_bitboard & bit != 0) * s
        score -= (b.red_bitboard & bit != 0) * s
    return score
