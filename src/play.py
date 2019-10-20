"""
file: play.py

description: contains the script to play the bot.
"""

import string
import sys
import time
import typing

import board

# set piece constants
YELLOW_PIECE: str = "@"
RED_PIECE: str = "-"
EMPTY_PIECE: str = " "

# set color constants
CLEAR: str = "\033[0m"
BOLD: str = "\033[1m"
YELLOW: str = "\033[33m"
RED: str = "\033[31m"

# define non-digits
NON_DIGITS: str = "".join(
    s for s in string.printable if s not in string.digits
)

# generate move conversion tables
COLUMN_TO_BIT: dict = {
    i + 1: tuple(1 << n for n in range(7 * i, 7 * i + 7))
    for i in range(7)
}
BIT_TO_COLUMN: dict = {1 << i: i // 7 + 1 for i in range(49)}


def colorize(s: str, flags: typing.Iterable) -> str:
    return "".join(flags) + s + CLEAR


def convert_to_win(b: board.Board, s: int) -> str:
    pieces_down = 100 * (42 - abs(s))
    if b.turn == board.YELLOW:
        return f"yellow in {pieces_down - b.yellow_bitboard}"
    else:
        return f"red in {pieces_down - b.red_bitboard}"


def get_legal_input(b: board.Board) -> int:
    legal_moves: int = b.get_legal_moves()

    while True:
        try:
            user_input: str = input("> ").strip(NON_DIGITS)
        except (KeyboardInterrupt, EOFError):
            print(colorize("Exiting program... ", RED))
            sys.exit(0)

        if not user_input.isdigit():
            print("Please enter a valid column number.")
            continue

        user_input: int = int(user_input)
        if not 1 <= user_input <= 7:
            print("Please enter a valid column number.")
            continue

        for bit in COLUMN_TO_BIT[user_input]:
            if bit & legal_moves:
                return bit
        else:
            print("That row is filled up, try another.")


def popcount(b):
    n = 0
    while b:
        b &= b - 1
        n += 1
    return n


def print_board(b: board.Board) -> None:
    p = [[EMPTY_PIECE for _ in range(6)] for _ in range(7)]
    for i in range(49):
        if b.yellow_bitboard >> i & 1:
            p[i // 7][i % 7 - 1] = YELLOW_PIECE
        if b.red_bitboard >> i & 1:
            p[i // 7][i % 7 - 1] = RED_PIECE

    p_v = [
        [colorize(c[i], (YELLOW, BOLD)) if c[i] == YELLOW_PIECE
         else colorize(c[i], (RED, BOLD)) for c in p]
        for i in range(5, -1, -1)
    ]
    p_v2 = ["| " + " | ".join(r) + " |" for r in p_v]

    out = "\n".join(p_v2)
    out += "\n" + "   ".join(map(str, range(1, 8))).center(2 + 7 * 4)
    print(out)


def timed_search(b: board.Board, t: float) -> typing.Tuple:
    s_t = time.time()
    s, bm, _ = search.search(b, 1)
    for d in range(2, 42 - popcount(b.yellow_bitboard | b.red_bitboard) + 1):
        print(
            "\rDepth: {}, Score: {}, Best Move: {}".format(
                d - 1, s / 100, BIT_TO_COLUMN[bm]
            ),
            end=""
        )
        s, bm, _ = search.search(b, d)
        if time.time() - s_t > t:
            if abs(s):
                pass
            return bm, d, s
    return bm, "full search", s


if __name__ == "__main__":
    import search

    game_board: board.Board = board.Board()

    for turn_number in range(42):
        print_board(game_board)
        if turn_number % 2 == 0:
            game_board.make_move(get_legal_input(game_board))
        else:
            best_move, depth, score = timed_search(game_board, 0.5)
            game_board.make_move(best_move)
            print(
                "\rDepth: {}, Score: {}, Best Move: {}".format(
                    depth, score / 100, BIT_TO_COLUMN[best_move]
                )
            )

        if game_board.is_game_over():
            break

    print_board(game_board)
