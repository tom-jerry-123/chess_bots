"""
Bot using Monte Carlo Tree Search

Algorithm:
* See paper *
"""

import chess
from playground.read_only_board import ReadOnlyBoard
from playground.hash_board import HashBoard
from agents import Agent
from agents.evaluation import eval_func
from agents.search.zobrist_hash import ZobristHash
from agents.search.hash_tree import HashTree

import random
import math
from timeit import default_timer  # For runtime profiling


class MonteCarloBot(Agent):
    def __init__(self, name="mtcs_bot"):
        super().__init__(name)
        self._num_pos_searched = 0
        self._zobrist_hasher = ZobristHash()
        self._game_tree = HashTree(self._zobrist_hasher)
        self._cur_transposition_cnt = 0

    def get_move(self, read_only_board: ReadOnlyBoard) -> chess.Move:
        self._num_pos_searched = 0
        # Get start time
        start_time = default_timer()

        hash_board = HashBoard(read_only_board.get_copy(), hasher=self._zobrist_hasher)
        root_key = hash_board.get_position_hash()
        # Now, run MTCS
        self.run_mtcs(hash_board=hash_board, root_key=root_key, num_sim=1000)

        best_move, best_eval = self.find_best_move_and_eval(hash_board)
        duration = default_timer() - start_time

        # Print num pos searched
        print(f"***\n'{self.get_name()}' searched through {self._num_pos_searched} positions. Best eval: {best_eval}.")
        print("***")
        # Print time taken
        print(f"### SYS INFO: time taken for move generation: {duration} ###")
        return best_move

    def run_mtcs(self, hash_board: HashBoard, root_key, num_sim=1000):
        self._game_tree.cur_root_key = root_key

        # Now, run mtcs 4-step process num_sim times
        for i in range(num_sim):
            self.recursive_tree_search(hash_board)

    def recursive_tree_search(self, hash_board: HashBoard):
        """
        Current code is VERY inefficient
        """
        key = hash_board.get_position_hash()
        ply_cnt = hash_board.ply()
        is_white = hash_board.turn()
        # node: current node we are at
        node = self._game_tree.get(key)
        if node is None:
            # If node is not on the tree, add to tree, make static eval, compute param, return
            # add one to the count of nodes
            self._num_pos_searched += 1

            self._game_tree.add(key, ply_cnt)
            node = self._game_tree.get(key)
            outcome = hash_board.outcome()
            if outcome is not None:
                if hash_board.get_shallow_copy().is_checkmate():
                    node.param = (1.0, 2 * eval_func.CHECKMATE_SCORE)
                    node.outcome_score = 0
                else:
                    node.param = (2 * eval_func.CHECKMATE_SCORE, 2 * eval_func.CHECKMATE_SCORE)
                    node.outcome_score = 0.5
            else:
                perspective = 1 if is_white else -1
                pawn_advantage = perspective * eval_func.evaluate(hash_board.get_shallow_copy())
                node.update_param_from_score(pawn_advantage)
            return

        move_chosen = None
        resulting_key = None
        thompson_sample = -1
        # Select next state to explore from all legal moves
        for move in hash_board.legal_moves():
            # naive and VERY inefficient implementation: we make and unmake each move
            # make the move
            hash_board.make_move(move)
            child = self._game_tree.get(hash_board.get_position_hash())
            if child is None:
                cur_sample = node.sample()
                if cur_sample > thompson_sample:
                    thompson_sample = cur_sample
                    move_chosen = move
                    resulting_key = hash_board.get_position_hash()
            elif child.outcome_score is None:
                # we take advantage of the fact that beta(a, b) = 1 - beta(b, a)
                cur_sample = 1 - child.sample()
                if cur_sample > thompson_sample:
                    thompson_sample = cur_sample
                    move_chosen = move
                    resulting_key = hash_board.get_position_hash()
            # undo it
            hash_board.undo_move()

        if move_chosen is None:
            move_lst = list(hash_board.legal_moves())
            random.shuffle(move_lst)
            move_chosen = move_lst[0]

        # Make move on board, explore node (call func), then undo move
        hash_board.make_move(move_chosen)
        # Win rate returned is next opp's win rate, so win rate for us should be 1 minus that.
        self.recursive_tree_search(hash_board)
        # Now that we searched the child, add it to the list of children
        if self._game_tree.get(resulting_key) is not None:
            node.children[move_chosen] = resulting_key
        hash_board.undo_move()

        # Perform appropriate back-prop. We first greedily choose the best move as the move that will be played
        # Then, we add the win rate (from our perspective) that will be provided by the best move
        # Note that we DO NOT care about what the best move is here
        best_child_win_rate = node.win_rate_from_param()
        for move, child_key in node.children.items():
            # we need to "negate" the win rate as it is
            cur_win_rate = 1 - self._game_tree.get(child_key).win_rate_from_param()
            best_child_win_rate = max(cur_win_rate, best_child_win_rate)
        if best_child_win_rate == 1:
            # that means we have forced checkmate
            node.outcome_score = 1
        elif best_child_win_rate == 0:
            # that means opponent has forced checkmate
            node.outcome_score = 0
        else:
            node.update_param_from_win_rate(best_child_win_rate)

    def find_best_move_and_eval(self, hash_board: HashBoard) -> (chess.Move, float):
        # COMPLETE FUNCTION: returns best move in given position
        best_move = chess.Move.null()
        best_expectation = -1
        best_eval = -math.inf  # this eval is not static, but taken from perspective of the current player
        node = self._game_tree.get(hash_board.get_position_hash())
        if node is None:
            raise RuntimeError("Node doesn't exist in tree. Build Tree first!")

        move_lst = list(hash_board.legal_moves())
        random.shuffle(move_lst)

        for move in move_lst:
            child_key = node.children.get(move, None)
            if child_key is None:
                cur_expectation = node.expectation()
                if cur_expectation > best_expectation:
                    best_move = move
                    best_expectation = cur_expectation
                    best_eval = node.pawn_advantage()
            else:
                # Remember to do 1 - W b/c win rate of W for opp means win rate of 1 - W for us
                cur_expectation = 1 - self._game_tree.get(child_key).expectation()
                if cur_expectation > best_expectation:
                    best_move = move
                    best_expectation = cur_expectation
                    # remember to negate as bad position for opp is good for us
                    best_eval = -(self._game_tree.get(child_key)).pawn_advantage()

        perspective = 1 if hash_board.turn() else -1

        return best_move, perspective * best_eval
