# Bot that plays randomly. For testing purposes

from agents import Agent
import chess
import random
from playground.read_only_board import ReadOnlyBoard


class RandomBot(Agent):
    def __init__(self):
        super().__init__("random bot")

    # Generates a random move to play
    def get_move(self, read_only_board: ReadOnlyBoard):
        legal_move_lst = list(read_only_board.get_legal_moves())
        index = random.randint(0, len(legal_move_lst) - 1)
        self._latest_move = legal_move_lst[index]
        return self._latest_move
