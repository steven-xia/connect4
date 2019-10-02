from libcpp.vector cimport vector

ctypedef unsigned long long bitboard
ctypedef vector[unsigned long long] bit_list


cdef bitboard shift(const bitboard b, const int d):
cpdef bit_list split_bitboard(const bitboard b):


cdef class Board(object):
    cdef public bitboard yellow_bitboard, red_bitboard
    cdef public int turn, turn_number, game_result
    cdef readonly bit_list past_moves

    cpdef bitboard get_legal_moves(self):
    cpdef int is_game_over(self):
    cpdef void make_move(self, const bitboard m):
    cpdef void undo_move(self):
