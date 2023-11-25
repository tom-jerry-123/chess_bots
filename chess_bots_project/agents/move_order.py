"""
Functions for making move ordering heuristics
"""


import chess
from agents.evaluation import eval_func
from agents.evaluation.piece_square_table import PieceSquareTable


def score_move(board: chess.Board, move: chess.Move) -> float:
    score = 0.0
    # Check for mate in one:
    if is_mate_in_one(board, move):
        return 2 * eval_func.CHECKMATE_SCORE

    piece_type_moved = board.piece_type_at(move.from_square)
    captured_type = board.piece_type_at(move.to_square)

    # add position score of destination square
    score += abs(PieceSquareTable.read(piece_type_moved, board.turn, move.to_square))
    # subtract position score of origin square
    score -= abs(PieceSquareTable.read(piece_type_moved, board.turn, move.from_square))

    # Check for capture
    if captured_type is not None:
        # small bug: we actually ignored en passant capture here, but that doesn't matter much
        score += 10 * eval_func.PIECE_VALUES[captured_type] - eval_func.PIECE_VALUES[piece_type_moved]
    # Add score for promotion
    if move.promotion is not None:
        score += eval_func.PIECE_VALUES[move.promotion]
    # Subtract score if square is attacked by pawns
    if board.attackers(not board.turn, move.to_square) & board.pawns:
        score -= eval_func.PIECE_VALUES[piece_type_moved]
    return score


def is_mate_in_one(board: chess.Board, move: chess.Move) -> bool:
    # make move, check if resulting position is checkmate, then unmake move and return result
    board.push(move)
    ret = board.is_checkmate()
    board.pop()
    return ret
