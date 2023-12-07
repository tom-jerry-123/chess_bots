"""
Evaluation Function for Chess Engines
Currently uses naive material heuristic
Pawn = 1, Minor Piece = 3, Rook = 5, Queen = 9, Checkmate = 1000
"""

import chess
from agents.evaluation.piece_square_table import PieceSquareTable


# Stores values of various pieces for calculations
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0  # King's value is not relevant for material calculation
}

PAWN_ADVANTAGE = PIECE_VALUES[chess.PAWN]  # a lot of chess stats are measured in terms of pawn advantage

CHECKMATE_SCORE = 1000000


def evaluate(position: chess.Board):
    # Does not check for fifty-move rule or threefold repetition or insufficient material
    if position.is_checkmate():
        return CHECKMATE_SCORE if position.turn == chess.BLACK else -CHECKMATE_SCORE
    elif position.is_stalemate():
        return 0

    score = material_score(position)
    score += piece_position_score(position)
    return score/PAWN_ADVANTAGE


def evaluate_material(position: chess.Board):
    # Does not check for fifty-move rule or threefold repetition
    if position.is_checkmate():
        return 1000000 if position.turn == chess.BLACK else -1000000
    elif position.is_stalemate():
        return 0

    return material_score(position)//PAWN_ADVANTAGE


def material_score(position: chess.Board):
    material = 0
    # Add material for white pieces
    material += PIECE_VALUES[chess.PAWN] * len(position.pieces(chess.PAWN, chess.WHITE))
    material += PIECE_VALUES[chess.KNIGHT] * len(position.pieces(chess.KNIGHT, chess.WHITE))
    material += PIECE_VALUES[chess.BISHOP] * len(position.pieces(chess.BISHOP, chess.WHITE))
    material += PIECE_VALUES[chess.ROOK] * len(position.pieces(chess.ROOK, chess.WHITE))
    material += PIECE_VALUES[chess.QUEEN] * len(position.pieces(chess.QUEEN, chess.WHITE))
    # Subtract material advantage for black pieces
    material -= PIECE_VALUES[chess.PAWN] * len(position.pieces(chess.PAWN, chess.BLACK))
    material -= PIECE_VALUES[chess.KNIGHT] * len(position.pieces(chess.KNIGHT, chess.BLACK))
    material -= PIECE_VALUES[chess.BISHOP] * len(position.pieces(chess.BISHOP, chess.BLACK))
    material -= PIECE_VALUES[chess.ROOK] * len(position.pieces(chess.ROOK, chess.BLACK))
    material -= PIECE_VALUES[chess.QUEEN] * len(position.pieces(chess.QUEEN, chess.BLACK))
    return material


def piece_position_score(position: chess.Board):
    # This hardcoding implementation is faster than the cleaner for loop (about 33% less time)
    score = 0
    for square in position.pieces(chess.PAWN, chess.WHITE):
        score += PieceSquareTable.read(chess.PAWN, chess.WHITE, square)
    for square in position.pieces(chess.KNIGHT, chess.WHITE):
        score += PieceSquareTable.read(chess.KNIGHT, chess.WHITE, square)
    for square in position.pieces(chess.BISHOP, chess.WHITE):
        score += PieceSquareTable.read(chess.BISHOP, chess.WHITE, square)
    for square in position.pieces(chess.ROOK, chess.WHITE):
        score += PieceSquareTable.read(chess.ROOK, chess.WHITE, square)
    for square in position.pieces(chess.QUEEN, chess.WHITE):
        score += PieceSquareTable.read(chess.QUEEN, chess.WHITE, square)
    for square in position.pieces(chess.KING, chess.WHITE):
        score += PieceSquareTable.read(chess.KING, chess.WHITE, square)

    for square in position.pieces(chess.PAWN, chess.BLACK):
        score += PieceSquareTable.read(chess.PAWN, chess.BLACK, square)
    for square in position.pieces(chess.KNIGHT, chess.BLACK):
        score += PieceSquareTable.read(chess.KNIGHT, chess.BLACK, square)
    for square in position.pieces(chess.BISHOP, chess.BLACK):
        score += PieceSquareTable.read(chess.BISHOP, chess.BLACK, square)
    for square in position.pieces(chess.ROOK, chess.BLACK):
        score += PieceSquareTable.read(chess.ROOK, chess.BLACK, square)
    for square in position.pieces(chess.QUEEN, chess.BLACK):
        score += PieceSquareTable.read(chess.QUEEN, chess.BLACK, square)
    for square in position.pieces(chess.KING, chess.BLACK):
        score += PieceSquareTable.read(chess.KING, chess.BLACK, square)
    return score
