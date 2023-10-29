"""
Object representing human agent
"""

from agents import Agent
import sys
import chess
from playground.read_only_board import ReadOnlyBoard, MoveStatus


class HumanAgent(Agent):
    def __init__(self):
        super().__init__("human")

    # Inherited abstract method
    def get_move(self, read_only_board: ReadOnlyBoard) -> chess.Move:
        self._print_command_menu()
        print("Enter a command: ", end="")
        command = input()
        got_move = self._process_command(command, read_only_board)
        while not got_move:
            print("Enter a move, or a new command:")
            command = input()
            got_move = self._process_command(command, read_only_board)
        return self._latest_move

    @staticmethod
    def _print_command_menu():
        print("*** Command Options ***")
        print("1. Enter a move (UCI or SAN string)")
        print("2. Resign (type 'resign' or '2')")
        print("3. UNDER CONSTRUCTION")
        print("4. Check position (type 'board' or '4')")
        print("5. Quit (type 'exit' or 'quit' or '5')")

    # Processes user command
    def _process_command(self, cmd: str, read_only_board: ReadOnlyBoard) -> bool:
        ret = False  # False -> move was not successfully made

        player = "WHITE" if read_only_board.get_turn() == chess.WHITE else "BLACK"
        opponent = "BLACK" if read_only_board.get_turn() == chess.WHITE else "WHITE"

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
            read_only_board.print_board()
            print("\n********\n")
        else:
            status = read_only_board.check_move_validity(cmd)
            # set move if move is valid, else give error message
            if status.value == MoveStatus.SAN.value:
                self._latest_move = read_only_board.parse_san(cmd)
                ret = True
            elif status.value == MoveStatus.UCI.value:
                self._latest_move = read_only_board.parse_uci(cmd)
                ret = True
            elif status.value == MoveStatus.ILLEGAL_SAN.value or status.value == MoveStatus.ILLEGAL_UCI.value:
                print(f"*** Error: Move '{cmd}' is illegal! Please try another move, or enter a valid command! ***")
            elif status.value == MoveStatus.AMBIGUOUS_SAN.value:
                print(f"*** Error: Move '{cmd}' is ambiguous in SAN. Please try another move or command! ***")
            else:
                print(f"*** Error: Move / Command '{cmd}' is not recognized. Please try a valid command! ***")
        return ret