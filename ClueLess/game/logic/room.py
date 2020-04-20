class Room:
	def __init__(self, room_name):
		self.name = room_name
		self.connections = []
		self.players = []

	def add_connections(self, room):
		self.connections.append(room)

	def add_player(self, player):
		self.players.append(player)
		
	def remove_player(self, player):
		self.players.remove(player)

	def get_players(self):
		return self.players

	def get_connections(self):
		return self.connections

	def get_name(self):
		return self.name

	def can_guess(self):
		return True
		
	def can_move(self):
		return True


class Hallway(Room):
	def can_guess(self):
		return False

	def can_move(self):
		return len(self.get_players) == 0
