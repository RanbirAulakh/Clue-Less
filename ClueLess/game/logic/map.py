# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

from .room import *
from . import constants

class Map :
	def __init__(self):
		self.rooms = []
		self.setupRooms()

	def setupRooms(self):
		SLHallway = Hallway(constants.STUDY_LIBRARY)
		LiCHallway = Hallway(constants.LIBRARY_CONSERVATORY)
		CBaHallway = Hallway(constants.CONSERVATORY_BALLROOM)
		BaKHallway = Hallway(constants.BALLROOM_KITCHEN)
		DKHallway = Hallway(constants.DINING_KITCHEN)
		DLoHallway = Hallway(constants.LOUNGE_DINING)
		HLoHallway = Hallway(constants.HALL_LOUNGE)
		BaBiHallway = Hallway(constants.BILLIARD_BALLROOM)
		LiBiHallway = Hallway(constants.LIBRARY_BILLIARD)
		BiDHallway = Hallway(constants.BILLIARD_DINING)
		HBiHallway = Hallway(constants.HALL_BILLIARD)
		SHHallway = Hallway(constants.STUDY_HALL)
		Study = Room(constants.STUDY)
		Hall = Room(constants.HALL)
		Library = Room(constants.LIBRARY)
		Lounge = Room(constants.LOUNGE)
		DiningRoom = Room(constants.DINING)
		Kitchen = Room(constants.KITCHEN)
		Ballroom = Room(constants.BALLROOM)
		Conservatory = Room(constants.CONSERVATORY)
		BilliardRoom = Room(constants.BILLIARD)
		SLHallway.addConnections(Study)
		SLHallway.addConnections(Library)
		LiCHallway.addConnections(Library)
		LiCHallway.addConnections(Conservatory)
		CBaHallway.addConnections(Conservatory)
		CBaHallway.addConnections(Ballroom)
		BaKHallway.addConnections(Ballroom)
		BaKHallway.addConnections(Kitchen)
		DKHallway.addConnections(Kitchen)
		DKHallway.addConnections(DiningRoom)
		DLoHallway.addConnections(DiningRoom)
		DLoHallway.addConnections(Lounge)
		HLoHallway.addConnections(Hall)
		HLoHallway.addConnections(Lounge)
		BaBiHallway.addConnections(Ballroom)
		BaBiHallway.addConnections(BilliardRoom)
		LiBiHallway.addConnections(Library)
		LiBiHallway.addConnections(BilliardRoom)
		BiDHallway.addConnections(BilliardRoom)
		BiDHallway.addConnections(DiningRoom)
		HBiHallway.addConnections(Hall)
		HBiHallway.addConnections(BilliardRoom)
		SHHallway.addConnections(Study)
		SHHallway.addConnections(Hall)
		Study.addConnections(SLHallway)
		Study.addConnections(SHHallway)
		Study.addConnections(BilliardRoom)
		Hall.addConnections(SHHallway)
		Hall.addConnections(HBiHallway)
		Hall.addConnections(HLoHallway)
		Lounge.addConnections(BilliardRoom)
		Lounge.addConnections(HLoHallway)
		Lounge.addConnections(DLoHallway)
		Library.addConnections(SLHallway)
		Library.addConnections(LiBiHallway)
		Library.addConnections(LiCHallway)
		BilliardRoom.addConnections(LiBiHallway)
		BilliardRoom.addConnections(BaBiHallway)
		BilliardRoom.addConnections(BiDHallway)
		BilliardRoom.addConnections(HBiHallway)
		DiningRoom.addConnections(BiDHallway)
		DiningRoom.addConnections(DKHallway)
		DiningRoom.addConnections(DLoHallway)
		Conservatory.addConnections(LiCHallway)
		Conservatory.addConnections(BilliardRoom)
		Conservatory.addConnections(CBaHallway)
		Ballroom.addConnections(CBaHallway)
		Ballroom.addConnections(BaBiHallway)
		Ballroom.addConnections(BaKHallway)
		Kitchen.addConnections(BaKHallway)
		Kitchen.addConnections(BilliardRoom)
		Kitchen.addConnections(DKHallway)
		# easier to lookup rooms with a map so we can set starting positions
		self.rooms = {
			constants.STUDY : Study,
			constants.HALL : Hall,
			constants.LOUNGE : Lounge,
			constants.LIBRARY : Library,
			constants.BILLIARD : BilliardRoom,
			constants.DINING : DiningRoom,
			constants.CONSERVATORY : Conservatory,
			constants.BALLROOM : Ballroom,
			constants.KITCHEN : Kitchen,
			constants.BILLIARD_DINING : BiDHallway,
			constants.DINING_KITCHEN : DKHallway,
			constants.STUDY_HALL : SHHallway,
			constants.STUDY_LIBRARY : SLHallway,
			constants.HALL_LOUNGE : HLoHallway,
			constants.HALL_BILLIARD : HBiHallway,
			constants.LIBRARY_BILLIARD : LiBiHallway,
			constants.CONSERVATORY_BALLROOM : CBaHallway,
			constants.BILLIARD_BALLROOM : BaBiHallway,
			constants.BALLROOM_KITCHEN : BaKHallway,
			constants.LIBRARY_CONSERVATORY : LiCHallway,
			constants.LOUNGE_DINING : DLoHallway
		}
		
	def getRooms(self):
		return self.rooms
