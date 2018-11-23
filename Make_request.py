#!/usr/bin/env python
import pika
import sys
import time
import random

architecture = ["A", "B"]
#architecture = ["A", "B", "C", "D", "E", "F"]

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

while(True):
	init_node = random.choice(architecture)

	channel.queue_declare(init_node+"I")

	channel.basic_publish(exchange='', routing_key='hello', body=init_node+',request')

	time.sleep(30)

connection.close()

#while(True):
