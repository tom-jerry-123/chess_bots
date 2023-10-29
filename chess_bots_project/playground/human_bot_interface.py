

from agents.human_agent import HumanAgent
from agents.random_bot import (RandomBot)
from .game import ChessGame
import chess
import sys


class HumanBotInterface:
    def __init__(self, human=chess.WHITE, bot="random"):
        self._game = ChessGame()
        self._human = human
        self._white = None
        self._black = None
        if human == chess.WHITE:
            self._white = HumanAgent()
            self._black = RandomBot()
        else:
            self._white = RandomBot()
            self._black = HumanAgent()

    def play(self):
        self._print_init_menu()
        while self._game.get_result() is None:
            if self._game.get_turn() == chess.WHITE:
                move = self._white.get_move(self._game.get_board())
                self._game.make_move(move)
                print(f"*** '{self._white.get_name()}' made move '{move.uci()}' ***")
            else:
                move = self._black.get_move(self._game.get_board())
                self._game.make_move(move)
                print(f"*** '{self._black.get_name()}' made move '{move.uci()}' ***")
            print("*** New Board ***")
            self._game.print_board()


    def _print_init_menu(self):
        player = "WHITE" if self._human else "BLACK"
        bot_agent = self._black if self._human else self._white
        print(f"You are playing {player} against bot '{bot_agent.get_name()}'!")
        print("*** Starting Position ***")
        self._game.print_board()
