"""
File for class PieceSquareTable
Tracks the score for each position for given piece to motivate putting pieces on good squares
"""

import chess


"""
Below are tables from white's perspective. bottom left [56] is a1, top right [7] h8.
Piece Square Tables from : https://www.chessprogramming.org/Simplified_Evaluation_Function
"""
class PieceSquareTable:
    _PAWN = (
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -10, -10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    )

    _KNIGHT = (
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    )

    _BISHOP = (
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    )

    _ROOK = (
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0
    )

    _QUEEN = (
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    )

    _KING = (
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20
    )

    # Stores the piece square tables
    _TABLES = None

    @staticmethod
    def read(piece_type: chess.PieceType, piece_color: chess.Color, square: chess.Square):
        if PieceSquareTable._TABLES is None:
            PieceSquareTable._build_tables()
        square_index = PieceSquareTable._square_to_index(square)
        return PieceSquareTable._TABLES[piece_type][piece_color][square_index]

    @staticmethod
    def _build_tables():
        PieceSquareTable._TABLES = {
            chess.PAWN: dict(),
            chess.KNIGHT: dict(),
            chess.BISHOP: dict(),
            chess.ROOK: dict(),
            chess.QUEEN: dict(),
            chess.KING: dict(),
        }

        # Piece square tables for White
        PieceSquareTable._TABLES[chess.PAWN][chess.WHITE] = PieceSquareTable._PAWN
        PieceSquareTable._TABLES[chess.KNIGHT][chess.WHITE] = PieceSquareTable._KNIGHT
        PieceSquareTable._TABLES[chess.BISHOP][chess.WHITE] = PieceSquareTable._BISHOP
        PieceSquareTable._TABLES[chess.ROOK][chess.WHITE] = PieceSquareTable._ROOK
        PieceSquareTable._TABLES[chess.QUEEN][chess.WHITE] = PieceSquareTable._QUEEN
        PieceSquareTable._TABLES[chess.KING][chess.WHITE] = PieceSquareTable._KING

        # Piece Square Tables for Black
        PieceSquareTable._TABLES[chess.PAWN][chess.BLACK] = PieceSquareTable._get_flipped_table(PieceSquareTable._PAWN)
        PieceSquareTable._TABLES[chess.KNIGHT][chess.BLACK] = PieceSquareTable._get_flipped_table(PieceSquareTable._KNIGHT)
        PieceSquareTable._TABLES[chess.BISHOP][chess.BLACK] = PieceSquareTable._get_flipped_table(
            PieceSquareTable._BISHOP)
        PieceSquareTable._TABLES[chess.ROOK][chess.BLACK] = PieceSquareTable._get_flipped_table(
            PieceSquareTable._ROOK)
        PieceSquareTable._TABLES[chess.QUEEN][chess.BLACK] = PieceSquareTable._get_flipped_table(
            PieceSquareTable._QUEEN)
        PieceSquareTable._TABLES[chess.KING][chess.BLACK] = PieceSquareTable._get_flipped_table(
            PieceSquareTable._KING)

    # Note that python-chess squares are from 0 to 63 (a1: 0, b1: 1,...h8: 63)
    # Table indices also from 0 to 63, but in our table, a8: 1, b8: 2, ... h1: 63)
    @staticmethod
    def _square_to_index(square: chess.Square):
        index = (7 - square // 8) * 8 + square % 8
        return index

    @staticmethod
    def _get_flipped_table(piece_score_table: tuple):
        piece_score_list = []
        for i in range(7, -1, -1):
            for j in range(8):
                index = i * 8 + j
                piece_score_list.append(-piece_score_table[index])
        return tuple(piece_score_list)

