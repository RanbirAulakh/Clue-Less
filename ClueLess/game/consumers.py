
import logging
import json

from .logic import game
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from asgiref.sync import async_to_sync

from django.contrib.auth.models import AnonymousUser


class GameConsumers(AsyncWebsocketConsumer):
    # instead of storing the data to the DB and reading from the DB,
    # we can manage the game from the memory
    game_model = {}

    # keeps seperated from game_model since game_model will be used to send to users.
    # game_model_answers should only be verified on server side
    game_model_answers = {}

    async def connect(self):
        if self.scope['user'] == AnonymousUser:
            raise DenyConnection("Invalid User!")

        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = 'game_%s' % self.game_id

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

        await self.update_user_joined()

        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': "{0} has joined the game {1}".format(self.scope["user"], self.game_id),
                'model': json.dumps(self.game_model[self.game_id])
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

        await self.update_user_left()
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': "{0} left the game {1}".format(self.scope["user"], self.game_id),
                'model': json.dumps(self.game_model[self.game_id])
            }
        )

    async def receive(self, text_data):
        # (a person is moved, a suggestion is made, a player
        # disproves a suggestion, or a player is unable to disprove a suggestion)

        text_data_json = json.loads(text_data)

        # type = text_data_json["type"]


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
        if self.game_id in self.game_model.keys():
            current_players_lst = self.game_model[self.game_id]['players']
            if str(self.scope["user"]) not in current_players_lst:
                current_players_lst.append(str(self.scope["user"]))
                self.game_model[self.game_id]['users'] = current_players_lst

            if len(current_players_lst) > 2:
                # start game
                pass
        else:
            # create new game
            g = game.Game()

            self.game_model[self.game_id] = {}
            self.game_model[self.game_id]['id'] = str(self.game_id)
            self.game_model[self.game_id]['players'] = [str(self.scope["user"])]
            self.game_model[self.game_id]['status'] = "Started"
            self.game_model[self.game_id]['current_turn'] = [str(self.scope["user"])]

    async def update_user_left(self):
        if self.game_id in self.game_model.keys():
            current_players_lst = self.game_model[self.game_id]['players']
            if str(self.scope["user"]) in current_players_lst:
                current_players_lst.remove(str(self.scope["user"]))
                self.game_model[self.game_id]['users'] = current_players_lst
