

import chess
from playground.game import ChessGame
import playground.special_positions as FENS
from agents.minimax_bot import MinimaxBot


class BotInterface:
    def __init__(self, fen=FENS.STARTING_FEN):
        self._game = ChessGame(fen)
        self._white = MinimaxBot(name="White")
        self._black = MinimaxBot(name="Black")
        self._ply_cnt = 0

    def play(self, max_ply=300):
        if self._ply_cnt > max_ply:
            print("### ERROR: Played too many plies in game. Reset Game / start new one! ###")
        while self._game.get_outcome() is None and self._ply_cnt < max_ply:
            if self._game.get_turn() == chess.WHITE:
                move = self._white.get_move(self._game.get_board())
                self._game.make_move(move)
                print(f"*** '{self._white.get_name()}' made move '{move.uci()}' ***")
            else:
                move = self._black.get_move(self._game.get_board())
                self._game.make_move(move)
                print(f"*** '{self._black.get_name()}' made move '{move.uci()}' ***")
            self._game.print_board()
            self._ply_cnt += 1
