import pika
import os
import enum
import inquirer
import random
import string
import json
import uuid

class Options(enum.Enum):
    PUBLIC_GAME = "Public"
    PRIVATE_GAME = "Private"
    BACK = "Go back to Main Menu"

# TODO SUGGESSTION implement JSON (generate or parse)
# TODO implment RabbitMQ Heartbeat (check if its online or not)
class Game:
    def __init__(self):
        self.device_id = str(uuid.uuid4())
        self.url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
        self.params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = self.result.method.queue
        self.channel.basic_consume(queue=self.callback_queue,on_message_callback=self.on_response,auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.device_id == props.correlation_id:
            self.response = body

    def create_game(self, player_name):
        choices = inquirer.list_input("What would you like to do?",
            choices=[Options.PUBLIC_GAME.value, Options.PRIVATE_GAME.value, Options.BACK.value])

        self.channel.queue_declare(queue='create_game')
        if Options.PUBLIC_GAME.value == choices:
            msg = { "username": player_name}
            self.channel.basic_publish(exchange='', routing_key='create_game', body='public')

        elif Options.PRIVATE_GAME.value == choices:
            private_key = self.generate_private_key()
            msg = { "username": player_name, "private_key": private_key}
            self.channel.basic_publish(exchange='', routing_key='create_game', body=json.dumps(msg))

        elif Options.BACK.value == choices:
            return

    def find_game(self):
        self.response = None
        print("Searching for game...")
        self.channel.basic_publish(exchange='', routing_key='find_game', body='public', 
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.device_id))
        
        while self.response is None:
            self.connection.process_data_events()
        print(self.response)
        # self.channel.start_consuming()

    def generate_private_key(self,stringLength=6):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
