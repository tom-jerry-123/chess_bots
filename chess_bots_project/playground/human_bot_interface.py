

from agents.human_agent import HumanAgent
from agents.random_bot import (RandomBot)
from agents.stockfish import StockfishBot
from agents.minimax_bot import MinimaxBot
from .game import ChessGame
import chess
import sys


class HumanBotInterface:
    def __init__(self, fen=None, human=chess.WHITE, bot="random"):
        self._game = ChessGame(fen)
        self._human = human
        self._white = None
        self._black = None
        self._bot = RandomBot()
        if bot == "stockfish":
            self._bot = StockfishBot()
        elif bot == "minimax" or bot == "conventional":
            self._bot = MinimaxBot()
        if human == chess.WHITE:
            self._white = HumanAgent()
            self._black = self._bot
        else:
            self._white = self._bot
            self._black = HumanAgent()

    def play(self):
        self._print_init_menu()
        while self._game.get_outcome() is None:
            if self._game.get_turn() == chess.WHITE:
                move = self._white.get_move(self._game.get_board())
                self._game.make_move(move)
                print(f"*** '{self._white.get_name()}' made move '{move.uci()}' ***")
            else:
                move = self._black.get_move(self._game.get_board())
                self._game.make_move(move)
                print(f"*** '{self._black.get_name()}' made move '{move.uci()}' ***")
            self._game.print_board()
        self._print_result()

    def _print_init_menu(self):
        player = "WHITE" if self._human else "BLACK"
        bot_agent = self._black if self._human else self._white
        print(f"You are playing {player} against bot '{bot_agent.get_name()}'!")
        print("*** Starting Position ***")
        self._game.print_board()

    def _print_result(self):
        outcome = self._game.get_outcome()
        winner = outcome.winner
        termination = outcome.termination
        if winner is None:
            print(f"Game drawn by {termination}")
        elif winner == chess.WHITE:
            print(f"'{self._white.get_name()}' wins!")
        else:
            print(f"'{self._black.get_name()}' wins!")
