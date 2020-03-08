class Player:
	
	def __init__(self, name):
		self.name = name
		self.clues = []
		
	def add_clue(self, clue):
		self.clues.append(clue)