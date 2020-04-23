#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
channel = connection.channel()
channel.queue_declare(queue='from_node')

def on_message(channel, delivery, properties, body):
    """Callback when a message arrives.
    :param channel: the AMQP channel object.
    :type channel: :class:`pika.channel.Channel`
    :param delivery: the AMQP protocol-level delivery object,
      which includes a tag, the exchange name, and the routing key.
      All of this should be information the sender has as well.
    :type delivery: :class:`pika.spec.Deliver`
    :param properties: AMQP per-message metadata.  This includes
      things like the body's content type, the correlation ID and
      reply-to queue for RPC-style messaging, a message ID, and so
      on.  It also includes an additional table of structured
      caller-provided headers.  Again, all of this is information
      the sender provided as part of the message.
    :type properties: :class:`pika.spec.BasicProperties`
    :param str body: Byte string of the message body.
    """
    # Just dump out the information we think is interesting.
    print('Exchange: %s' % (delivery.exchange,))
    print('Routing key: %s' % (delivery.routing_key,))
    print('Content type: %s' % (properties.content_type,))
    print()
    print(body)
    print()

# def callback(ch, method, properties, body):
#   requestParams = json.loads(body.decode('utf-8'))

# receive message and complete simulation
channel.basic_consume(on_message, queue='from_node', no_ack=True)
channel.start_consuming()