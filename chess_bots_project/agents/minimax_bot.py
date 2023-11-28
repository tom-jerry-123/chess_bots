# Implementation file for minimax bot

import chess
from playground.read_only_board import ReadOnlyBoard
from agents import Agent
from agents.evaluation import eval_func
from agents.search.zobrist_hash import ZobristHash
from agents.search.transposition_table import TranspositionTable
from agents.evaluation.piece_square_table import PieceSquareTable
import math
from timeit import default_timer  # For runtime profiling


class MinimaxBot(Agent):
    """
    Functions
    minimax(chess.Board, alpha: float, beta: float, depth: int) -> float
    get_o
    """
    def __init__(self, name="conventional_bot"):
        super().__init__(name)
        self._num_pos_searched = 0
        self._zobrist_hasher = ZobristHash()
        self._transposition_table = TranspositionTable(self._zobrist_hasher)
        self._cur_transposition_cnt = 0
        self._opp_pawn_attacks = None

    def get_move(self, read_only_board: ReadOnlyBoard):
        self._num_pos_searched = 0
        # Get start time
        start_time = default_timer()
        position = read_only_board.get_copy()
        best_move, best_eval = self._search_for_moves(position, 5)
        # Print num pos searched
        print(f"*** '{self.get_name()}' searched through {self._num_pos_searched} positions. Best eval: {best_eval}. ***")
        # Print time taken
        duration = default_timer() - start_time
        print(f"### SYS INFO: time taken for move generation: {duration} ###")
        return best_move

    def _search_for_moves(self, board: chess.Board, search_depth=5) -> (chess.Move, float):
        if search_depth <= 0:
            search_depth = 1  # force set depth to at least one so we can

        bot_color = board.turn
        best_move = chess.Move.null()
        # Initialize alpha and beta for the mini / nega max search
        alpha = -math.inf
        move_lst = self._get_ordered_move_lst(board)
        # move_lst = board.legal_moves
        for move in move_lst:
            board.push(move)
            # remember to negate result of negamax as good pos for opp is bad for us.
            # Note: beta=-inf always at the lowest depth
            evaluation = -self._negamax(board, depth=search_depth-1, alpha=-math.inf, beta=-alpha)
            board.pop()
            if evaluation > alpha:
                alpha = evaluation
                best_move = move

        best_eval = alpha if bot_color else -alpha
        return (best_move, best_eval)

    # Note: depth refers to number of plies (half-moves) to search.
    # By convention, black tries to minimize score; white, maximize
    def _minimax(self, board: chess.Board, depth=5, alpha=-math.inf, beta=math.inf):
        """
        Minimax function (not used anymore)
        Now, we use negamax instead b/c code is cleaner
        """
        if depth <= 0:
            # we hit maximum depth -> return evaluation
            self._num_pos_searched += 1
            return eval_func.evaluate(board)
        if board.outcome() is not None:
            # game has ended, evaluate position
            self._num_pos_searched += 1
            return eval_func.evaluate(board)

        best_evaluation = -math.inf if board.turn == chess.WHITE else math.inf
        # I tested and found that move ordering makes things faster
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

    # negamax version of minimax algorithm
    def _negamax(self, board: chess.Board, depth=5, alpha=-math.inf, beta=math.inf):
        """
        Negamax version of minimax algorithm
        Evaluation is now defined to be positive if it is good for current player,
        so we don't need to check if player is maximizer or minimizer
        Param:
        board (chess.Board) : chess board position
        depth (int)         : positive int representing depth (num ply) left to search
        alpha (float)       : (positive) score of best eval for current player seen so far
        beta (float)        : (negative) score of worst eval for current player seen so far
        """
        if depth <= 0 or board.outcome() is not None:
            # we hit maximum depth -> return evaluation
            perspective = 1 if board.turn else -1
            self._num_pos_searched += 1
            return perspective * eval_func.evaluate(board)

        # I tested and found that move ordering makes things faster
        move_lst = self._get_ordered_move_lst(board)
        # move_lst = board.legal_moves
        for move in move_lst:
            # Evaluate move. Make move, evaluate, then unmake
            board.push(move)
            # we need to negate as what's good for opponent is bad for current player
            evaluation = -self._negamax(board, depth=depth - 1, alpha=-beta, beta=-alpha)
            board.pop()
            # Check for best evaluation
            if evaluation >= beta:
                # Move was too good! Opp will avoid this
                return beta
            alpha = max(alpha, evaluation)

        return alpha

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
        # Do not add this into the heuristic. Makes search a lot worse
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
