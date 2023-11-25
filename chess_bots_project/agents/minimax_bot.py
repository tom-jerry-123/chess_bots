# Implementation file for minimax bot

import chess
from playground.read_only_board import ReadOnlyBoard
from agents import Agent
from agents.evaluation import eval_func
import math
from timeit import default_timer


class MinimaxBot(Agent):
    """
    Functions
    minimax(chess.Board, alpha: float, beta: float, depth: int) -> float
    get_o
    """
    def __init__(self, name="conventional_bot"):
        super().__init__(name)
        self._num_pos_searched = 0
        self._opp_pawn_attacks = None

    def get_move(self, read_only_board: ReadOnlyBoard):
        self._num_pos_searched = 0
        # Get start time
        start_time = default_timer()
        position = read_only_board.get_copy()
        bot_color = position.turn
        best_eval = -math.inf if bot_color == chess.WHITE else math.inf
        best_move = chess.Move.null()
        move_lst = self._get_ordered_move_lst(position)
        # move_lst = position.legal_moves
        for move in move_lst:
            position.push(move)
            evaluation = self._minimax(position, depth=4)
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
        # Print time taken
        duration = default_timer() - start_time
        print(f"### SYS INFO: time taken for move generation: {duration} ###")
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
        move_lst = self._get_ordered_move_lst(board)
        # move_lst = board.legal_moves
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
                if best_evaluation >= beta:
                    # White to move, so black had a better option from another branch. Prune!
                    break
                alpha = max(alpha, evaluation)
        else:
            # Black's turn. We want to minimize score
            for move in move_lst:
                board.push(move)
                evaluation = self._minimax(board, depth=depth-1, alpha=alpha, beta=beta)
                board.pop()
                # check for best evaluation
                best_evaluation = min(best_evaluation, evaluation)
                if best_evaluation <= alpha:
                    # Black to move, so white had a better option from another branch. Prune!
                    break
                beta = min(beta, evaluation)

        return best_evaluation

    """
    Helper Functions
    """
    def _get_ordered_move_lst(self, board: chess.Board):
        move_score_lst = []
        # self._compute_opp_pawn_attacks(board)
        for move in board.legal_moves:
            score = self._score_move(board, move)
            move_score_lst.append((move, score))
        move_score_lst.sort(key=lambda x: x[1], reverse=True)
        return [tup[0] for tup in move_score_lst]

    def _score_move(self, board: chess.Board, move: chess.Move):
        score = 0.0
        piece_type_moved = board.piece_type_at(move.from_square)
        captured_type = board.piece_type_at(move.to_square)
        # # add position score of destination square
        # score += abs(PieceSquareTable.read(piece_type_moved, board.turn, move.to_square))
        # # subtract position score of origin square
        # score -= abs(PieceSquareTable.read(piece_type_moved, board.turn, move.from_square))
        if captured_type is not None:
            # small bug: we actually ignored en passant capture here, but that doesn't matter much
            score += 10 * eval_func.PIECE_VALUES[captured_type] - eval_func.PIECE_VALUES[piece_type_moved]
        if move.promotion is not None:
            score += eval_func.PIECE_VALUES[move.promotion]
        # if move.to_square in self._opp_pawn_attacks:
        #     # we penalize moves to squares attacked by enemy pawns
        #     score -= eval_func.PIECE_VALUES[piece_type_moved]
        return score

    # Currently not used as it is too slow and doesn't help
    def _compute_opp_pawn_attacks(self, board: chess.Board):
        opp = not board.turn
        self._opp_pawn_attacks = set()
        for square in chess.SQUARES:
            # Check if any attackers to the square is an opponent pawn
            # Recall that board.attackers() and board.pawns return SquareSet, a bitmask of the 64 squares
            if board.attackers(opp, square) & board.pawns:
                self._opp_pawn_attacks.add(square)

    # use this to generate capture moves
    def _get_capture_moves(self, board: chess.Board):
        capture_moves = []
        for move in board.legal_moves:
            # if we made en passant capture or move to a square occupied by enemy piece, we made capture
            if board.is_en_passant(move) or board.piece_type_at(move.to_square) is not None:
                capture_moves.append(move)
        return capture_moves
