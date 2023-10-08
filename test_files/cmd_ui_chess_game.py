# Command line interface program for a chess game. Only supports human players


import chess
import sys


def print_command_menu():
    print("*** Command Options ***")
    print("1. Enter a move (UCI or SAN string)")
    print("2. Resign (type 'resign' or '2')")
    print("3. Offer draw (type 'draw' or '3')")
    print("4. Check position (type 'board' or '4')")
    print("5. Quit (type 'exit' or 'quit' or '5')")


def process_command(cmd):
    if cmd == "exit" or cmd == "quit" or cmd == "5":
        print("Thanks for playing, bye!")
        sys.exit()
    elif cmd == "cmd":
        print_command_menu()
    elif cmd == "resign" or cmd == "2":
        print(f"\n*** {opponent} wins by resignation. ***\n", "Thanks for playing, bye!")
        sys.exit()
    elif cmd == "draw" or cmd == "3":
        print(f"{player} offers a draw. Do you (as {opponent}), accept ('Y' or 'y' to accept, anything else to decline)?", end='')
        accept_draw = input()
        if accept_draw == 'Y' or accept_draw == 'y':
            print("\n*** Game drawn by agreement. ***\n", "Thank you for playing, bye!")
            sys.exit()
        else:
            print("Draw declined.")
    elif cmd == "board" or cmd == "4":
        print("\n********\n", "Current position:\n", board, "\n********\n")
    else:
        # then, we assume player wanted to enter a move. Check if move is valid, and reprompt until move is valid
        invalid_san = False
        try:
            move = board.parse_san(cmd)
            board.push(move)
            print(f"\n*** Made move '{cmd}' ***\n")
        except chess.InvalidMoveError:
            invalid_san = True
        except chess.IllegalMoveError:
            print(f"\n*** ERROR: '{cmd}' is an illegal move! Try entering a different move / command. ***\n")
        except chess.AmbiguousMoveError:
            print(f"\n*** ERROR: '{cmd}' is ambiguous in the current position! Try a different move / command. ***\n")

        if invalid_san:
            try:
                move = board.parse_uci(cmd)
                board.push(move)
                print(f"\n*** Made move '{cmd}' ***\n")
            except chess.InvalidMoveError:
                print(f"\n*** ERROR: '{cmd}' is an unrecognized command / move. ***\n")
            except chess.IllegalMoveError:
                print(f"\n*** ERROR: '{cmd}' is an illegal move! Try another move / cmd. ***\n")


# main program
board = chess.Board()
print("Created board with starting position")
print(board, end='\n\n')
print_command_menu()

while True:
    player = "WHITE" if board.turn == chess.WHITE else "BLACK"
    opponent = "WHITE" if board.turn != chess.WHITE else "BLACK"
    print(f"{player}'s turn.")
    print("Enter your command (or 'cmd' for command options): ", end='')
    command = input()
    process_command(command)
