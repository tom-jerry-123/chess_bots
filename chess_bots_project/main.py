# Main file for chess_bots_project
# This project is based in command line interface
# May be migrating to web-based gui interface in the future

import sys
from playground.human_bot_interface import HumanBotInterface
from playground.bot_interface import BotInterface
import playground.special_positions as fens


if __name__ != "__main__":
    sys.exit()

my_interface = BotInterface()

my_interface.play(max_ply=200)
