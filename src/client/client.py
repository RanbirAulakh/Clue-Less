import pika
import os
import sys
import inquirer
import enum

class Options(enum.Enum):
    CREATE_GAME = "Create a Clue-Less Game"
    FIND_GAME = "Find a Clue-Less Game"
    QUIT = "Exit Clue-Less Application"

class Client:
    player_name = ""

    def __init__(self):
        print("Welcome to Clue-Less (Text) Game!")

        player_name = inquirer.text(message="Please enter your username? ")
        print("Hello {0}".format(player_name))

        choices = inquirer.list_input("What would you like to do?", 
            choices=[Options.CREATE_GAME.value, Options.FIND_GAME.value, Options.QUIT.value])

        if Options.CREATE_GAME.value == choices:
            print(Options.CREATE_GAME.value)
        elif Options.FIND_GAME.value == choices:
            print("Me want to find a game")
        elif Options.QUIT.value == choices:
            print("Clue-Less is successfully closed.")
        else:
            print("Shouldn't reach here")

    def create_game(self):
        pass

    def client(self):
        pass
