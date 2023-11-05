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
    elif position.is_insufficient_material():
        return 0
    # Else:
    material = 0
    for square in chess.SQUARES:
        piece = position.piece_at(square)
        if piece is not None:
            piece_value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                material += piece_value
            else:
                material -= piece_value
    return material
