import constants
import random
import player
import room
import clue
import map

class Game():
	def __init__(self, id, players):
		#create decks of the different clue types
		suspects = createSuspectDeck(constants.SUSPECTS)
		weapons = createWeaponsDeck(constants.WEAPONS)
		rooms = createRoomsDeck(constants.ROOMS)
		# draw 1 from each and store it as the murder you are solving
		storedMurder = createMurder(suspects, rooms, weapons)
		#combine the decks then deal to the players)
		clueDeck = random.shuffle(suspects + weapons + rooms)
		pass
		
	def createSuspectDeck(suspects):
		for i in suspects :
			clue.__init__(i, "Suspect")
		pass
		
	def createWeaponsDeck(weapons):
		pass
		
	def createRoomsDeck(rooms):
		pass
		
	def createMurder(suspectClues, roomClues, weaponClues):
		pass
	
	