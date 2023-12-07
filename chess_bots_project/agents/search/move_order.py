"""
Functions for making move ordering heuristics
"""


import chess
from agents.evaluation import eval_func
from agents.evaluation.piece_square_table import PieceSquareTable


def get_ordered_move_lst(board: chess.Board):
    """
    Returns an ordered move list, along with their move scores.
    """
    move_lst = []
    for move in board.legal_moves:
        move_score = score_move(board, move)
        move_lst.append((move, move_score))
    move_lst.sort(key=lambda x: x[1], reverse=True)
    return move_lst


def simple_score_move(board: chess.Board, move: chess.Move) -> float:
    """
    Calculates a simple score heuristic for moves only looking at captures and promotions
    Returns score in terms of pawn advantage
    """
    score = 0.0

    piece_type_moved = board.piece_type_at(move.from_square)
    captured_type = board.piece_type_at(move.to_square)

    # Check for capture
    if captured_type is not None:
        # small bug: we actually ignored en passant capture here, but that doesn't matter much
        score += 10 * eval_func.PIECE_VALUES[captured_type] - eval_func.PIECE_VALUES[piece_type_moved]
    # Add score for promotion
    if move.promotion is not None:
        score += eval_func.PIECE_VALUES[move.promotion]
    # Adjust the score by pawn advantage before returning
    return score / eval_func.PAWN_ADVANTAGE


def score_move(board: chess.Board, move: chess.Move) -> float:
    """
    A much more comprehensive move ordering function
    """
    score = 0.0
    # Check for mate in one:
    if is_mate_in_one(board, move):
        return 2 * eval_func.CHECKMATE_SCORE

    piece_type_moved = board.piece_type_at(move.from_square)
    captured_type = board.piece_type_at(move.to_square)
    perspective = 1 if board.turn else -1
    pos_score_scale_factor = 1 if piece_type_moved == chess.PAWN else 0.2

    # add position score of destination square
    score += perspective * pos_score_scale_factor * PieceSquareTable.read(piece_type_moved, board.turn, move.to_square)
    # subtract position score of origin square
    score -= perspective * pos_score_scale_factor * PieceSquareTable.read(piece_type_moved, board.turn, move.from_square)

    # Check for capture
    if captured_type is not None:
        # small bug: we actually ignored en passant capture here, but that doesn't matter much
        score += 10 * eval_func.PIECE_VALUES[captured_type] - eval_func.PIECE_VALUES[piece_type_moved]
    # Add score for promotion
    if move.promotion is not None:
        score += eval_func.PIECE_VALUES[move.promotion]
    # Subtract score if square is attacked by pawns
    if board.attackers(not board.turn, move.to_square) & board.pawns:
        score -= eval_func.PIECE_VALUES[piece_type_moved] - eval_func.PIECE_VALUES[chess.PAWN]
    # Adjust the score by pawn advantage before returning
    return score / eval_func.PAWN_ADVANTAGE


def is_mate_in_one(board: chess.Board, move: chess.Move) -> bool:
    # make move, check if resulting position is checkmate, then unmake move and return result
    board.push(move)
    ret = board.is_checkmate()
    board.pop()
    return ret
