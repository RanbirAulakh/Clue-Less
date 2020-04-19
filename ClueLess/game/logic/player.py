class Player():
	def __init__(self, name, character):
		self.name = name
		self.character = character
		self.hand = []
		self.seen = []
		
	def getHand(self):
		return self.hand
		
	def getName(self):
		return self.name
		
	def appendSeen(self, clue):
		self.seen.append(clue)
	
	def getSeen(self):
		return self.seen
		
	def getCharacter(self):
		return self.character
