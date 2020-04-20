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
            print("TYPE IF/ELSE {0}".format(text_data_json))
            if text_data_json["type"] == "select_move":
                self.select_move()
            elif text_data_json["type"] == "select_accuse":
                self.select_suggestion()
            elif text_data_json["type"] == "select_suggestion":
                self.select_accuse()
        else:
            message = text_data_json['message']
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
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

    async def show_available_rooms(self):
        print("Show_available_rooms")

    async def get_locations(self):
        if self.game_memory_data[self.game_id].status == "Started":
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'chat_message',
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
                    'your_turn': False
                }
            )

            # Once group messages are sent out
            # then alert user that it is their turn
            # and their buttons will be enabled
            await self.channel_layer.group_send(
                user_channel,
                {
                    'type': 'chat_message',
                    'your_turn': True,
                }
            )

    async def select_move(self):
        user = str(self.scope['user'])
        print("Implement Select Move")

    async def select_suggestion(self):
        user = str(self.scope['user'])
        print("Implement Select suggestion")

    async def select_accuse(self):
        user = str(self.scope['user'])
        print("Implement Select accuse")