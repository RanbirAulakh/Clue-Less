import pika
import os
import random
from .game import Game

# TODO multiple host https://pika.readthedocs.io/en/stable/examples/blocking_consume_recover_multiple_hosts.html
# TODO investigate why RabbitMQ is not thread-safe

class Server:
    # basic code from https://www.rabbitmq.com/#getstarted 
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    game_model = {}

    def __init__(self):
        print("Welcome to Clue-Less (Text) Server!")
        self.start_queue()
        self.start_consume()
        self.channel.start_consuming() # this will listen for customer's messages

    def start_queue(self):
        self.channel.queue_declare(queue='create_game') # Declare a queue
        self.channel.queue_declare(queue='find_game') # Declare a queue

    def custom_queue(self, key):
        self.channel.queue_declare(queue=key) # Declare a queue

    def start_consume(self):
        self.channel.basic_consume(queue="create_game", auto_ack=True, on_message_callback=self.create_game)
        self.channel.basic_consume(queue="find_game", auto_ack=True, on_message_callback=self.find_game)

    def start_custom_consume(self, key):
        self.channel.basic_consume(queue=key, auto_ack=True, on_message_callback=self.game) # Declare a queue

    def create_game(self, ch, method, properties, body):
        print(str(body))
        print(properties.headers)
        generated_id = self.generate_game_id()
        if(body.decode() == "public"):
            g = Game(generated_id, False, "user", None)
            self.game_model[generated_id] = g

            # create game id queue 
            self.custom_queue(str(generated_id))

        elif(body.decode() == "private"):
            g = Game(generated_id, True, "user", None)
            self.game_model[generated_id] = g

            # create game id queue 
            self.custom_queue(str(generated_id))
        else:
            pass # it shouldn't reach here
        
    def find_game(self, ch, method, props, body):
        print("find game")
        resp = (len(self.game_model))
        print(resp)
        ch.basic_publish(exchange='', routing_key=props.reply_to, 
                properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(resp))

    def generate_game_id(self):
        while(True):
            generated_id = random.randint(0, 10000)
            if generated_id not in self.game_model.keys():
                return generated_id

    def game(self):
        pass
        