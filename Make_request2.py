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

'''
while(True):
	init_node = random.choice(architecture)

	channel.queue_declare(init_node+"I")
	
	print("envoi d'un message sur la queue : " + init_node + "I")

	channel.basic_publish(exchange='', routing_key=init_node + "I", body=init_node+',request')

	time.sleep(30)

connection.close()
'''

init_node = 'A'

channel.queue_declare("I"+init_node)
	
print("envoi d'un message sur la queue : " + "I" + init_node)

channel.basic_publish(exchange='', routing_key="I" + init_node, body=init_node+',request')

def callback(ch, method, properties, body):
    #message = body.split(',')
    print(body)

channel.basic_consume(callback,
                      queue=init_node+"I",
                      no_ack=True)


channel.start_consuming()
#while(True):
