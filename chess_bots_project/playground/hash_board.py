"""
A wrapper class for chess.Board
Contains Zobrist hash of current position so it doesn't have to be computed from scratch every time
"""


import chess
from agents.search.zobrist_hash import ZobristHash
import timeit


class HashBoard:
    """

    """
    def __init__(self, board=chess.Board(), hasher = None):
        self._board = board
        self._hasher = hasher
        if hasher is None:
            self._hasher = ZobristHash()
        self._position_hash = self._hasher.compute_hash(self.get_deep_copy())

    """
    Getter Methods
    """

    def get_shallow_copy(self):
        """
        !!! WARNING: this returns the actual board, NOT a copy !!!
        DO NOT modify board while using it. Use at own risk.
        """
        return self._board

    def get_deep_copy(self):
        return self._board.copy()

    def get_position_hash(self):
        return self._position_hash

    def get_recomputed_hash(self):
        return self._hasher.compute_hash(self._board)

    """
    MOVE-MAKING FUNCTIONS
    """

    def make_move(self, move: chess.Move):
        """
        Does not check legality of move
        Assumes move is either legal or null. In case of null move, piece_type is None
        """

        origin_square = move.from_square
        destination_square = move.to_square
        color = self._board.turn
        move_piece_type = self._board.piece_type_at(origin_square)
        capture_piece_type = self._board.piece_type_at(destination_square)

        # add hash (or undo) representing black's turn. It's the same operation
        self._position_hash ^= self._hasher.get_turn_hash()
        if move_piece_type is None:
            # we assume move is null. Make the move and return
            self._board.push(move)
            return

        # undo hash for location of piece moved
        self._position_hash ^= self._hasher.get_piece_square_hash(move_piece_type, color, origin_square)
        # undo hash for current castling rights
        self._position_hash ^= self._hasher.get_castling_rights_hash(self._board.castling_rights)
        # undo hash for en passant, if applicable
        if self._board.has_legal_en_passant():
            self._position_hash ^= self._hasher.get_en_passant_hash(self._board.ep_square)

        # NOW, MAKE THE MOVE
        self._board.push(move)

        # add hash for piece at destination square
        if move.promotion is not None:
            self._position_hash ^= self._hasher.get_piece_square_hash(move.promotion, color, destination_square)
        else:
            self._position_hash ^= self._hasher.get_piece_square_hash(move_piece_type, color, destination_square)
        # undo hash for captured piece, if any
        if capture_piece_type is not None:
            self._position_hash ^= self._hasher.get_piece_square_hash(capture_piece_type, not color, destination_square)

        # Now we made the move, add hash for new castling rights, and new enpassant capture (if applicable)
        self._position_hash ^= self._hasher.get_castling_rights_hash(self._board.castling_rights)
        if self._board.has_legal_en_passant():
            self._position_hash ^= self._hasher.get_en_passant_hash(self._board.ep_square)

    def undo_move(self):
        """
        Undoes the last move and updates the current position hash accordingly
        """
        # First, undo some hashing done by move; particularly, en passant & castling
        self._position_hash ^= self._hasher.get_castling_rights_hash(self._board.castling_rights)
        if self._board.has_legal_en_passant():
            self._position_hash ^= self._hasher.get_en_passant_hash(self._board.ep_square)

        # Undo hash for turn
        self._position_hash ^= self._hasher.get_turn_hash()

        # *** NOW, UNMAKE THE MOVE ***
        move = self._board.pop()

        origin_square = move.from_square
        destination_square = move.to_square
        color = self._board.turn
        move_piece_type = self._board.piece_type_at(move.from_square)
        capture_piece_type = self._board.piece_type_at(destination_square)

        if move_piece_type is None:
            # we undid a null move
            return

        # undo hash for piece at destination square
        if move.promotion is not None:
            self._position_hash ^= self._hasher.get_piece_square_hash(move.promotion, color, destination_square)
        else:
            self._position_hash ^= self._hasher.get_piece_square_hash(move_piece_type, color, destination_square)
        # redo hash for captured piece, if any
        if capture_piece_type is not None:
            self._position_hash ^= self._hasher.get_piece_square_hash(capture_piece_type, not color, destination_square)

        # redo hash for location of piece moved
        self._position_hash ^= self._hasher.get_piece_square_hash(move_piece_type, color, origin_square)
        # redo hash for last move's castling rights
        self._position_hash ^= self._hasher.get_castling_rights_hash(self._board.castling_rights)
        # redo hash for en passant, if applicable
        if self._board.has_legal_en_passant():
            self._position_hash ^= self._hasher.get_en_passant_hash(self._board.ep_square)

    """
    Printing Functions
    """

    def print_board(self):
        print("*** Printing Board ***")
        print(f"* Board Hash: {self.get_position_hash()} *")
        print(self._board)
        print()
