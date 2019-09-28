"""
file: perft.py

description: script to do a performance test on the board implementation.
"""

import math
import sys
import time

import board
import evaluate
import search


try:
    BENCHMARK = sys.argv[1].lower() == "bench"
except IndexError:
    BENCHMARK = False


def perft_func(d):
    return search.negamax(board.Board(), evaluate.evaluate, d, board.YELLOW)


def time_search(t, d, r=24, v=True):
    t /= r
    past_times = []
    while sum(past_times) < t:
        s_time = time.time()
        for _ in range(r):
            _, l, n = perft_func(d)
        e_time = time.time()

        past_times.append((e_time - s_time) / r)

        if v:
            pct = min(100, 100 * sum(past_times) / t)
            avg = sum(past_times) / len(past_times)
            std = sum((n - avg) ** 2 for n in past_times)
            std = math.sqrt(std / len(past_times))

            sys.stdout.write("\rProgress {}%:  {} ms ± {} ms (95%)".format(
                round(pct, 1),
                round(1000 * avg, 1),
                round(2 * 1000 * std, 1)
            ))
            sys.stdout.flush()

    if v:
        sys.stdout.write("\n")

    avg = sum(past_times) / len(past_times)
    std = sum((n - avg) ** 2 for n in past_times)
    std = math.sqrt(std / len(past_times))

    return avg, std


if __name__ == "__main__":

    if not BENCHMARK:
        sys.stdout.write("depth".rjust(6))
        sys.stdout.write("time (ms)".rjust(12))
        sys.stdout.write("nodes".rjust(12))
        sys.stdout.write("nps".rjust(11))
        sys.stdout.write("\n")
        sys.stdout.flush()

        max_depth = 9

        for depth in range(max_depth):
            start_time = time.time()
            _, pv, nodes_searched = perft_func(depth + 1)
            end_time = time.time()

            time_taken = end_time - start_time
            speed = 0 if time_taken == 0 else nodes_searched / time_taken

            sys.stdout.write(str(depth + 1).rjust(6))
            sys.stdout.write(str(round(1000 * time_taken)).rjust(12))
            sys.stdout.write(str(nodes_searched).rjust(12))
            sys.stdout.write(str(round(speed)).rjust(11))
            sys.stdout.write("\n")
            sys.stdout.flush()
    else:
        time_search(t=3600, d=7, r=24)
