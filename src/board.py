"""
file: board.py

description: contains code for board representation and move generation.
"""

import typing

# set utility constants
YELLOW: int = 1
RED: int = -1

UNKNOWN: int = 42
DRAW: int = 0

# the board will be represented with a 7x7 bitboard with the bottom as a
# placeholder/helper for move generation. the representation will be from
# bottom left (msb) to top right (lsb).
EMPTY_BOARD: int = sum(
    1 << i for i, x in enumerate(not i % 7 for i in range(49)) if x
)

FULL_BOARD: int = ~EMPTY_BOARD

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

    return b << d if d >= 0 else b >> -d


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
        self.game_result = UNKNOWN

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

    def is_game_over(self) -> bool:
        """
        checks whether or not the current game position is over.
        :return: whether the game is over
        """

        if self.yellow_bitboard | self.red_bitboard == FULL_BOARD:
            self.game_result = DRAW
            return True

        if self.turn == YELLOW:
            win_result = RED
            current_pieces = self.red_bitboard
        else:
            win_result = YELLOW
            current_pieces = self.yellow_bitboard

        if (current_pieces
                & shift(current_pieces, UP)
                & shift(current_pieces, 2 * UP)
                & shift(current_pieces, 3 * UP)) \
                or (current_pieces
                    & shift(current_pieces, DOWN)
                    & shift(current_pieces, 2 * DOWN)
                    & shift(current_pieces, 3 * DOWN)) \
                or (current_pieces
                    & shift(current_pieces, LEFT)
                    & shift(current_pieces, 2 * LEFT)
                    & shift(current_pieces, 3 * LEFT)) \
                or (current_pieces
                    & shift(current_pieces, RIGHT)
                    & shift(current_pieces, 2 * RIGHT)
                    & shift(current_pieces, 3 * RIGHT)) \
                or (current_pieces
                    & shift(current_pieces, UP_LEFT)
                    & shift(current_pieces, 2 * UP_LEFT)
                    & shift(current_pieces, 3 * UP_LEFT)) \
                or (current_pieces
                    & shift(current_pieces, UP_RIGHT)
                    & shift(current_pieces, 2 * UP_RIGHT)
                    & shift(current_pieces, 3 * UP_RIGHT)) \
                or (current_pieces
                    & shift(current_pieces, DOWN_LEFT)
                    & shift(current_pieces, 2 * DOWN_LEFT)
                    & shift(current_pieces, 3 * DOWN_LEFT)) \
                or (current_pieces
                    & shift(current_pieces, DOWN_RIGHT)
                    & shift(current_pieces, 2 * DOWN_RIGHT)
                    & shift(current_pieces, 3 * DOWN_RIGHT)):
            self.game_result = win_result
            return True

        self.game_result = UNKNOWN
        return False

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
    print(tuple(split_bitboard(board.get_legal_moves())))
