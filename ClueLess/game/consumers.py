# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro
# description:

import logging
import json

from .logic import game
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async

from django.contrib.auth.models import AnonymousUser

from . import models


class GameConsumers(AsyncWebsocketConsumer):
    # instead of storing the data to the DB and reading from the DB,
    # we can manage the game from the memory
    # This is the model that will be returned to user (contains partial data)
    game_model = {}

    # Private game memory (contains all data)
    game_memory_data = {}

    # game log
    game_log = {}

    async def connect(self):
        if self.scope['user'] == AnonymousUser:
            raise DenyConnection("Invalid User!")

        # get game_id from URL
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = 'game_%s' % self.game_id

        # create new channel with game_id
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        # create card individual channel with game_id
        individual_user_chan = "{0}_game_{1}".format(str(self.scope['user']), self.game_id)
        await self.channel_layer.group_add(
            individual_user_chan,
            self.channel_name
        )

        # check if the game exist in the memory
        # If not, create new game and store them in the memory
        if self.game_id not in self.game_memory_data.keys():
            print("Creating new game instances")
            self.game_memory_data[self.game_id] = game.Game()

            self.game_model[self.game_id] = {}
            self.game_model[self.game_id]['id'] = str(self.game_id)
            self.game_model[self.game_id]['players'] = []

            self.game_log[self.game_id] = {}
            self.game_log[self.game_id] = ''

        # accept users connection
        await self.accept()

        if self.game_memory_data[self.game_id].status == "Finished!":
            return

        # add user to the game
        await self.update_user_joined()

        # let other users in the game know that this user joined
        msg = "{0} has joined the game {1}".format(self.scope["user"], self.game_id)
        self.game_log[self.game_id] += '\n' + msg
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': msg,
                'game_status': self.game_memory_data[self.game_id].status,
                'model': json.dumps(self.game_model[self.game_id]),
            }
        )

        await self.send(text_data=json.dumps({
                "log": self.game_log[self.game_id]
            }
        ))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

        await self.update_user_left()
        msg = "{0} left the game {1}".format(self.scope["user"], self.game_id)
        self.game_log[self.game_id] += '\n' + msg

        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': msg,
                'model': json.dumps(self.game_model[self.game_id])
            }
        )

    async def receive(self, text_data):
        """
        This function is responsible for listening users interactions such as:
            Move
            Choose Character
            Make Suggestion
            Disapprove Suggestion
            Unable to disprove a suggestion
            Accuse someone
        """

        text_data_json = json.loads(text_data)

        if "player_select" in text_data_json:
            await self.update_chosen_character(text_data_json['player_select'])
            await self.get_cards()
            await self.get_locations()
            await self.update_users_turn()

        elif "show_available_moves" in text_data_json:
            await self.show_available_rooms()
        elif "type" in text_data_json:
            if text_data_json["type"] == "select_move":
                await self.select_move(text_data_json)
            elif text_data_json["type"] == "select_accuse":
                await self.select_accuse(text_data_json)
            elif text_data_json["type"] == "select_suggestion":
                await self.select_suggestion(text_data_json)
            elif text_data_json["type"] == "end_turn":
                await self.end_turn()
            elif text_data_json["type"] == "approved_cards":
                await self.choose_approved_cards(text_data_json)
            elif text_data_json["type"] == "what_card_to_show":
                await self.show_one_card(text_data_json)
        else:
            message = text_data_json['message']
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'game_status': self.game_memory_data[self.game_id].status,
                    'message': message
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    async def update_user_joined(self):
        user = str(self.scope['user'])

        self.game_model[self.game_id]['players'].append(user)

        if not self.game_memory_data[self.game_id].already_chosen(user):
            await self.send(text_data=json.dumps({
                    "pick_character": True,
                    'game_status': self.game_memory_data[self.game_id].status,
                    "available_characters": self.game_memory_data[self.game_id].available_characters
                }
            ))
        else:
            character_select = self.game_memory_data[self.game_id].get_chosen_character(user)
            player_cards = self.game_memory_data[self.game_id].get_cards(user)
            locations = self.game_memory_data[self.game_id].get_locations()

            # if user accidentally refreshed
            # let that player know that it is their turn and alert others that this is player's turn
            await self.update_users_turn()

            await self.send(text_data=json.dumps({
                    "update_character_section": character_select,
                    "your_cards": player_cards,
                    'game_status': self.game_memory_data[self.game_id].status,
                    "update_location": locations,
                }
            ))

    async def update_user_left(self):
        user = str(self.scope['user'])

        # self.game_memory_data[self.game_id]['game'].remove_player(user)
        self.game_model[self.game_id]['players'].remove(user)

    async def update_chosen_character(self, character_select):
        user = str(self.scope['user'])
        self.game_memory_data[self.game_id].add_player(user)
        if self.game_memory_data[self.game_id].player_select_character(user, character_select):
            msg = "{0} selects {1} as their game piece character.".format(user, character_select)
            self.game_log[self.game_id] += '\n' + msg

            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    "available_characters": self.game_memory_data[self.game_id].available_characters,
                }
            )
            await self.send(text_data=json.dumps({
                    "pick_character": False,
                    "available_characters": None,
                    "update_character_section": character_select
                }
            ))

            # check if # of players has chose their character and start the game!
            required_players = await self.get_required_players()
            if str(required_players) == str(len(self.game_memory_data[self.game_id].players)):
                if self.game_memory_data[self.game_id].status == "Not Started":
                    self.game_memory_data[self.game_id].start_game()
                    self.game_model[self.game_id]['status'] = "Started"

        else:
            await self.send(text_data=json.dumps({
                    "error": "Character already chosen! Please choose another one!",
                    "pick_character": True,
                    "available_characters": self.game_memory_data[self.game_id].available_characters
                }
            ))

    @database_sync_to_async
    def get_required_players(self):
        return models.Game.objects.get(id=self.game_id).required_players

    async def get_cards(self):
        """
        This is useful is player accidentally refresh.
        :return:
        """
        if self.game_memory_data[self.game_id].status == "Started":
            for i in self.game_memory_data[self.game_id].players:
                user = i.name
                user_channel = "{0}_game_{1}".format(user, self.game_id)
                cards = self.game_memory_data[self.game_id].get_cards(user)

                msg = "{0} drew {1} cards!".format(user, len(cards))
                self.game_log[self.game_id] += '\n' + msg

                await self.channel_layer.group_send(
                    user_channel,
                    {
                        'type': 'chat_message',
                        'your_cards': cards,
                    }
                )

                # let other people know how many cards you drew
                await self.channel_layer.group_send(
                    self.game_group_name,
                    {
                        'type': 'chat_message',
                        'message': msg,
                    }
                )

    async def get_locations(self):
        if self.game_memory_data[self.game_id].status == "Started":
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'game_status': self.game_memory_data[self.game_id].status,
                    "update_location": self.game_memory_data[self.game_id].get_locations()
                }
            )

    async def update_users_turn(self):
        if self.game_memory_data[self.game_id].status == "Started":
            whose_turn_user = self.game_memory_data[self.game_id].current_turn.name
            user_channel = "{0}_game_{1}".format(whose_turn_user, self.game_id)

            print(user_channel)

            msg = "It is {0}'s turn.".format(whose_turn_user)
            self.game_log[self.game_id] += '\n' + msg

            # reason the group message goes first
            # 1. It will send to all users within the game
            # and it will disable everyone' buttons
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                }
            )

            # Once group messages are sent out
            # then alert user that it is their turn
            # and their buttons will be enabled
            current_location = self.game_memory_data[self.game_id].get_player_current_location(whose_turn_user)
            available_moves = self.game_memory_data[self.game_id].get_available_moves()
            is_in_room = self.game_memory_data[self.game_id].is_in_room(whose_turn_user)  # verify if user is in room
            is_moved_made = self.game_memory_data[self.game_id].is_move_made

            await self.channel_layer.group_send(
                user_channel,
                {
                    'type': 'chat_message',
                    'enable_btn': {'move': not is_moved_made, 'accuse': True, 'suggest': is_in_room, 'end_turn': True},
                    'available_moves': available_moves,
                    'game_status': self.game_memory_data[self.game_id].status,
                    'current_location': current_location,
                }
            )

    async def select_move(self, data):
        print("Select move")
        user = str(self.scope['user'])
        next_move = data['move_to']
        user_channel = "{0}_game_{1}".format(user, self.game_id)

        flag = self.game_memory_data[self.game_id].move_player(user, next_move)
        if flag:
            msg = "{0} moved to {1}".format(user, next_move)
            self.game_log[self.game_id] += '\n' + msg

            current_location = self.game_memory_data[self.game_id].get_player_current_location(user)

            # group msg
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                }
            )

            # user msg
            await self.channel_layer.group_send(
                user_channel,
                {
                    'type': 'chat_message',
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': True, 'suggest': True, 'end_turn': True},
                    'current_location': current_location,
                }
            )

            await self.get_locations()

    async def select_suggestion(self, data):
        user = str(self.scope['user'])
        user_channel = "{0}_game_{1}".format(user, self.game_id)

        suspect_suggest = data['suggest']['suspect']
        room_suggest = data['suggest']['room']
        weapon_suggest = data['suggest']['weapon']

        msg = "\n{0} suggested the crime was committed in the {1} by {2} with the {3}".format(user, suspect_suggest, room_suggest, weapon_suggest)

        result = self.game_memory_data[self.game_id].make_guess(user, {"suspect": suspect_suggest, "room": room_suggest, "weapon": weapon_suggest})

        msg += '\n' + "{0} will look at their cards to see if {1} makes the right suggestion." \
            .format(result['player_to_approve_disapprove'], user)

        self.game_log[self.game_id] += '\n' + msg

        # approver/disapprover msg
        approver_channel = "{0}_game_{1}".format(result['player_to_approve_disapprove'], self.game_id)
        await self.channel_layer.group_send(
            approver_channel,
            {
                'type': 'chat_message',
                'message': msg,
                'game_status': self.game_memory_data[self.game_id].status,
                'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                'cards_to_approve_disapprove': result['cards'],
                'player_owner_cards': result['player_owner_cards'],
                'suggester_name': result['player_suggester'],
                'suggest_msg':
                    "{0} suggested the crime was committed in the '{1}' by '{2}' with the '{3}'. "
                    "Below is {4}'s cards. Please tick if it matches suggester's comment."
                        .format(user, suspect_suggest, room_suggest, weapon_suggest, result['player_owner_cards'])
            }
        )

        # alert all
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': msg,
                'game_status': self.game_memory_data[self.game_id].status,
                'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                'update_location': self.game_memory_data[self.game_id].get_locations()
            }
        )

    async def select_accuse(self, data):
        user = str(self.scope['user'])
        user_channel = "{0}_game_{1}".format(user, self.game_id)
        suspect_accused = data['accused']['suspect']
        room_accused = data['accused']['room']
        weapon_accused = data['accused']['weapon']

        msg = "{0} accuse {1} of committing the crime in the {2} with the {3}".format(user, suspect_accused, room_accused, weapon_accused)
        self.game_log[self.game_id] += '\n' + msg

        # check if its correct
        is_correct = self.game_memory_data[self.game_id].make_accusation(user, [suspect_accused, room_accused, weapon_accused])

        if is_correct:
            msg += "\nCONGRATULATION! {0} is a winner!".format(user)

            # group msg
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'winner': {"user": user, "bool": False},
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                }
            )

            # user msg
            await self.channel_layer.group_send(
                user_channel,
                {
                    'type': 'chat_message',
                    'winner': {"user": user, "bool": True},
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                }
            )

        else:
            msg += "\nUnfortunately, {0} is incorrect and no longer can make moves, suggestions, or accusation. Poor guy.".format(user)

            # group msg
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                }
            )

            # user msg
            await self.channel_layer.group_send(
                user_channel,
                {
                    'type': 'chat_message',
                    'incorrect_accused_notification': True,
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                }
            )

            # next turn
            self.game_memory_data[self.game_id].next_turn()
            await self.update_users_turn()

    async def end_turn(self):
        self.game_memory_data[self.game_id].next_turn()
        await self.update_users_turn()

    async def choose_approved_cards(self, data):
        approved_cards = data['approved_cards']
        owner_card_user_channel = "{0}_game_{1}".format(str(data['owner_cards']), self.game_id)
        suggester_user_channel = "{0}_game_{1}".format(str(data['suggester']), self.game_id)

        print(approved_cards)

        if len(approved_cards) == 0:
            msg = "Unfortunately, suggester, {0}, fails to prove {1}."\
                .format(str(data['owner_cards']), str(data['suggester']))
            self.game_log[self.game_id] += '\n' + msg
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False}
                }
            )

            await self.end_turn()

        elif len(approved_cards) == 1:
            # message to suggester and show only 1 card!
            msg = "{0} showed one card to {1}.".format(str(data['owner_cards']), str(data['suggester']))
            await self.channel_layer.group_send(
                suggester_user_channel,
                {
                    'type': 'chat_message',
                    'message': msg + ". {0} showed you {1}".format(str(data['owner_cards']), approved_cards[0]),
                    'enable_btn': {'move': False, 'accuse': True, 'suggest': False, 'end_turn': True}
                }
            )

            # alert others that owner of the card showed one card to suggester
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False}
                }
            )

            self.game_log[self.game_id] += '\n' + msg

            await self.end_turn()

        elif len(approved_cards) > 1:
            msg = "{0} is determining which card to show to suggester, {1}."\
                .format(str(data['owner_cards']), str(data['suggester']))

            # send to user to choose which one of the card to show to suggester
            await self.channel_layer.group_send(
                owner_card_user_channel,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'choose_approved_cards': approved_cards,
                    'approved_cards_suggester': str(data['suggester']),
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False},
                }
            )

            # alert others that owner is deciding which card to send to suggester
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'game_status': self.game_memory_data[self.game_id].status,
                    'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False}
                }
            )

    async def show_one_card(self, data):
        print("w here?");
        owner = str(self.scope['user'])
        card = data['what_card_to_show']
        suggester_user_channel = "{0}_game_{1}".format(str(data['suggester']), self.game_id)

        # message to suggester and show only 1 card!
        msg = "{0} showed one card to {1}.".format(owner, str(data['suggester']))
        await self.channel_layer.group_send(
            suggester_user_channel,
            {
                'type': 'chat_message',
                'message': msg + ". {0} showed you {1}".format(owner, card),
                'enable_btn': {'move': False, 'accuse': True, 'suggest': False, 'end_turn': True}
            }
        )

        # alert others that owner is showed one card to suggester
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': msg,
                'game_status': self.game_memory_data[self.game_id].status,
                'enable_btn': {'move': False, 'accuse': False, 'suggest': False, 'end_turn': False}
            }
        )

        self.game_log[self.game_id] += '\n' + msg
        await self.end_turn()
