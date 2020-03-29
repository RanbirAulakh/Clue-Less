import constants
import random
from player import Player
import room
from clue import Clue
import map

class Game():
	def __init__(self, id, players):
		#create decks of the different clue types
		suspects = self.createSuspectDeck(constants.SUSPECTS)
		weapons = self.createWeaponsDeck(constants.WEAPONS)
		rooms = self.createRoomsDeck(constants.ROOMS)
		# draw 1 from each and store it as the murder you are solving
		storedMurder = self.createMurder(suspects, rooms, weapons)
		#combine the decks then deal to the players)
		clueDeck = suspects + weapons + rooms
		random.shuffle(clueDeck)
		numPlayers = len(players)
		self.dealHands(players,clueDeck)
		pass
		
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
	
testPlayer1 = Player("test")
testPlayer2 = Player("test2")
Object = Game("id",[testPlayer1, testPlayer2])
print("\n")
thing=Object.getMurder()
for i in testPlayer1.getHand():
	print("Player 1 : " + i.getClueName())
for i in testPlayer2.getHand():
	print("Player 2 : " + i.getClueName())