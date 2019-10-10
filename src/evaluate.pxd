# cython: language_level=3

cimport board

cdef int popcount(board.bitboard b) nogil
cdef int evaluate(board.Board b) nogil
