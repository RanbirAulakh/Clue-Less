# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

from .room import *
from . import constants

class Map :
	def __init__(self):
		self.rooms = []
		self.setup_rooms()

	def setup_rooms(self):
		s_li_hallway = Hallway(constants.STUDY_LIBRARY)
		li_c_hallway = Hallway(constants.LIBRARY_CONSERVATORY)
		c_ba_hallway = Hallway(constants.CONSERVATORY_BALLROOM)
		ba_k_hallway = Hallway(constants.BALLROOM_KITCHEN)
		d_k_hallway = Hallway(constants.DINING_KITCHEN)
		d_lo_hallway = Hallway(constants.LOUNGE_DINING)
		h_lo_hallway = Hallway(constants.HALL_LOUNGE)
		ba_bi_hallway = Hallway(constants.BILLIARD_BALLROOM)
		li_bi_hallway = Hallway(constants.LIBRARY_BILLIARD)
		bi_d_hallway = Hallway(constants.BILLIARD_DINING)
		h_bi_hallway = Hallway(constants.HALL_BILLIARD)
		s_h_hallway = Hallway(constants.STUDY_HALL)
		study = Room(constants.STUDY)
		hall = Room(constants.HALL)
		library = Room(constants.LIBRARY)
		lounge = Room(constants.LOUNGE)
		dining_room = Room(constants.DINING)
		kitchen = Room(constants.KITCHEN)
		ballroom = Room(constants.BALLROOM)
		conservatory = Room(constants.CONSERVATORY)
		billiard_room = Room(constants.BILLIARD)
		s_li_hallway.add_connections(study)
		s_li_hallway.add_connections(library)
		li_c_hallway.add_connections(library)
		li_c_hallway.add_connections(conservatory)
		c_ba_hallway.add_connections(conservatory)
		c_ba_hallway.add_connections(ballroom)
		ba_k_hallway.add_connections(ballroom)
		ba_k_hallway.add_connections(kitchen)
		d_k_hallway.add_connections(kitchen)
		d_k_hallway.add_connections(dining_room)
		d_lo_hallway.add_connections(dining_room)
		d_lo_hallway.add_connections(lounge)
		h_lo_hallway.add_connections(hall)
		h_lo_hallway.add_connections(lounge)
		ba_bi_hallway.add_connections(ballroom)
		ba_bi_hallway.add_connections(billiard_room)
		li_bi_hallway.add_connections(library)
		li_bi_hallway.add_connections(billiard_room)
		bi_d_hallway.add_connections(billiard_room)
		bi_d_hallway.add_connections(dining_room)
		h_bi_hallway.add_connections(hall)
		h_bi_hallway.add_connections(billiard_room)
		s_h_hallway.add_connections(study)
		s_h_hallway.add_connections(hall)
		study.add_connections(s_li_hallway)
		study.add_connections(s_h_hallway)
		study.add_connections(billiard_room)
		hall.add_connections(s_h_hallway)
		hall.add_connections(h_bi_hallway)
		hall.add_connections(h_lo_hallway)
		lounge.add_connections(billiard_room)
		lounge.add_connections(h_lo_hallway)
		lounge.add_connections(d_lo_hallway)
		library.add_connections(s_li_hallway)
		library.add_connections(li_bi_hallway)
		library.add_connections(li_c_hallway)
		billiard_room.add_connections(li_bi_hallway)
		billiard_room.add_connections(ba_bi_hallway)
		billiard_room.add_connections(bi_d_hallway)
		billiard_room.add_connections(h_bi_hallway)
		dining_room.add_connections(bi_d_hallway)
		dining_room.add_connections(d_k_hallway)
		dining_room.add_connections(d_lo_hallway)
		conservatory.add_connections(li_c_hallway)
		conservatory.add_connections(billiard_room)
		conservatory.add_connections(c_ba_hallway)
		ballroom.add_connections(c_ba_hallway)
		ballroom.add_connections(ba_bi_hallway)
		ballroom.add_connections(ba_k_hallway)
		kitchen.add_connections(ba_k_hallway)
		kitchen.add_connections(billiard_room)
		kitchen.add_connections(d_k_hallway)
		# easier to lookup rooms with a map so we can set starting positions
		self.rooms = {
			constants.STUDY : study,
			constants.HALL : hall,
			constants.LOUNGE : lounge,
			constants.LIBRARY : library,
			constants.BILLIARD : billiard_room,
			constants.DINING : dining_room,
			constants.CONSERVATORY : conservatory,
			constants.BALLROOM : ballroom,
			constants.KITCHEN : kitchen,
			constants.BILLIARD_DINING : bi_d_hallway,
			constants.DINING_KITCHEN : d_k_hallway,
			constants.STUDY_HALL : s_h_hallway,
			constants.STUDY_LIBRARY : s_li_hallway,
			constants.HALL_LOUNGE : h_lo_hallway,
			constants.HALL_BILLIARD : h_bi_hallway,
			constants.LIBRARY_BILLIARD : li_bi_hallway,
			constants.CONSERVATORY_BALLROOM : c_ba_hallway,
			constants.BILLIARD_BALLROOM : ba_bi_hallway,
			constants.BALLROOM_KITCHEN : ba_k_hallway,
			constants.LIBRARY_CONSERVATORY : li_c_hallway,
			constants.LOUNGE_DINING : d_lo_hallway
		}
		
	def get_rooms(self):
		return self.rooms

#m = Map()
#print(m.get_rooms())
#print(m.get_rooms()[constants.STUDY])
#print(m.get_rooms()[constants.STUDY].get_name())
#print(m.get_rooms()[constants.STUDY].get_connections())
