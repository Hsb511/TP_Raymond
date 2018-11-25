#!/usr/bin/env python
import pika
import sys
import time
import random

architecture = ["A", "B", "C", "D", "E", "F"]

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

while(True):
	init_node = random.choice(architecture)

	channel.queue_declare(init_node + "I")
	
	channel.basic_publish(exchange='', routing_key = init_node + "I", body="[X] Envoi d'une requete sur la queue : " + "I" + init_node)

	channel.queue_declare("I" + init_node)

	channel.basic_publish(exchange='', routing_key = "I" + init_node, body = init_node+',request')
	
	time.sleep(1)

connection.close()

