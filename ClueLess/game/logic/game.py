# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

# import constants
import logging
from . import constants
import random
from .player import Player
from .room import *
from .clue import Clue
from .map import Map


class Game():
	def __init__(self):
		"""
		TODO Random characters for each player or initialize the players out of initial game?
		"""
		print("Creating a game")

		self.players = []
		self.murder = []

		# create decks of the different clue types
		suspects = self.createSuspectDeck(constants.SUSPECTS)
		weapons = self.createWeaponsDeck(constants.WEAPONS)
		rooms = self.createRoomsDeck(constants.ROOMS)

		# draw 1 from each and store it as the murder you are solving
		self.createMurder(suspects, rooms, weapons)

		# combine the decks then deal to the players
		clueDeck = suspects + weapons + rooms
		random.shuffle(clueDeck)

		#numPlayers = len(players) // TODO move to another function
		#self.dealHands(players, clueDeck) // TODO move to another function

		self.map = Map()

	def add_player(self, player_name, chosen_character):
		for i in self.players:
			if i.name == player_name:
				print("Player {0} already exist!".format(player_name))
				return

		p = Player(player_name, chosen_character)
		print("Adding {0} to the game.".format(i.name))
		self.players.append(p)

	def remove_player(self, player_name):
		for i in self.players:
			if i.name == player_name:
				print("Removing {0} from the game.".format(i.name))
				self.players.remove(i)
				break
		
	# create individual decks for the creation of the muder
	def createSuspectDeck(self, suspects):
		clues = []
		for i in suspects:
			clues.append(Clue(i, "Suspect"))
		return clues 
		
	def createWeaponsDeck(self, weapons):
		clues = []
		for i in weapons:
			clues.append(Clue(i, "Weapon"))
		return clues 
		
	def createRoomsDeck(self, rooms):
		clues = []
		for i in rooms:
			clues.append(Clue(i, "Room"))
		return clues 
		
	# Shuffle and use the individual decks to put together the murder to be solved.
	def createMurder(self, suspectClues, roomClues, weaponClues):
		self.murder = []
		random.shuffle(suspectClues)
		random.shuffle(roomClues)
		random.shuffle(weaponClues)
		self.murder.append(suspectClues.pop())
		self.murder.append(roomClues.pop())
		self.murder.append(weaponClues.pop())

		print("MURDER SUSPECT: {0} / ROOM: {1} / WEAPON: {2}".format(self.murder[0].name, self.murder[1].name, self.murder[2].name))
		
	def getMurder(self):
		return self.murder
		
	"""
	Deal initial hands, and if a player leaves, place their hand in the "clueDeck" var
	and pass it to remaining players.
	"""
	def deal_hands(self, players, clue_deck):
		num_players = len(players)
		if len(self.players) == 3: # TODO change to 4
			rounds = 0
			while len(clue_deck) != 0:
				players[rounds % num_players].getHand().append(clue_deck.pop())
				rounds += 1

	def getMap(self):
		return self.map
	
	def makeTurnOrder(self, players) :
		turnOrder = []
		for i in constants.SUSPECTS :
			for ii in players :
				if ii.getCharacter().lower() == i.lower() :
					turnOrder.append(ii)
		return turnOrder
		
	def getTurnOrder(self) :
		return self.turnOrder
		
