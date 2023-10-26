# Bot that plays randomly. For testing purposes

from ..agents import Agent
import chess
import random


class RandomBot(Agent):
    def __init__(self):
        super().__init__()
        self._latest_legal_move_lst = None

    # Generates a random move to play
    def get_move(self, board_str):
        if self._latest_legal_move_lst is None:
            print("\n*** INTERNAL ERROR: Random bot needs list of legal moves ***\n")
            return None
        legal_move_lst = self._latest_legal_move_lst
        index = random.randint(0, len(legal_move_lst) - 1)
        self._latest_move = legal_move_lst[index]
        # reset legal move list to None now that we're done with it
        self._latest_legal_move_lst = None
        return self._latest_move
