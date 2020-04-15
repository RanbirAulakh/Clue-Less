# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

#Constants of the weapons
CANDLESTICK="Candlestick"
REVOLVER="Revolver"
PIPE="Lead Pipe"
ROPE="Rope"
WRENCH="Wrench"
DAGGER="Dagger"


#Array of weapons constants
WEAPONS=[CANDLESTICK, REVOLVER, ROPE, PIPE, WRENCH, DAGGER]

#Suspects/Possible Players
PLUM="Professor Plum"
MUSTARD="Colonel Mustard"
GREEN="Mr. Green"
WHITE="Mrs. White"
SCARLET="Ms. Scarlet" #Ms. to Miss?
PEACOCK="Mrs. Peacock"

#Array of them like the weapons
SUSPECTS=[PEACOCK,PLUM,MUSTARD,GREEN,WHITE,SCARLET]

#Room names, 9 in all, Ordered by Top left corner to bottom right corner
"""
Study 	= Hall 	   = Lounge
||			||		||
Library = billiard = dining
||			||		||
Conserv = Ballroom = Kitchen
"""
STUDY="Study"
HALL="Hall"
LOUNGE="Lounge"
LIBRARY="Library"
BILLIARD="Billiard Room"
DINING="Dining"
CONSERVATORY="Conservatory"
BALLROOM="Ballroom"
KITCHEN="Kitchen"

ROOMS=[STUDY,HALL,LOUNGE,LIBRARY,BILLIARD,DINING,CONSERVATORY,BALLROOM,KITCHEN]

#Hallways - Treated as rooms for movement, but no actual guesses may be made.
#No hallways for secret passages, suggest having an array of connections in each
#room object and referencing our constants for what it is.
STUDY_HALL="Study-Hall Hallway"
HALL_LOUNGE="Hall-Lounge Hallway"
STUDY_LIBRARY="Study-Library Hallway"
HALL_BILLIARD="Hall-Billiard Room Hallway"
LOUNGE_DINING="Lounge-Dining Room Hallway"
LIBRARY_BILLIARD="Library-Billiard Room Hallway"
BILLIARD_DINING="Billiard Room-Dining Room Hallway"
LIBRARY_CONSERVATORY="Library-Conservatory Hallway"
BILLIARD_BALLROOM="Billiard Room-Ballroom Hallway"
DINING_KITCHEN="Dining Room-Kitchen Hallway"
CONSERVATORY_BALLROOM="Conservatory-Ballroom Hallway"
BALLROOM_KITCHEN="Ballroom-Kitchen Hallway"

HALLWAYS=[STUDY_HALL, HALL_LOUNGE, STUDY_LIBRARY, HALL_BILLIARD, LOUNGE_DINING, LIBRARY_BILLIARD,
BILLIARD_DINING, LIBRARY_CONSERVATORY, BILLIARD_BALLROOM, DINING_KITCHEN, CONSERVATORY_BALLROOM,
BALLROOM_KITCHEN]
