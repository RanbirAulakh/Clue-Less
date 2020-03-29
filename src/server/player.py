class Player():
	def __init__(self, name):
		self.name = name
		self.hand = []
		
	def getHand(self):
		return self.hand