# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

from room import Room
import constants

class Map :
	def __init__(self):
		self.map = {
			constants.STUDY : [constants.STUDY_HALL, constants.STUDY_LIBRARY, constants.KITCHEN],
			constants.HALL : [constants.STUDY_HALL, constants.HALL_LOUNGE, constants.HALL_BILLIARD],
			constants.LOUNGE : [constants.HALL_LOUNGE, constants.LOUNGE_DINING, constants.CONSERVATORY],
			constants.LIBRARY : [constants.STUDY_LIBRARY, constants.LIBRARY_CONSERVATORY, constants.LIBRARY_BILLIARD],
			constants.BILLIARD : [constants.HALL_BILLIARD, constants.BILLIARD_DINING, constants.LIBRARY_BILLIARD, constants.BILLIARD_BALLROOM],
			constants.DINING : [constants.BILLIARD_DINING, constants.LOUNGE_DINING, constants.DINING_KITCHEN],
			constants.CONSERVATORY : [constants.CONSERVATORY_BALLROOM, constants.LIBRARY_CONSERVATORY, constants.LOUNGE],
			constants.BALLROOM : [constants.BILLIARD_BALLROOM, constants.CONSERVATORY_BALLROOM, constants.BALLROOM_KITCHEN],
			constants.KITCHEN : [constants.DINING_KITCHEN, constants.BALLROOM_KITCHEN, constants.STUDY],
			constants.BILLIARD_DINING:[constants.BILLIARD, constants.DINING],
			constants.DINING_KITCHEN:[constants.DINING, constants.KITCHEN],
			constants.STUDY_HALL : [constants.STUDY, constants.HALL],
			constants.STUDY_LIBRARY : [constants.STUDY, constants.LIBRARY],
			constants.HALL_LOUNGE : [constants.HALL, constants.LOUNGE],
			constants.HALL_BILLIARD : [constants.HALL, constants.BILLIARD],
			constants.LIBRARY_BILLIARD : [constants.LIBRARY, constants.BILLIARD],
			constants.CONSERVATORY_BALLROOM : [constants.CONSERVATORY, constants.BALLROOM],
			constants.BILLIARD_BALLROOM : [constants.BILLIARD, constants.BALLROOM],
			constants.BALLROOM_KITCHEN : [constants.BALLROOM, constants.KITCHEN],
			constants.LIBRARY_CONSERVATORY : [constants.LIBRARY, constants.CONSERVATORY],
			constants.LOUNGE_DINING : [constants.LOUNGE, constants.DINING]
		}
		print(self.map[constants.STUDY])
		pass
		