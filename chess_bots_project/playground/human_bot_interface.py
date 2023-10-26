

from ..agents.human_agent import HumanAgent
from ..agents.random_bot import RandomBot
from .game import ChessGame
import chess
import sys


class HumanBotInterface:
    def __init__(self, human=chess.WHITE, bot="random"):
        self._game = ChessGame()
        self._white = None
        self._black = None
        self._latest_move = None
        if human == chess.WHITE:
            self._white = HumanAgent()
            self._black = RandomBot()
        else:
            self._white = RandomBot()
            self._black = HumanAgent()

    def play(self):
        while self._game.get_result() is None:
            pass

    def run_user_menu(self):
        self._print_command_menu()
        print("Enter a command: ", end="")
        command = input()
        got_move = self._process_command(command)
        while not got_move:
            print("Enter a move, or a new command:")
            command = input()
            got_move = self._process_command(command)

    # prints menu options for user
    @staticmethod
    def _print_command_menu():
        print("*** Command Options ***")
        print("1. Enter a move (UCI or SAN string)")
        print("2. Resign (type 'resign' or '2')")
        print("3. UNDER CONSTRUCTION")
        print("4. Check position (type 'board' or '4')")
        print("5. Quit (type 'exit' or 'quit' or '5')")

    # Processes user command
    def _process_command(self, cmd):
        ret = False # False -> move was not successfully made

        player = "WHITE" if self._game.get_turn() == chess.WHITE else "BLACK"
        opponent = "BLACK" if self._game.get_turn() == chess.WHITE else "WHITE"

        if cmd == "exit" or cmd == "quit" or cmd == "5":
            print("Thanks for playing, bye!")
            sys.exit()
        elif cmd == "cmd":
            self._print_command_menu()
        elif cmd == "resign" or cmd == "2":
            print(f"\n*** {opponent} wins by resignation. ***\n", "Thanks for playing, bye!")
            sys.exit()
        elif cmd == "draw" or cmd == "3":
            print("Draw offers are currently not supported. Please try something else")
        elif cmd == "board" or cmd == "4":
            print("\n********\n", "Current position:")
            self._game.print_board()
            print("\n********\n")
        else:
            self._latest_move = self._game.parse_str_for_move(cmd)
            if self._latest_move is not None:
                ret = True
        return ret
