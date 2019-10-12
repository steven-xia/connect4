# cython: language_level=3

from libcpp.vector cimport vector

ctypedef unsigned long long bitboard
ctypedef vector[unsigned long long] bit_list

cdef int YELLOW, RED, UNKNOWN, DRAW
cdef int UP, RIGHT, DOWN, LEFT, UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT
cdef bitboard ONE, EMPTY_BOARD, FULL_BOARD
cdef bit_list BIT_LIST

cdef bitboard shift(const bitboard& b, const int& d) nogil
cdef bit_list split_bitboard(const bitboard& b) nogil

cdef class Board(object):
    cdef public bitboard yellow_bitboard, red_bitboard
    cdef public int turn, turn_number, game_result
    cdef readonly bit_list past_moves

    cdef bitboard cget_legal_moves(self) nogil
    cdef int cis_game_over(self) nogil
    cdef void cmake_move(self, const bitboard& m) nogil
    cdef void undo_move(self) nogil

    cpdef bitboard get_legal_moves(self)
    cpdef int is_game_over(self)
    cpdef void make_move(self, const bitboard m)
