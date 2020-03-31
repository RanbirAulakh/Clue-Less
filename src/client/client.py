import pika
import os
import sys
from PyInquirer import prompt

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

        # self.player_name = inquirer.text(message="Please enter your username? ")
        questions = [{ 'type': 'input', 'name':'name', 'message':'Please enter your username?'}]
        self.player_name = prompt(questions)['name'];
        print("Hello {0}".format(self.player_name))

        self.main_menu_prompt()
    
    def main_menu_prompt(self):
        while(True):
            options = [{
                'type':'list',
                'name':'choices',
                'message':'What would you like to do?',
                'choices':[Options.CREATE_GAME.value, Options.FIND_GAME.value, Options.QUIT.value]
            }]
            choices = prompt(options)

            if Options.CREATE_GAME.value == choices['choices']:
                Game().create_game(self.player_name)
            elif Options.FIND_GAME.value == choices['choices']:
                Game().find_game()
            elif Options.QUIT.value == choices['choices']:
                print("Clue-Less is successfully closed.")
                sys.exit(0)
            else:
                print("Shouldn't reach here")
