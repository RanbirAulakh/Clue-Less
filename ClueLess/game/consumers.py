
import logging
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from asgiref.sync import async_to_sync

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist


class GameConsumers(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope['user'] == AnonymousUser:
            raise DenyConnection("Invalid User!")

        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = 'game_%s' % self.game_id

        print("{0} is connected to Game {1}".format(self.scope["user"], self.game_id))

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': "{0} is connected to Game {1}".format(self.scope["user"], self.game_id)
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

        # await self.send(text_data=json.dumps({
        #     'message_user_connected': "{0} left the Game {1}".format(self.scope["user"], self.game_id)
        # }))
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': "{0} left the Game {1}".format(self.scope["user"], self.game_id)
            }
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        print(event)
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

