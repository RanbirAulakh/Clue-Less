import pika
import os
import sys
import inquirer
import enum
from .game import Game

class Options(enum.Enum):
    CREATE_GAME = "Create a Clue-Less Game"
    FIND_GAME = "Find a Clue-Less Game"
    QUIT = "Exit Clue-Less Application"

class Client:
    player_name = ""

    def __init__(self):
        print("Welcome to Clue-Less (Text) Game!")

        self.player_name = inquirer.text(message="Please enter your username? ")
        print("Hello {0}".format(self.player_name))

        self.main_menu_prompt()
    
    def main_menu_prompt(self):
        while(True):
            choices = inquirer.list_input("What would you like to do?", 
                choices=[Options.CREATE_GAME.value, Options.FIND_GAME.value, Options.QUIT.value])

            if Options.CREATE_GAME.value == choices:
                Game().create_game(self.player_name)
            elif Options.FIND_GAME.value == choices:
                Game().find_game()
            elif Options.QUIT.value == choices:
                print("Clue-Less is successfully closed.")
                sys.exit(0)
            else:
                print("Shouldn't reach here")
