import pika
import os

def callback(ch, method, properties, body):
    print(" [x] Received " + str(body))
    
def start_server():
    # basic code from https://www.rabbitmq.com/#getstarted 
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://oczwxoia:Ed4t562v_dpmVP5P-j9EmwTBmz2Fc5RJ@termite.rmq.cloudamqp.com/oczwxoia')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='hello') # Declare a queue
    channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

start_server()
