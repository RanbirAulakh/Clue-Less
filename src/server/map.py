# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

from room import *
import constants

def genMap() :
	map = {
		constants.STUDY : Room(constants.STUDY, [constants.STUDY_HALL, constants.STUDY_LIBRARY, constants.KITCHEN]),
		constants.HALL : Room(constants.HALL,[constants.STUDY_HALL, constants.HALL_LOUNGE, constants.HALL_BILLIARD]),
		constants.LOUNGE : Room(constants.LOUNGE,[constants.HALL_LOUNGE, constants.LOUNGE_DINING, constants.CONSERVATORY]),
		constants.LIBRARY : Room(constants.LIBRARY,[constants.STUDY_LIBRARY, constants.LIBRARY_CONSERVATORY, constants.LIBRARY_BILLIARD]),
		constants.BILLIARD : Room(constants.BILLIARD,[constants.HALL_BILLIARD, constants.BILLIARD_DINING, constants.LIBRARY_BILLIARD, constants.BILLIARD_BALLROOM]),
		constants.DINING : Room(constants.DINING,[constants.BILLIARD_DINING, constants.LOUNGE_DINING, constants.DINING_KITCHEN]),
		constants.CONSERVATORY : Room(constants.CONSERVATORY,[constants.CONSERVATORY_BALLROOM, constants.LIBRARY_CONSERVATORY, constants.LOUNGE]),
		constants.BALLROOM : Room(constants.BALLROOM,[constants.BILLIARD_BALLROOM, constants.CONSERVATORY_BALLROOM, constants.BALLROOM_KITCHEN]),
		constants.KITCHEN : Room(constants.KITCHEN,[constants.DINING_KITCHEN, constants.BALLROOM_KITCHEN, constants.STUDY]),
		constants.BILLIARD_DINING : Hallway(constants.BILLIARD_DINING,[constants.BILLIARD, constants.DINING]),
		constants.DINING_KITCHEN : Hallway(constants.DINING_KITCHEN,[constants.DINING, constants.KITCHEN]),
		constants.STUDY_HALL : Hallway(constants.STUDY_HALL,[constants.STUDY, constants.HALL]),
		constants.STUDY_LIBRARY : Hallway(constants.STUDY_LIBRARY,[constants.STUDY, constants.LIBRARY]),
		constants.HALL_LOUNGE : Hallway(constants.HALL_LOUNGE,[constants.HALL, constants.LOUNGE]),
		constants.HALL_BILLIARD : Hallway(constants.HALL_BILLIARD,[constants.HALL, constants.BILLIARD]),
		constants.LIBRARY_BILLIARD : Hallway(constants.LIBRARY_BILLIARD,[constants.LIBRARY, constants.BILLIARD]),
		constants.CONSERVATORY_BALLROOM : Hallway(constants.CONSERVATORY_BALLROOM,[constants.CONSERVATORY, constants.BALLROOM]),
		constants.BILLIARD_BALLROOM : Hallway(constants.BILLIARD_BALLROOM,[constants.BILLIARD, constants.BALLROOM]),
		constants.BALLROOM_KITCHEN : Hallway(constants.BALLROOM_KITCHEN,[constants.BALLROOM, constants.KITCHEN]),
		constants.LIBRARY_CONSERVATORY : Hallway(constants.LIBRARY_CONSERVATORY,[constants.LIBRARY, constants.CONSERVATORY]),
		constants.LOUNGE_DINING : Hallway(constants.LOUNGE_DINING,[constants.LOUNGE, constants.DINING])
	}
	print(constants.STUDY)
	return map
		