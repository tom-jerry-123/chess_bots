

import chess
from playground.game import ChessGame
import playground.special_positions as FENS
from agents.minimax_bot import MinimaxBot
import chess.pgn
import datetime


class BotInterface:
    def __init__(self, fen=FENS.STARTING_FEN, file_path=""):
        self._game = ChessGame(fen)
        self._white = MinimaxBot(name="White")
        self._black = MinimaxBot(name="Black")
        self._ply_cnt = 0
        self._file_path = file_path

    def play(self, max_ply=100, write_to_pgn=False):
        if self._ply_cnt > max_ply:
            print("### ERROR: Played too many plies in game. Reset Game / start new one! ###")
        whose_turn = self._game.get_turn()
        print(f"*** Starting Position ({'WHITE' if whose_turn else 'BLACK'} to move)")
        self._game.print_board()
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
        # write game to pgn if mandated
        if write_to_pgn:
            pgn = self._game.get_pgn()
            pgn.headers["Event"] = "Bot Game"
            pgn.headers["Site"] = "DIY Chess Interface"
            pgn.headers["Date"] = str(datetime.datetime.now())
            pgn.headers["White"] = "Bot"
            pgn.headers["Black"] = "Bot"
            try:
                with open(self._file_path, "w", encoding="utf-8") as pgn_file:
                    pgn_file.write(str(pgn))
            except:
                print("### ERROR: attempt to write game to file went wrong! ###")
