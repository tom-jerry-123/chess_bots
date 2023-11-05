# Implementation file for minimax bot

import chess
from playground.read_only_board import ReadOnlyBoard
from agents import Agent
from agents import eval_func
import math


class MinimaxBot(Agent):
    """
    Functions
    minimax(chess.Board, alpha: float, beta: float, depth: int) -> float
    get_o
    """
    def __init__(self):
        super().__init__("conventional_bot")
        self._num_pos_searched = 0

    def get_move(self, read_only_board: ReadOnlyBoard):
        self._num_pos_searched = 0
        position = read_only_board.get_copy()
        bot_color = position.turn
        best_eval = -math.inf if bot_color == chess.WHITE else math.inf
        best_move = chess.Move.null()
        # move_lst = self._get_ordered_move_lst(position)
        move_lst = position.legal_moves
        for move in move_lst:
            position.push(move)
            evaluation = self._minimax(position, depth=5)
            position.pop()
            if bot_color == chess.WHITE:
                if evaluation > best_eval:
                    best_eval = evaluation
                    best_move = move
            else:
                if evaluation < best_eval:
                    best_eval = evaluation
                    best_move = move
        # Print num pos searched
        print(f"*** '{self.get_name()}' searched through {self._num_pos_searched} positions. Best eval: {best_eval}. ***")
        return best_move

    # Note: depth refers to number of plies (half-moves) to search.
    # By convention, black tries to minimize score; white, maximize
    """
    Minimax function
    """
    def _minimax(self, board: chess.Board, depth=5, alpha=-math.inf, beta=math.inf):
        if depth <= 0:
            # we hit maximum depth -> return evaluation
            self._num_pos_searched += 1
            return eval_func.evaluate(board)
        if board.outcome() is not None:
            # game has ended, evaluate position
            self._num_pos_searched += 1
            return eval_func.evaluate(board)

        best_evaluation = -math.inf if board.turn == chess.WHITE else math.inf
        # move_lst = self._get_ordered_move_lst(board)
        move_lst = board.legal_moves
        # what we do changes depending on who's turn it is
        if board.turn == chess.WHITE:
            # White's turn. We want to maximize
            for move in move_lst:
                # Evaluate move. Make move, evaluate, then unmake
                board.push(move)
                evaluation = self._minimax(board, depth=depth-1, alpha=alpha, beta=beta)
                board.pop()
                # Check for best evaluation
                best_evaluation = max(best_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    # White to move, so black had a better option from another branch. Prune!
                    break
        else:
            # Black's turn. We want to minimize score
            for move in move_lst:
                board.push(move)
                evaluation = self._minimax(board, depth=depth-1, alpha=alpha, beta=beta)
                board.pop()
                # check for best evaluation
                best_evaluation = min(best_evaluation, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    # Black to move, so white had a better option from another branch. Prune!
                    break

        self._num_pos_searched += 1
        return best_evaluation

    """
    Helper Functions
    """
    def _get_ordered_move_lst(self, board: chess.Board):
        move_score_lst = []
        for move in board.legal_moves:
            score = self._score_move(board, move)
            move_score_lst.append((move, score))
        move_score_lst.sort(key=lambda x: x[1], reverse=True)
        ret_lst = []
        for tup in move_score_lst:
            ret_lst.append(tup[0])
        return ret_lst

    def _score_move(self, board: chess.Board, move: chess.Move):
        score = 0.0
        start_sqr = move.from_square
        end_sqr = move.to_square
        if board.is_capture(move):
            # prioritize capturing most valuable piece with least valuable piece
            score += 10 * eval_func.PIECE_VALUES[board.piece_type_at(end_sqr)] - eval_func.PIECE_VALUES[board.piece_type_at(start_sqr)]
        if move.promotion is not None:
            score += eval_func.PIECE_VALUES[move.promotion]
        if board.gives_check(move):
            # prioritize checks with less valuable pieces. Divide by 2 b/c checks less important than capture
            score += (10 - eval_func.PIECE_VALUES[board.piece_type_at(start_sqr)]) / 2
        if end_sqr in self._opp_pawn_attacks(board):
            # we penalize moves to squares attacked by enemy pawns
            score -= eval_func.PIECE_VALUES[board.piece_type_at(start_sqr)]
        return score

    @staticmethod
    def _opp_pawn_attacks(board: chess.Board) -> set:
        opp = not board.turn
        attacked_squares = set()
        for square in chess.SQUARES:
            # Check if any attackers to the square is an opponent pawn
            # Recall that board.attackers() and board.pawns return SquareSet, a bitmask of the 64 squares
            if board.attackers(opp, square) & board.pawns:
                attacked_squares.add(square)
        return attacked_squares
