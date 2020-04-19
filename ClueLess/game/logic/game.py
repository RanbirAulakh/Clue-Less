# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

# import constants
import logging
from . import constants
import random
from .player import Player
from .room import *
from .clue import Clue
from .map import Map

class Game:
	def __init__(self):
		self.players = []
		self.murder = []

		"""
		TODO Random characters for each player or initialize the players out of initial game?
		"""
		# create decks of the different clue types
		suspects = self.create_suspect_deck(constants.SUSPECTS)
		weapons = self.create_weapons_deck(constants.WEAPONS)
		rooms = self.create_rooms_deck(constants.ROOMS)

		# draw 1 from each and store it as the murder you are solving
		self.create_murder(suspects, rooms, weapons)

		# combine the decks then deal to the players)
		clue_deck = suspects + weapons + rooms
		random.shuffle(clue_deck)

		self.map = Map()

		# self.turn_order = self.make_turn_order(players) # TODO move to another function

	def add_player(self, player_name):
		for i in self.players:
			if i.name == player_name:
				print("Player {0} already exist!".format(player_name))
				return

		p = Player(player_name, None)
		print("Adding {0} to the game.".format(p.name))
		self.players.append(p)

	def remove_player(self, player_name):
		for i in self.players:
			if i.name == player_name:
				print("Removing {0} from the game.".format(i.name))
				self.players.remove(i)
				break

	def deal_hands(self):
		pass
		# self.deal_hands(players,clue_deck) # TODO move to another function

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
		self.murder = []
		random.shuffle(suspect_clues)
		random.shuffle(room_clues)
		random.shuffle(weapon_clues)
		self.murder.append(suspect_clues.pop())
		self.murder.append(room_clues.pop())
		self.murder.append(weapon_clues.pop())

		print("MURDER SUSPECT: {0} / ROOM: {1} / WEAPON: {2}".format(self.murder[0].name, self.murder[1].name, self.murder[2].name))
		
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
