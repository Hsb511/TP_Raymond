#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

architecture = ["A", "B", "C", "D", "E", "F"]

def callback(ch, method, properties, body):
    print(body)


for k in architecture:
    channel.queue_declare(k + "I")
    channel.basic_consume(callback,
                      queue=k+"I",
                      no_ack=True)

channel.start_consuming()
