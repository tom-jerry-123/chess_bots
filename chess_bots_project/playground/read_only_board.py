

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


class ReadOnlyBoard:
    """
    Read-Only version of chess.Board
    A wrapper for the actual game board with read-only access. Pass this wrapper of actual game board
    to agents that need board position. Ensures they won't change actual game board.

    Attribute(s)
    board (chess.Board) : (private) member element representing the chess board

    Methods
    (bool)          get_turn            : returns whose turn it is
    (legal_moves)   get_legal_moves     : returns the set of legal moves (not as a list)
    (chess.Board)   get_copy            : returns a copy of the board
    (None)          print_board         : prints current position
    (MoveStatus)    check_move_validity : returns validity of move string in form of MoveStatus object
    (chess.Move)    parse_san           : calls parse_san on the underlying board. Does NOT check move validity
    (chess.Move)    parse_uci           : calls parse_uci on the underlying board. Does NOT check move validity
    """
    def __init__(self, board=chess.Board()):
        self._board = board

    """
    chess.Board methods (does exactly the same thing as the chess.Board method of same name)
    """

    def get_turn(self):
        return self._board.turn

    # WARNING: this function returns legal_moves object, not a list
    def get_legal_moves(self):
        return self._board.legal_moves

    # Call this function to get copy of board.
    # Only do this when board needs to be manipulated or passed to engine
    def get_copy(self):
        return self._board.copy()

    """
    Other Methods
    """
    def print_board(self):
        print("*** Board ***")
        print(self._board)
        print()

    def check_move_validity(self, move_str: str) -> MoveStatus:
        status = None
        # first, see if move is valid in SAN
        try:
            self._board.parse_san(move_str)
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
                self._board.parse_uci(move_str)
                print(f"*** Successfully parsed move '{move_str}' ***")
                status = MoveStatus.UCI
            except chess.InvalidMoveError:
                status = MoveStatus.INVALID
            except chess.IllegalMoveError:
                status = MoveStatus.ILLEGAL_UCI

        return status

    # Accesses parse_san function of board. Should only be used after checking move is valid san
    def parse_san(self, valid_move_str):
        return self._board.parse_san(valid_move_str)

    def parse_uci(self, valid_move_str):
        return self._board.parse_uci(valid_move_str)
