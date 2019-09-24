"""
file: perft.py

description: script to do a performance test on the board implementation.
"""

import board


def perft_func(b: board.Board, d: int = 0) -> int:
    if d == 0:
        return 1

    positions = 0
    for move in board.split_bitboard(b.get_legal_moves()):
        temp_b = b.__copy__()
        temp_b.make_move(move)
        positions += perft_func(temp_b, d - 1)
    return positions


if __name__ == "__main__":
    import sys
    import time

    sys.stdout.write("depth".rjust(6))
    sys.stdout.write("time (ms)".rjust(11))
    sys.stdout.write("nodes".rjust(12))
    sys.stdout.write("nps".rjust(10))
    sys.stdout.write("\n")
    sys.stdout.flush()

    max_depth = 9

    for depth in range(max_depth):
        start_time = time.time()
        nodes_searched = perft_func(board.Board(), depth + 1)
        end_time = time.time()

        time_taken = end_time - start_time
        speed = 0 if time_taken == 0 else nodes_searched / time_taken

        sys.stdout.write(str(depth + 1).rjust(6))
        sys.stdout.write(str(round(1000 * time_taken)).rjust(11))
        sys.stdout.write(str(nodes_searched).rjust(12))
        sys.stdout.write(str(round(speed)).rjust(10))
        sys.stdout.write("\n")
        sys.stdout.flush()
