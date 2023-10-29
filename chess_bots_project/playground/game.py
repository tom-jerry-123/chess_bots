"""
Class representing chess game.
"""
import chess
from .read_only_board import ReadOnlyBoard


class ChessGame:
    """
    Attributes
    name (str) = name of chess game
    _board (chess.Board) = Represents chess board for given game
    _white (agent) = agent representing white (human or bot)
    _black (agent) = agent representing black (human or bot)
    """
    WHITE_WIN = 1
    DRAW = 0
    BLACK_WIN = -1

    def __init__(self):
        self.name = "Unnamed Chess Game"
        self._board = chess.Board()
        self._result = None # MIGHT NOT USE THIS. May instead use python-chess game result methods

    '''
    OUTPUT FUNCTIONS
    '''
    def print_board(self):
        print(f"\n*** Printing board from '{self.name}'")
        print(self._board)
        print("\n")

    '''
    GETTER FUNCTIONS
    '''
    def get_turn(self):
        return self._board.turn

    def get_legal_moves(self):
        return list(self._board.legal_moves)

    def get_result(self):
        return self._result

    # Returns a read-only version of the current board
    def get_board(self):
        return ReadOnlyBoard(self._board)

    '''
    BOARD STATE INQUIRY METHODS
    Inquires about the state of the game
    '''
    #
    #

    '''
    BOARD ACTION METHODS
    Commits actions (make move, resign, draw)
    '''

    # Current player resigns. Is not currently implemented
    def resign(self):
        if self._result is not None:
            print("Game already ended. Can't resign now. Reset board for a new game first.")
            return
        if self._board.turn == chess.WHITE:
            self._result = self.BLACK_WIN
        else:
            self._result = self.WHITE_WIN

    # Draws the game. This is not currently implemented
    def draw(self):
        if self._result is not None:
            print("Game already ended. Can't draw now. Reset board for a new game first.")
            return
        self._result = self.DRAW

    # makes a move from chess.Move object.
    def make_move(self, move, check_validity=False):
        if not check_validity:
            self._board.push(move)
        elif self.check_move(move):
            self._board.push(move)

    # resets the game to starting position
    def reset_game(self):
        self._board.reset()

    '''
    HELPER FUNCTIONS
    These will probably not get used as they are no longer useful
    '''

    # check if string given (in UCI or SAN) is a legal move (and not null). If it is, return chess.Move object for move
    def parse_str_for_move(self, move_str, print_error=True):
        move = None
        invalid_san = False
        # first, see if move is valid in SAN
        try:
            move = self._board.parse_san(move_str)
        except chess.InvalidMoveError:
            invalid_san = True
        except chess.IllegalMoveError:
            if print_error:
                print(f"\n*** ERROR: '{move_str}' is an illegal move! Try entering a different move / command. ***\n")
        except chess.AmbiguousMoveError:
            if print_error:
                print(f"\n*** ERROR: '{move_str}' is ambiguous in the current position! Try a different move / command. ***\n")

        if invalid_san:
            # check if move is valid in UCI
            try:
                move = self._board.parse_uci(move_str)
            except chess.InvalidMoveError:
                if print_error:
                    print(f"\n*** ERROR: '{move_str}' is an unrecognized command / move. ***\n")
            except chess.IllegalMoveError:
                if print_error:
                    print(f"\n*** ERROR: '{move_str}' is an illegal move! Try another move / move_str. ***\n")

        return move

    # checks if a move is valid. Accepts only chess.Move arguments
    def check_move(self, move):
        return move in self._board.legal_moves
