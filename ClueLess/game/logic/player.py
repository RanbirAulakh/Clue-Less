class Player():
	def __init__(self, name, character):
		self.name = name
		self.character = character
		self.hand = []
		self.seen = []
		self.current_location = ""
		
	def get_hand(self):
		return self.hand

	def get_hand_str(self):
		lst = []
		for i in self.hand:
			lst.append(i.name)

		return lst
		
	def get_name(self):
		return self.name
		
	def append_seen(self, clue):
		self.seen.append(clue)
	
	def get_seen(self):
		return self.seen
		
	def get_character(self):
		return self.character
