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


def perft_func(d):
    return search.search(board.Board(), d)


def time_search(o, d, r=24, elo0=0.0, elo1=100.0):
    past_times = []
    sprt_result = {"finished": False}
    while not sprt_result["finished"]:
        s_time = time.time()
        for _ in range(r):
            _, l, n = perft_func(d)
        e_time = time.time()

        past_times.append((e_time - s_time) / r)

        sprt_result = stat_utils.SPRT(
            {
                "wins": 1 + sum(1000 * past_t < o for past_t in past_times),
                "losses": 1 + sum(1000 * past_t > o for past_t in past_times),
                "draws": 1 + sum(1000 * past_t == o for past_t in past_times)
            },
            elo0, 0.05, elo1, 0.05, 200
        )

        wld = (
            1 + sum(1000 * past_t < o for past_t in past_times),
            1 + sum(1000 * past_t > o for past_t in past_times),
            1 + sum(1000 * past_t == o for past_t in past_times)
        )
        elo_result = stat_utils.get_elo(wld)

        med = sorted(past_times)[len(past_times) // 2]
        avg = sum(past_times) / len(past_times)
        std = sum((n - avg) ** 2 for n in past_times)
        std = math.sqrt(std / len(past_times))
        output = "\rConfidence: {}%  ({} ms +- {} ms)  -->  pElo: {} +- {}  (+{}-{}={})".format(
            round(50 + 50 * sprt_result["llr"] / sprt_result["upper_bound"], 1),
            round(1000 * med, 1),
            round(2 * 1000 * std, 1),
            round(elo_result[0], 1),
            round(elo_result[1], 1),
            wld[0] - 1, wld[1] - 1, wld[2] - 1
        )

        try:
            sys.stdout.write(output.replace("+-", "±"))
        except UnicodeEncodeError:
            sys.stdout.write(output)

        sys.stdout.flush()

    sys.stdout.write("\n")


if __name__ == "__main__":
    OLD_PERFORMANCE = 143.99433135986328
    RUN_LENGTH = 1
    DEPTH = 12

    ELO0 = 0.5
    ELO1 = 4.5

    initial_message = f"SPRT test [{ELO0}, {ELO1}]:"
    try:
        print(initial_message.replace("*", "×"))
    except UnicodeEncodeError:
        print(initial_message)

    time_search(OLD_PERFORMANCE, d=DEPTH, r=RUN_LENGTH, elo0=ELO0, elo1=ELO1)
