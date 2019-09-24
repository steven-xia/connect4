"""
file: board.py

description: contains code for board representation and move generation.
"""

import typing

# set utility constants
YELLOW: int = 0
RED: int = 1

# the board will be represented with a 7x7 bitboard with the bottom as a
# placeholder/helper for move generation. the representation will be from
# bottom left (msb) to top right (lsb).
EMPTY_BOARD: int = sum(
    1 << i
    for i, x in enumerate(0 if i % 7 else 1 for i in range(49))
    if x
)

# define bit list (list of all bits)
BIT_LIST: typing.Tuple[int] = tuple(1 << i for i in range(49))

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


def shift(b: int, d: int) -> int:
    """
    returns a copy of the bitboard `b` after shifting by direction `d`.
    :param b: the bitboard to shift
    :param d: direction to shift the bitboard
    :return: copy of shifted bitboard
    """

    return b << d


def split_bitboard(b: int) -> typing.Iterator[int]:
    """
    returns an iterable of the possible moves from the given bitboards.
    :param b: bitboard to break down into individual moves.
    :return: iterator of all moves
    """

    return (x for x in (b & bit for bit in BIT_LIST) if x)


# main class for board representation.
class Board(object):
    def __init__(self, ybb: int = 0, rbb: int = 0, t: int = YELLOW):
        """
        wrapper class for the bitboard board representation. contains multiple
        utility methods for easy utilisation of the board.
        :param ybb: bitboard for yellow pieces
        :param rbb: bitboard for red pieces
        :param t: turn indicator
        """

        # piece bitboards for both players. the yellow player goes first.
        self.yellow_bitboard: int = ybb
        self.red_bitboard: int = rbb

        self.turn: int = t
        self.past_moves = []

    def __copy__(self):
        return Board(self.yellow_bitboard, self.red_bitboard, self.turn)

    def __deepcopy__(self):
        return self.__copy__()

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

        self.past_moves.append(m)

        if self.turn == YELLOW:
            self.yellow_bitboard += m
            self.turn = RED
        else:
            self.red_bitboard += m
            self.turn = YELLOW

    def undo_move(self) -> None:
        """
        undoes a move from the current game state.
        :return: None
        """

        if self.turn == YELLOW:
            self.red_bitboard -= self.past_moves.pop()
            self.turn = RED
        else:
            self.yellow_bitboard -= self.past_moves.pop()
            self.turn = YELLOW


if __name__ == "__main__":
    board = Board()
    print(tuple(
        split_bitboard(board.get_legal_moves())
    ))
