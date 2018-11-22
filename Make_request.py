#!/usr/bin/env python
import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare('AB')

channel.basic_publish(exchange='',
					  routing_key='hello',
					  body='A,request')
connection.close()

#while(True):
