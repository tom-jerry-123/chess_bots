"""
Implementation of Zobrist Hashing
"""


import random

import chess
from timeit import default_timer


class ZobristHash:
    CASTLING_SQUARE_MASKS = (chess.BB_A1, chess.BB_H1, chess.BB_A8, chess.BB_H8)
    Duration = 0

    def __init__(self):
        self._piece_square_hash = {}
        self._castling_rights_hash = {}
        self._en_passant_file_hash = {}
        self._black_turn_hash = int()
        self._initialize_hash_values()

    def _initialize_hash_values(self):
        # initialize piece table
        for piece_type in chess.PIECE_TYPES:
            for color in chess.COLORS:
                for square in chess.SQUARES:
                    self._piece_square_hash[(piece_type, color, square)] = random.getrandbits(64)
        # compute hash keys for castling_rights. Assigns hash key for each possible castling right bitboard
        self._initialize_castling_rights_hash(0, 0)
        # compute hash keys for file with en passant capture
        for i in range(8):
            self._en_passant_file_hash[i] = random.getrandbits(64)
        # compute hash for who's turn it is
        self._black_turn_hash = random.getrandbits(64)

    def _initialize_castling_rights_hash(self, bitmask, index):
        if index >= len(self.CASTLING_SQUARE_MASKS):
            # once bitmask is complete, generate random hash value for the mask
            self._castling_rights_hash[bitmask] = random.getrandbits(64)
            return

        # recursively call function to build castling rights bitmask
        self._initialize_castling_rights_hash(bitmask, index+1)
        self._initialize_castling_rights_hash(bitmask | self.CASTLING_SQUARE_MASKS[index], index+1)

    def compute_hash(self, board: chess.Board):
        start = default_timer()
        board_hash = 0

        for piece_type in chess.PIECE_TYPES:
            for color in chess.COLORS:
                for square in board.pieces(piece_type, color):
                    board_hash ^= self._piece_square_hash[(piece_type, color, square)]

        board_hash ^= self._castling_rights_hash[board.castling_rights]
        en_passant_square = board.ep_square
        if en_passant_square is not None:
            en_passant_file = chess.square_file(en_passant_square)
            board_hash ^= self._en_passant_file_hash[en_passant_file]
        if board.turn == chess.BLACK:
            board_hash ^= self._black_turn_hash

        self.Duration += default_timer() - start

        return board_hash

    def get_turn_hash(self):
        # returns the hash int that represent black's turn
        return self._black_turn_hash

    def get_piece_square_hash(self, piece_type, color, square):
        return self._piece_square_hash[(piece_type, color, square)]

    def get_castling_rights_hash(self, castling_rights):
        return self._castling_rights_hash[castling_rights]

    def get_en_passant_hash(self, ep_square):
        if ep_square is None:
            return 0
        file_num = chess.square_file(ep_square)
        return self._en_passant_file_hash[file_num]
