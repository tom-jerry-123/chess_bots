# Main file for chess_bots_project
# This project is based in command line interface
# May be migrating to web-based gui interface in the future

import sys
from playground.human_bot_interface import HumanBotInterface
from playground.bot_interface import BotInterface
import playground.special_positions as fens


if __name__ != "__main__":
    sys.exit()

# Bot vs. Bot
my_interface = BotInterface(fen=fens.STARTING_FEN, file_path="play_results/bot_game.pgn")
my_interface.play(max_ply=30 , write_to_pgn=True)

# # Human vs. Bot
# cmd_interface = HumanBotInterface(bot="minimax")
# cmd_interface.play()
