"""
Object representing human agent
"""

from ..agents import Agent
import sys
import chess


class HumanAgent(Agent):
    def __init__(self):
        super().__init__()

    # Inherited abstract method
    def get_move(self, board_str):

        return self._current_move

    @staticmethod
    def get_command():
        print("Enter a command: ", end="")
        cmd = input()
        return cmd

    def set_move(self, move):

    """
    HELPER FUNCTIONS
    """
