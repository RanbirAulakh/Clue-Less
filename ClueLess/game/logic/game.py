# # TODO implement Property (python3)
# # https://www.datacamp.com/community/tutorials/property-getters-setters
# =======
# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

# import constants
from . import constants
import random
from .player import Player
from .room import *
from .clue import Clue
from .map import Map

class Game():
	id = ""
	visibility = True
	created_by = ""
	private_key = ""
	def __init__(self, id, players, visibility, created_by, private_key=""):
		self.players = players
		"""
		Add game lookup by id?
		
		Random characters for each player or initialize the players out of initial game?
		"""
		#create decks of the different clue types
		suspects = self.create_suspect_deck(constants.SUSPECTS)
		weapons = self.create_weapons_deck(constants.WEAPONS)
		rooms = self.create_rooms_deck(constants.ROOMS)
		# draw 1 from each and store it as the murder you are solving
		self.create_murder(suspects, rooms, weapons)
		#combine the decks then deal to the players)
		clue_deck = suspects + weapons + rooms
		random.shuffle(clue_deck)
		self.deal_hands(players,clue_deck)
		
		self.id = id
		self.visibility = visibility
		self.created_by = created_by
		self.private_key = private_key
		self.map = Map()
		self.turn_order = self.make_turn_order(players)
		
		pass
		
	# create individual decks for the creation of the muder
	def create_suspect_deck(self, suspects):
		clues=[]
		for i in suspects :
			clues.append(Clue(i, "Suspect"))
		return clues 
		
	def create_weapons_deck(self, weapons):
		clues=[]
		for i in weapons :
			clues.append(Clue(i, "Weapon"))
		return clues 
		
	def create_rooms_deck(self, rooms):
		clues=[]
		for i in rooms :
			clues.append(Clue(i, "Room"))
		return clues 
		
	# Shuffle and use the individual decks to put together the murder to be solved.
	def create_murder(self, suspect_clues, room_clues, weapon_clues):
		murder = []
		random.shuffle(suspect_clues)
		random.shuffle(room_clues)
		random.shuffle(weapon_clues)
		murder.append(suspect_clues.pop())
		murder.append(room_clues.pop())
		murder.append(weapon_clues.pop())
		self.murder = murder
		
	def get_murder(self):
		return self.murder
		
	"""
	Deal initial hands, and if a player leaves, place their hand in the "clue_deck" var
	and pass it to remaining players.
	"""
	def deal_hands(self, players, clue_deck):
		num_players = len(players)
		rounds = 0
		while len(clue_deck) != 0 :
			players[rounds%num_players].get_hand().append(clue_deck.pop())
			rounds += 1

	def game_model(self):
		# responible for handling PLAYERS, RULES, ETC
		pass

	def convert_to_json(self):
		return { "id": self.id, "visibility": self.visibility, "created_by": self.created_by, "key": self.private_key}
			
	def get_map(self):
		return self.map
	
	def make_turn_order(self, players) :
		turn_order = []
		for i in constants.SUSPECTS :
			for ii in players :
				if ii.get_character().lower() == i.lower() :
					turn_order.append(ii)
		return turn_order
		
	def get_turn_order(self) :
		return self.turn_order
		
	def move_player(self, player, target_room):
		start_room = player.get_room()
		if(target_room in start_room.get_connections()):
			if(target_room.can_move()):
				start_room.remove_player(player)
				target_room.add_player(player)
				return True
			else:
				return False
		return False
		
	#assuming the the clues are strings in this case. could make a map of the clues
	#and pull them by name to do exact compares.
	def make_guess(self, guessing_player, clues):
		for player in self.players :
			if(guessing_player != player):
				for c in player.get_hand() :
					if (c.get_clue_name().lower() in clues) :
						return c
		#No clues found in other players hands	
		return None
	
	def make_accusation(self, clues):
		murder = self.get_murder()
		clue_names = []
		for m in murder:
			clue_names.append(m.get_clue_name().lower())
		
		for c in clues :
			#if even one of the clues is not in the murder clues, player loses
			if(c.get_clue_name().lower() not in clue_names):
				return False
		#if all of the passed in clues are in the murder clues, they win
		return True
					
				
