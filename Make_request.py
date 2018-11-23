#!/usr/bin/env python
import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare('BI')

channel.basic_publish(exchange='',
					  routing_key='hello',
					  body='B,request')
connection.close()

#while(True):
