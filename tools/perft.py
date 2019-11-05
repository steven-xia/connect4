"""
file: perft.py

description: script to do a performance test on the board implementation.
"""

import math
import sys
import time

import board
import search
import stat_utils


try:
    BENCHMARK = sys.argv[1].lower() == "bench"
except IndexError:
    BENCHMARK = False


def perft_func(d):
    return search.search(board.Board(), d)


def get_confidence(past_times, p=0.95):
    if len(past_times) == 1:
        return (1 << 63) / 1000

    avg = sum(past_times) / len(past_times)
    std = sum((n - avg) ** 2 for n in past_times)
    std = math.sqrt(95 * std) / len(past_times)  # just too look nice. ;)
    # std = math.sqrt(std / len(past_times))  # actual calculation
    conf = stat_utils.phi_inv(0.50 + p / 2) * std
    return conf


def confidence_benchmark(d, c=4.0):
    past_times = []
    conf = 1 << 15
    while 1000 * conf > c:
        s_time = time.time()
        _, l, n = perft_func(d)
        e_time = time.time()

        past_times.append(e_time - s_time)

        med = sorted(past_times)[len(past_times) // 2]
        conf = get_confidence(past_times)

        output = "\rCurrent:  {} ms +- {} ms (95%)".format(
            round(1000 * med, 1),
            round(1000 * conf, 1)
        )
        try:
            sys.stdout.write(output.replace("+-", "±"))
        except UnicodeEncodeError:
            sys.stdout.write(output)

        sys.stdout.flush()

    sys.stdout.write("\n")

    med = sorted(past_times)[len(past_times) // 2]
    return med


if __name__ == "__main__":

    if not BENCHMARK:
        sys.stdout.write("depth".rjust(6))
        sys.stdout.write("time (ms)".rjust(12))
        sys.stdout.write("nodes".rjust(12))
        sys.stdout.write("nps".rjust(11))
        sys.stdout.write("score".rjust(10))
        sys.stdout.write("\n")
        sys.stdout.flush()

        max_depth = 14

        for depth in range(max_depth):
            start_time = time.time()
            score, pv, nodes_searched = perft_func(depth + 1)
            end_time = time.time()

            time_taken = end_time - start_time
            speed = 0 if time_taken == 0 else nodes_searched / time_taken

            sys.stdout.write(str(depth + 1).rjust(6))
            sys.stdout.write(str(round(1000 * time_taken)).rjust(12))
            sys.stdout.write(str(nodes_searched).rjust(12))
            sys.stdout.write(str(round(speed)).rjust(11))
            sys.stdout.write(str(score / 100).rjust(10))
            sys.stdout.write("\n")
            sys.stdout.flush()
    else:
        CONFIDENCE = 2.0
        DEPTH = 12

        initial_message = f"Benchmark for: d{DEPTH} +- {CONFIDENCE}"
        try:
            print(initial_message.replace("+-", "±"))
        except UnicodeEncodeError:
            print(initial_message)

        median = confidence_benchmark(d=DEPTH, c=CONFIDENCE)
        print(f"Final time: {1000 * median} ms")
