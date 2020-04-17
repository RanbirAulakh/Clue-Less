class Room():
	def __init__(self, roomName):
		self.name = roomName
		self.connections = []
		self.players = []
		self.maxplayers = 8


	def setConnections(self, room):
		self.connections = self.connections.add(room)

	def setPlayers(self, newplayers):
		self.players = newplayers

	def getMaxPlayers(self):
		return self.maxplayers

	def getPlayers(self):
		return self.players

	def getConnections(self):
		return self.connections

	def getName(self):
		return self.name

	def canGuess(self):
		return True

class Hallway(Room):
	def canGuess(self):
		return False
	def getMaxPlayers(self):
		return 1
