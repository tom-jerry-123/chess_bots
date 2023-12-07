"""
Similar to the Transposition Table; a transposition tree
Stores search tree for monte carlo
"""


import chess
import numpy as np
from scipy.stats import beta
import enum

from agents.search.zobrist_hash import ZobristHash
from agents.evaluation import eval_func


class TreeNode:
    LN_10 = np.log(10)

    def __init__(self, key, ply):
        self._key = key
        self.param = (1.0, 1.0)  # This stores parameters for the current player, NOT for white in general
        self.children = dict()  # Stores chess.Move, hash_key
        self.ply = ply
        # is_determined: i.e. no longer need to search this node AT ALL b/c we determined its eval for certain.
        # any node with node forced draw or checkmate is a determined state
        # including terminal states like checkmates or stalemates
        self.outcome_score = None

    def update_param_from_score(self, pawn_advantage: float):
        wins = self.win_rate_from_score(pawn_advantage)
        new_param = (self.param[0] + wins, self.param[1] + 1 - wins)
        self.param = new_param

    def update_param_from_win_rate(self, win_rate: float):
        new_param = (self.param[0] + win_rate, self.param[1] + 1 - win_rate)
        self.param = new_param

    def win_rate_from_score(self, pawn_advantage):
        if pawn_advantage > 10:
            return 0.9999
        elif pawn_advantage < -10:
            return 0.0001
        return 1/(1 + np.exp(-self.LN_10 * pawn_advantage / 4))

    def win_rate_from_param(self):
        if self.param[0] + self.param[1] - 2 <= 0:
            return 0.5
        return (self.param[0] - 1) / (self.param[0] + self.param[1] - 2)

    def pawn_advantage(self):
        if self.param[0] + self.param[1] - 2 <= 0:
            return 0.5
        win_rate = self.win_rate_from_param()
        if win_rate == 1:
            return eval_func.CHECKMATE_SCORE
        elif win_rate == 0:
            return -eval_func.CHECKMATE_SCORE
        return 4 * np.log10(win_rate / (1 - win_rate))

    def sample(self):
        # Returns a sample of the beta with laplace smoothing
        if self.outcome_score is not None:
            return self.outcome_score
        return beta.rvs(self.param[0] + 1, self.param[1] + 1)

    def expectation(self):
        if self.outcome_score is not None:
            return self.outcome_score
        return self.param[0] / (self.param[0] + self.param[1])


class HashTree:
    def __init__(self, hasher: ZobristHash):
        self.tree = dict()
        self._hasher = hasher
        self.cur_root_key = int

    def add(self, hash_key: int, ply_cnt: int):
        # right now, we automatically replace entry when hash collision occurs
        self.tree[hash_key] = TreeNode(hash_key, ply_cnt)

    def get(self, hash_key: int) -> TreeNode | None:
        return self.tree.get(hash_key, None)

    def size(self):
        return len(self.tree)
