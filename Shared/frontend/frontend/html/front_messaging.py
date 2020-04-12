import pika
import json
import logging
import time
import os

class messaging:
  
    request_queue_name = 'requesting data'


    credentials = pika.PlainCredentials(os.environ['RABBITMQ_DEFAULT_USER'],
                                        os.environ['RABBITMQ_DEFAULT_PASS'])

    # docker-compose will resolve this host to our messaging service
    host = 'messaging'

    def __init__(s):
     
        logging.info("Messaging: Establishing connection")
        s.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=s.host, credentials=s.credentials))
        s.channel = s.connection.channel()
        logging.info("Messaging: Creating queues")
        s.channel.queue_declare(queue=s.request_queue_name)
        s.result_queue = s.channel.queue_declare(queue='', exclusive=True).method.queue

    def __del__(s):
    
        logging.info("Messaging: Connection will close down")
        s.connection.close()

    def send(s, action, data):

        logging.info(f"Messaging: send(action={action}, data={data})")

        s.channel.basic_publish(
            exchange='',
            routing_key=s.request_queue_name,
            properties=pika.BasicProperties(
                reply_to=s.result_queue),
                body=json.dumps({'action': action, 'data': data}
            )
        )

    def receive(s):

        attempts = 0
        while True:
            method_frame, properties, body = s.channel.basic_get(
                s.result_queue, auto_ack=True)
            if method_frame:
                received = json.loads(body)
                logging.info(f"Messaging: received={received}")
                return received
            elif attempts > 10:
                logging.info("Messaging: receive did not get message")
                return None
            else:
                time.sleep(0.1)
                attempts += 1
