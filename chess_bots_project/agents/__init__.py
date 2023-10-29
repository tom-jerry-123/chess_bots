"""
This Package contains all con
Includes:
Human Agent
Random Move Bot
Stockfish Bot, i.e. bot using stockfish api
Minimax Bot, Conventional Minimax Algo with heuristic eval function
"""

from abc import ABC, abstractmethod

import chess


# Interface for Agents
class Agent:
    def __init__(self, name=""):
        self._latest_move = chess.Move.null()
        self._name = name
    """
    Description
    Gets the agent's next move given the current position
    Args
    _board (chess.Board) = chess board of the current position. Should NOT be altered by program
    """
    @abstractmethod
    def get_move(self, board_str):
        pass

    def get_name(self):
        return self._name
