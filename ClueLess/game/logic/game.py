# # TODO implement Property (python3)
# # https://www.datacamp.com/community/tutorials/property-getters-setters
# =======
# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

# import constants
from . import constants
import random
from .player import Player
from .room import *
from .clue import Clue
from .map import Map

class Game():
	id = ""
	visibility = True
	created_by = ""
	private_key = ""
	def __init__(self, id, players, visibility, created_by, private_key=""):
		"""
		Add game lookup by id?
		
		Random characters for each player or initialize the players out of initial game?
		"""
		#create decks of the different clue types
		suspects = self.createSuspectDeck(constants.SUSPECTS)
		weapons = self.createWeaponsDeck(constants.WEAPONS)
		rooms = self.createRoomsDeck(constants.ROOMS)
		# draw 1 from each and store it as the murder you are solving
		self.createMurder(suspects, rooms, weapons)
		#combine the decks then deal to the players)
		clueDeck = suspects + weapons + rooms
		random.shuffle(clueDeck)
		numPlayers = len(players)
		self.dealHands(players,clueDeck)
		self.map = Map()
		
		self.id = id
		self.visibility = visibility
		self.created_by = created_by
		self.private_key = private_key
		
	# create individual decks for the creation of the muder
	def createSuspectDeck(self, suspects):
		clues=[]
		for i in suspects :
			clues.append(Clue(i, "Suspect"))
		return clues 
		
	def createWeaponsDeck(self, weapons):
		clues=[]
		for i in weapons :
			clues.append(Clue(i, "Weapon"))
		return clues 
		
	def createRoomsDeck(self, rooms):
		clues=[]
		for i in rooms :
			clues.append(Clue(i, "Room"))
		return clues 
		
	# Shuffle and use the individual decks to put together the murder to be solved.
	def createMurder(self, suspectClues, roomClues, weaponClues):
		murder = []
		random.shuffle(suspectClues)
		random.shuffle(roomClues)
		random.shuffle(weaponClues)
		murder.append(suspectClues.pop())
		murder.append(roomClues.pop())
		murder.append(weaponClues.pop())
		self.murder = murder
		
	def getMurder(self):
		return self.murder
		
	"""
	Deal initial hands, and if a player leaves, place their hand in the "clueDeck" var
	and pass it to remaining players.
	"""
	def dealHands(self, players, clueDeck):
		numPlayers = len(players)
		rounds = 0
		while len(clueDeck) != 0 :
			players[rounds%numPlayers].getHand().append(clueDeck.pop())
			rounds += 1

	def game_model(self):
		# responible for handling PLAYERS, RULES, ETC
		pass

	def convert_to_json(self):
		return { "id": self.id, "visibility": self.visibility, "created_by": self.created_by, "key": self.private_key}

# disabiling it for now
# testPlayer1 = Player("test", "green")
# testPlayer2 = Player("test2", "plum")
# HallTest = Hallway("hall",["1","2"])
# print(HallTest.canGuess())
# Object = Game("id",[testPlayer1, testPlayer2], True, "Player")
# print("\n")
# thing=Object.getMurder()
# for i in testPlayer1.getHand():
# 	print("Player 1 : " + i.getClueName())
# for i in testPlayer2.getHand():
# 	print("Player 2 : " + i.getClueName())
