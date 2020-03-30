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
    REFRESH_GAME = "Refresh games"

# TODO SUGGESSTION implement JSON (generate or parse)
# TODO implment RabbitMQ Heartbeat (check if its online or not)
class Game:
    def __init__(self):
        self.player_name = ""
        self.device_id = str(uuid.uuid4())
        self.url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
        self.params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()

    def on_response(self, ch, method, props, body):
        if self.device_id == props.correlation_id:
            self.response = body

    def create_game(self, player_name):
        self.player_name = player_name
        choices = inquirer.list_input("What would you like to do?",
            choices=[Options.PUBLIC_GAME.value, Options.PRIVATE_GAME.value, Options.BACK.value])

        self.channel.queue_declare(queue='create_game')
        if Options.PUBLIC_GAME.value == choices:
            msg = { "visibility": True, "user": self.player_name, "key": None}
            self.channel.basic_publish(exchange='', routing_key='create_game', body=json.dumps(msg))

        elif Options.PRIVATE_GAME.value == choices:
            key = inquirer.text("Create your own password (Leave blank for generated key)?")
            if key == "":
                key = self.generate_private_key()
                print("Your password is: {0} and share with your friends!".format(key))
            msg = { "visibility": False, "user": self.player_name, "key":key}
            self.channel.basic_publish(exchange='', routing_key='create_game', body=json.dumps(msg))

        elif Options.BACK.value == choices:
            return

    def find_game(self):
        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = self.result.method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

        self.response = None
        print("Searching for game...")
        self.channel.basic_publish(exchange='', routing_key='find_game', body='public', 
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.device_id))
        
        while self.response is None:
            self.connection.process_data_events()
        
        if(self.response.decode() == "No available games!"):
            choices = inquirer.list_input("No available games!",
                choices=[Options.REFRESH_GAME.value, Options.BACK.value])

            if Options.REFRESH_GAME.value == choices:
                self.find_game()
            elif Options.BACK.value == choices:
                return
        else:
            self.display_available_games(self.response)
    
    def display_available_games(self, msg):
        self.response = None # clear it
        json_msg = json.loads(msg.decode())

        lst = []
        for i in json_msg:
            visibility = "Public" if json_msg[i]["visibility"] else "Private"
            game_choice_format = "{0} - {1}'s Lobby ({2})".format(i, json_msg[i]["created_by"], visibility)
            lst.append(game_choice_format)

        lst.extend([Options.REFRESH_GAME.value, Options.BACK.value])
        choices = inquirer.list_input("Which Clue-Less games would you like to join?", choices=lst)

        if choices == Options.REFRESH_GAME.value:
            self.find_game()
        elif choices == Options.REFRESH_GAME.value:
            return
        else:
            id = choices.split(" -")[0]
            if json_msg[id]["visibility"]:
                self.join_lobby(id)
            else:
                # TODO validate private_key on server side
                validate_key = inquirer.text("What is the password to this lobby?")
                if validate_key == json_msg[id]["key"]:
                    # join the lobby
                    self.join_lobby(id)
                else:
                    print("Incorrect password!")
                    self.find_game()

    def join_lobby(self, id):
        pass 

    def game_chat(self, ch, method, properties, body):
        print("here??")
        print(body.decode())

    def generate_private_key(self,stringLength=6):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
