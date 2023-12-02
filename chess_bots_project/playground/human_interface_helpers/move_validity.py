"""
File containing helper methods to check validity of human-entered move
"""

import chess
from enum import Enum, auto


class MoveStatus(Enum):
    """
    MoveStatus
    Used to encapsulate validity of move string (and also what notation it is in)
    """
    UNKNOWN = auto()
    SAN = auto()
    UCI = auto()
    INVALID = auto()
    ILLEGAL_SAN = auto()
    AMBIGUOUS_SAN = auto()
    ILLEGAL_UCI = auto()


def check_move_validity(_board: chess.Board, move_str: str) -> MoveStatus:
    """
    Trusted Function: You can safely pass your chess board to this function
    """
    status = None
    # first, see if move is valid in SAN
    try:
        _board.parse_san(move_str)
        print(f"*** Successfully parsed move '{move_str}' ***")
        status = MoveStatus.SAN
    except chess.InvalidMoveError:
        status = MoveStatus.INVALID
    except chess.IllegalMoveError:
        status = MoveStatus.ILLEGAL_SAN
    except chess.AmbiguousMoveError:
        status = MoveStatus.AMBIGUOUS_SAN

    if status == MoveStatus.INVALID:
        # check if move is valid in UCI
        try:
            _board.parse_uci(move_str)
            print(f"*** Successfully parsed move '{move_str}' ***")
            status = MoveStatus.UCI
        except chess.InvalidMoveError:
            status = MoveStatus.INVALID
        except chess.IllegalMoveError:
            status = MoveStatus.ILLEGAL_UCI

    return status


def process_move_str(board: chess.Board, move_str: str) -> chess.Move | None:
    """
    First, checks the validity of the move, returning a move status
    Then, gives error message (and return None) if move invalid; returns the move if it is valid
    """
    status = check_move_validity(board, move_str)
    # set move if move is valid, else give error message
    if status.value == MoveStatus.SAN.value:
        return board.parse_san(move_str)
    elif status.value == MoveStatus.UCI.value:
        return board.parse_uci(move_str)
    elif status.value == MoveStatus.ILLEGAL_SAN.value or status.value == MoveStatus.ILLEGAL_UCI.value:
        print(f"*** Error: Move '{move_str}' is illegal! Please try another move, or enter a valid command! ***")
    elif status.value == MoveStatus.AMBIGUOUS_SAN.value:
        print(f"*** Error: Move '{move_str}' is ambiguous in SAN. Please try another move or command! ***")
    else:
        print(f"*** Error: Move / Command '{move_str}' is not recognized. Please try a valid one! ***")

    return None
