class Room():
	def __init__(self, roomName):
		self.name = roomName
		self.connections = []
		self.players = []

	def addConnections(self, room):
		self.connections.append(room)

	def addPlayer(self, player):
		self.players.append(player)
		
	def removePlayer(self, player):
		self.players.remove(player)

	def getPlayers(self):
		return self.players

	def getConnections(self):
		return self.connections

	def getName(self):
		return self.name

	def canGuess(self):
		return True
		
	def canMove(self):
		return True


class Hallway(Room):
	def canGuess(self):
		return False
	def canMove(self):
		return len(self.getPlayers) == 0
