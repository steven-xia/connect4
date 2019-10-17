# cython: language_level=3
# distutils: language = c++

"""
file: board.py

description: contains code for board representation and move generation.
"""

# set utility constants
YELLOW = 1
RED = -1

cdef UNKNOWN = 42
cdef DRAW = 0

cdef int _yellow = 1
cdef int _red = -1

cdef int _unknown = 42
cdef int _draw = 0

cdef bitboard ONE = 1

# the board will be represented with a 7x7 bitboard with the bottom as a
# placeholder/helper for move generation. the representation will be from
# bottom left (msb) to top right (lsb).
cdef bitboard EMPTY_BOARD = sum(
    1 << i for i, x in enumerate(not i % 7 for i in range(49)) if x
)

cdef bitboard FULL_BOARD = ~EMPTY_BOARD

# define bit list (list of all bits)
cdef bit_list BIT_LIST = [ONE << i for i in range(49)]

# define column list (list of all column bits)
cdef bitboard first_column = (1 << 8) - 1
cdef bit_list COLUMN_LIST = [first_column << 7 * i for i in range(7)]

# directions for shifting the bitboard representation.
cdef int UP = 1
cdef int RIGHT = 7
cdef int DOWN = -UP
cdef int LEFT = -RIGHT

cdef int UP_RIGHT = UP + RIGHT
cdef int UP_LEFT = UP + LEFT
cdef int DOWN_RIGHT = DOWN + RIGHT
cdef int DOWN_LEFT = DOWN + LEFT

# define utility functions here.
cdef bitboard shift(const bitboard& b, const int& d) nogil:
    """
    returns a copy of the bitboard `b` after shifting by direction `d`.
    :param b: the bitboard to shift
    :param d: direction to shift the bitboard
    :return: copy of shifted bitboard
    """

    return b << d

cdef bit_list split_bitboard(const bitboard& b) nogil:
    """
    returns a list of the possible moves from the given bitboards.
    :param b: bitboard to break down into individual moves.
    :return: list of all moves
    """

    cdef bit_list moves
    moves.reserve(7)

    cdef bitboard column, x
    for column in COLUMN_LIST:
        x = b & column
        if x:
            moves.push_back(x)

    return moves

# main class for board representation.
cdef class Board(object):
    def __init__(self, const bitboard ybb = 0, const bitboard rbb = 0,
                 const int t = _yellow):
        """
        wrapper class for the bitboard board representation. contains multiple
        utility methods for easy utilisation of the board.
        :param ybb: bitboard for yellow pieces
        :param rbb: bitboard for red pieces
        :param t: turn indicator
        """

        # piece bitboards for both players. the yellow player goes first.
        self.yellow_bitboard = ybb
        self.red_bitboard = rbb

        self.turn = t
        self.turn_number = 1
        self.past_moves = []
        self.past_moves.reserve(42)
        self.game_result = _unknown

    def __copy__(self):
        return Board(self.yellow_bitboard, self.red_bitboard, self.turn)

    def __deepcopy__(self):
        return self.__copy__()

    cdef bitboard cget_legal_moves(self) nogil:
        """
        generates all legal moves from the current board position.
        :return: bitboard representation of all legal moves
        """

        cdef bitboard pieces = self.yellow_bitboard | self.red_bitboard | EMPTY_BOARD
        return shift(pieces, UP) & (~pieces)

    cpdef bitboard get_legal_moves(self):
        return self.cget_legal_moves()

    cdef int cis_game_over(self) nogil:
        """
        checks whether or not the current game position is over.
        :return: whether the game is over
        """

        if self.yellow_bitboard | self.red_bitboard == FULL_BOARD:
            self.game_result = _draw
            return True

        cdef int win_result
        cdef bitboard current_pieces
        if self.turn == _yellow:
            win_result = _red
            current_pieces = self.red_bitboard
        else:
            win_result = _yellow
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

        self.game_result = _unknown
        return False

    cpdef int is_game_over(self):
        return self.cis_game_over()

    cdef void cmake_move(self, const bitboard& m) nogil:
        """
        makes a move on the current game position.
        :param m: bitboard representation of the move.
        :return: None
        """

        self.past_moves[self.turn_number] = m
        self.turn_number += 1

        if self.turn == _yellow:
            self.yellow_bitboard += m
            self.turn = _red
        else:
            self.red_bitboard += m
            self.turn = _yellow

    cpdef void make_move(self, const bitboard m):
        self.cmake_move(m)

    cdef void undo_move(self) nogil:
        """
        undoes a move from the current game state.
        :return: None
        """

        self.turn_number -= 1

        if self.turn == _yellow:
            self.red_bitboard -= self.past_moves[self.turn_number]
            self.turn = _red
        else:
            self.yellow_bitboard -= self.past_moves[self.turn_number]
            self.turn = _yellow

if __name__ == "__main__":
    board = Board()
    print(split_bitboard(board.get_legal_moves()))
