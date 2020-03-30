import pika
import os
import random
from .game import Game
from .player import Player
import json

# TODO multiple host https://pika.readthedocs.io/en/stable/examples/blocking_consume_recover_multiple_hosts.html
# TODO investigate why RabbitMQ is not thread-safe
class Server:

    def __init__(self):
        # basic code from https://www.rabbitmq.com/#getstarted 
        self.url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
        self.params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.game_model = {}

        print("Welcome to Clue-Less (Text) Server!")
        self.generate_game_test()
        self.start_queue()
        self.start_consume()
        self.channel.start_consuming() # this will listen for customer's messages

    def start_queue(self):
        self.channel.queue_declare(queue='create_game') # Declare a queue
        self.channel.queue_declare(queue='find_game') # Declare a queue
        
        # self.channel.exchange_declare(exchange='logs', exchange_type='fanout')
        # result = self.channel.queue_declare(queue='loggy', exclusive=True)
        # queue_name = result.method.queue
        # self.channel.queue_bind(exchange='logs', queue=queue_name)
        # self.channel.basic_consume(queue='loggy', auto_ack=True, on_message_callback=self.game_lobby) # Declare a queue

    def start_consume(self):
        self.channel.basic_consume(queue="create_game", auto_ack=True, on_message_callback=self.create_game)
        self.channel.basic_consume(queue="find_game", auto_ack=True, on_message_callback=self.find_game)

    def custom_queue(self, key):
        self.channel.queue_declare(queue=key) # Declare a queue

    def start_custom_consume(self, key):
        self.channel.basic_consume(queue=key, auto_ack=True, on_message_callback=self.game_lobby) # Declare a queue
        
    # remove this testing function
    def generate_game_test(self):
        testPlayer1 = Player("test", "green")
        generated_id = self.generate_game_id()

        g = Game(generated_id, [testPlayer1], True, "Deez", None)
        self.game_model[generated_id] = g
        self.custom_queue(str(generated_id))
        self.start_custom_consume(str(generated_id))

        generated_id = self.generate_game_id()
        g = Game(generated_id, [testPlayer1], True, "Dog", None)
        self.game_model[generated_id] = g
        self.custom_queue(str(generated_id))
        self.start_custom_consume(str(generated_id))
        
        generated_id = self.generate_game_id()
        g = Game(generated_id, [testPlayer1], False, "Hola", "1234")
        self.game_model[generated_id] = g
        self.custom_queue(str(generated_id))
        self.start_custom_consume(str(generated_id))

    def create_game(self, ch, method, properties, body):
        testPlayer1 = Player("test", "green")

        json_msg = json.loads(body.decode())
        generated_id = self.generate_game_id()

        g = Game(generated_id, [testPlayer1], json_msg["visibility"], json_msg["user"], json_msg["key"])
        self.game_model[generated_id] = g

        # create game id queue 
        self.custom_queue(str(generated_id))
        self.start_custom_consume(str(generated_id))
        print("server created a game " + str(body))
        
    def find_game(self, ch, method, props, body):
        msg = { }
        for i in self.game_model:
            clueless_game = self.game_model[i]
            msg[clueless_game.id] = self.game_model[i].convert_to_json()

        if(len(msg) < 1):
            msg = "No available games!"

        ch.basic_publish(exchange='', routing_key=props.reply_to, 
                properties=pika.BasicProperties(correlation_id = props.correlation_id), 
                body=json.dumps(msg))

    def generate_game_id(self):
        while(True):
            generated_id = random.randint(0, 10000)
            if generated_id not in self.game_model.keys():
                return generated_id

    def game_lobby(self, ch, method, props, body):
        print(method)
        #json_msg = json.loads(body.decode())
        #game_id = json_msg["id"]
        #msg = "{0} said: {1}".format(json_msg["user"], json_msg["msg"])
        # self.channel.basic_publish(exchange='logs', routing_key='get_server', body="pbuck")
        #return