# Main file for chess_bots_project
# This project is based in command line interface
# May be migrating to web-based gui interface in the future

import sys
from playground.human_bot_interface import HumanBotInterface


if __name__ != "__main__":
    sys.exit()

my_interface = HumanBotInterface(fen="8/4k3/5r2/8/8/4BB2/4K3/8 w - - 0 1", human=False, bot="minimax")

my_interface.play()
