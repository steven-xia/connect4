"""
file: board.py

description: contains code for board representation and move generation.
"""

import typing

# set utility constants
YELLOW = 0
RED = 1

# the board will be represented with a 7x7 bitboard with the bottom as a
# placeholder/helper for move generation. the representation will be from
# bottom left (msb) to top right (lsb).
EMPTY_BOARD: int = sum(
    1 << i
    for i, x in enumerate(0 if i % 7 else 1 for i in range(49))
    if x
)

# directions for shifting the bitboard representation.
UP: int = 1
RIGHT: int = 7
DOWN: int = -UP
LEFT: int = -RIGHT

UP_RIGHT: int = UP + RIGHT
UP_LEFT: int = UP + LEFT
DOWN_RIGHT: int = DOWN + RIGHT
DOWN_LEFT: int = DOWN + LEFT


# define utility functions here.
def shift(b: int, d: int) -> int:
    """
    returns a copy of the bitboard `b` after shifting by direction `d`.
    :param b: the bitboard to shift
    :param d: direction to shift the bitboard
    :return: copy of shifted bitboard
    """

    return b << d


def iter_moves(b: int) -> typing.Iterator[int]:
    """
    returns an iterable of the possible moves from the given bitboards.
    :param b: bitboard to break down into individual moves.
    :return: iterator of all moves
    """

    return (x for x in (b & (1 << i) for i in range(49)) if x)


# main class for board representation.
class Board(object):
    def __init__(self):
        """
        wrapper class for the bitboard board representation. contains multiple
        utility methods for easy utilisation of the board.
        """

        # piece bitboards for both players. the yellow player goes first.
        self.yellow_bitboard: int = 0
        self.red_bitboard: int = 0

        self.turn: int = YELLOW

    def get_legal_moves(self) -> int:
        """
        generates all legal moves from the current board position.
        :return: bitboard representation of all legal moves
        """

        pieces: int = self.yellow_bitboard | self.red_bitboard | EMPTY_BOARD
        return shift(pieces, UP) & (~pieces)

    def make_move(self, m: int) -> None:
        """
        makes a move on the current game position.
        :param m: bitboard representation of the move.
        :return: None
        """

        self.yellow_bitboard if self.turn == YELLOW else self.red_bitboard += m
        self.turn = RED if self.turn == YELLOW else YELLOW


if __name__ == "__main__":
    board = Board()
    print(tuple(
        iter_moves(board.get_legal_moves())
    ))
