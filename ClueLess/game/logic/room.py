"""
Since accusations can be made anywhere, no real reason to have it as a method, but guesses(suggestions?) can only be made in
main rooms.
"""

class Room:
	def __init__(self, roomName, roomConnections):
		self.name = roomName
		self.connections = roomConnections
		self.players=[]
		
	def getConnections(self):
		return self.connections
		
	def getName(self):
		return self.name
		
	def canGuess(self):
		return True
		
	def canMove(self):
		return True
		
	def addPlayer(self, player):
		self.players.append(player)
		
class Hallway(Room):
	def canGuess(self):
		return False
		
	def canMove(self):
		return len(self.players) == 0
