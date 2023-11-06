"""
Evaluation Function for Chess Engines
Currently uses naive material heuristic
Pawn = 1, Minor Piece = 3, Rook = 5, Queen = 9, Checkmate = 1000
"""

import chess


PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # King's value is not relevant for material calculation
}


def evaluate(position: chess.Board):
    # Does not check for fifty-move rule or threefold repetition
    if position.is_checkmate():
        return 1000 if position.turn == chess.BLACK else -1000
    elif position.is_stalemate():
        return 0

    # Else:
    material = 0
    material += PIECE_VALUES[chess.PAWN] * len(position.pieces(chess.PAWN, chess.WHITE))
    material += PIECE_VALUES[chess.KNIGHT] * len(position.pieces(chess.KNIGHT, chess.WHITE))
    material += PIECE_VALUES[chess.BISHOP] * len(position.pieces(chess.BISHOP, chess.WHITE))
    material += PIECE_VALUES[chess.ROOK] * len(position.pieces(chess.ROOK, chess.WHITE))
    material += PIECE_VALUES[chess.QUEEN] * len(position.pieces(chess.QUEEN, chess.WHITE))
    material -= PIECE_VALUES[chess.PAWN] * len(position.pieces(chess.PAWN, chess.BLACK))
    material -= PIECE_VALUES[chess.KNIGHT] * len(position.pieces(chess.KNIGHT, chess.BLACK))
    material -= PIECE_VALUES[chess.BISHOP] * len(position.pieces(chess.BISHOP, chess.BLACK))
    material -= PIECE_VALUES[chess.ROOK] * len(position.pieces(chess.ROOK, chess.BLACK))
    material -= PIECE_VALUES[chess.QUEEN] * len(position.pieces(chess.QUEEN, chess.BLACK))
    return material
