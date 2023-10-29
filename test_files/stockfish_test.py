

import chess
import chess.engine


def print_board(cur_board):
    print("*** Current Position ***")
    print(cur_board)
    print("************************")


def call_stockfish(board, depth=20):
    with chess.engine.SimpleEngine.popen_uci("C:/Users/jerry/libraries/stockfish/stockfish-windows-x86-64-avx2.exe") as engine:
        result = engine.play(board, chess.engine.Limit(depth=depth))
        score = result.info.get("score", None)
        return result.move, score


my_board = chess.Board("r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4")
# best_move, evaluation = call_stockfish(my_board)
best_move, evaluation = call_stockfish(my_board)

print_board(my_board)
print("Best move:", best_move)
print("Evaluation:", evaluation)
