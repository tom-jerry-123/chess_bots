

import chess
from enum import Enum, auto


class MoveStatus(Enum):
    UNKNOWN = auto()
    SAN = auto()
    UCI = auto()
    INVALID = auto()
    ILLEGAL_SAN = auto()
    AMBIGUOUS_SAN = auto()
    ILLEGAL_UCI = auto()


class ReadOnlyBoard:
    def __init__(self, board=chess.Board()):
        self._board = board

    def get_turn(self):
        return self._board.turn

    def get_legal_moves(self):
        return self._board.legal_moves

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
