"""
Implementation of transposition table
"""


import typing
import enum


class NodeType(enum.Enum):
    PV = 1  # these nodes contain exact score
    CUT = 2  # these nodes are lower bound of exact score
    ALL = 3  # these nodes contain upper bound of score


class MinimaxEntry(typing.NamedTuple):
    key: int
    score: float
    node_type: NodeType
    age: int


class TranspositionTable:
    def __init__(self, hasher):
        self.table = dict()
        self._hasher = hasher  # hasher is a Zobrist hash object. used to compute hashes

    def add(self, hash_key, score, node_type, move_number):
        # right now, we automatically replace entry when hash collision occurs
        self.table[hash_key] = MinimaxEntry(hash_key, score, node_type, move_number)
