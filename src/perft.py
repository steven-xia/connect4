"""
file: perft.py

description: script to do a performance test on the board implementation.
"""

if __name__ == "__main__":
    import sys
    import time

    import board
    import evaluate
    import search

    sys.stdout.write("depth".rjust(6))
    sys.stdout.write("time (ms)".rjust(11))
    sys.stdout.write("nodes".rjust(12))
    sys.stdout.write("nps".rjust(10))
    sys.stdout.write("\n")
    sys.stdout.flush()

    max_depth = 7

    for depth in range(max_depth):
        start_time = time.time()
        _, pv, nodes_searched = search.negamax(
            board.Board(),
            evaluate.evaluate,
            depth + 1,
            board.YELLOW
        )
        end_time = time.time()

        time_taken = end_time - start_time
        speed = 0 if time_taken == 0 else nodes_searched / time_taken

        sys.stdout.write(str(depth + 1).rjust(6))
        sys.stdout.write(str(round(1000 * time_taken)).rjust(11))
        sys.stdout.write(str(nodes_searched).rjust(12))
        sys.stdout.write(str(round(speed)).rjust(10))
        sys.stdout.write("\n")
        sys.stdout.flush()
