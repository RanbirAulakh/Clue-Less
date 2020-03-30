class Room:
	def __init__(self, roomName, roomConnections):
		self.name = roomName
		self.connections = roomConnections
		
	def getConnections(self):
		return self.connections
		
	def getName(self):
		return self.name
		
	def canGuess(self):
		return True
		
class Hallway(Room):
	def canGuess(self):
		return False
