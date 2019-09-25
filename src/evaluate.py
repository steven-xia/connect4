import board


PIECE_TABLE = [
    0, 23, 31,  49,  49, 31, 23,
    0, 31, 43,  61,  61, 43, 31,
    0, 49, 61,  88,  88, 61, 49,
    0, 81, 93, 120, 120, 93, 81,
    0, 49, 61,  88,  88, 61, 49,
    0, 31, 43,  61,  61, 43, 31,
    0, 23, 31,  49,  49, 31, 23,
]

PIECE_TABLE = [(1 << i, PIECE_TABLE[i]) for i in range(49) if i % 7]


def evaluate(b: board.Board) -> int:
    score = 0
    for bit, s in PIECE_TABLE:
        score += (b.yellow_bitboard & bit != 0) * s
        score -= (b.red_bitboard & bit != 0) * s
    return score
