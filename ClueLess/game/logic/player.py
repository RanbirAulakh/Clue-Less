class Player:
	def __init__(self, name, character):
		self.name = name
		self.character = character
		self.hand = []
		self.room = None
		self.current_location = ""
		
	def get_hand(self):
		return self.hand

	def get_hand_str(self):
		lst = []
		for i in self.hand:
			lst.append(i.name)

		return lst

	def disprove(self, hand):
		returnVal = []
		for card in self.hand:
			for proofcard in hand:
				if card.get_clue_name == proofcard.get_clue_name:
					returnVal.add(card)
		return returnVal
	
	def get_name(self):
		return self.name
		
	def get_character(self):
		return self.character
		
	def set_room(self, room):
		self.room = room
		
	def get_room(self):
		return self.room
		
	def get_current_location(self):
		return self.current_location
		
	def set_current_location(self, location):
		self.current_location = location
