"""
Stockfish Bot
Current Version: 16
Makes api calls to compiled stockfish engine. Make sure you have stockfish installed before running this.
"""

from agents import Agent
import chess
import chess.engine

from playground.read_only_board import ReadOnlyBoard


class StockfishBot(Agent):
    """
    Literally, Stockfish 16

    Inherited Attributes
    name (str)                  : name of agent
    latest_move (chess.Move)    : latest move made by agent

    New Attribute(s)
    path (str)                  : path to stockfish executable

    Methods
    get_move                    : gets move that stockfish agent would make
    """
    def __init__(self):
        super().__init__("Stockfish 16")
        self._path = "C:/Users/jerry/libraries/stockfish/stockfish-windows-x86-64-avx2.exe"

    def get_move(self, read_only_board: ReadOnlyBoard):
        cur_board = read_only_board.get_copy()
        with chess.engine.SimpleEngine.popen_uci(self._path) as stockfish:
            result = stockfish.play(cur_board, chess.engine.Limit(depth=20))
            return result.move
