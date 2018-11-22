#!/usr/bin/env python
import pika
import sys
import time

"""myid = ""
holder = "" """
using = False
request_Q = []
asked = False

#On initialise le noeud, le premier argument est son id, le deuxieme est son holder
myid = sys.argv[1]
holder = sys.argv[2]

#On initie la connection et le channel
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

#On cree une queue par voisin, on inscrit manuellement le nom des queues
channel.queue_declare(queue=sys.argv[3])

if (len(sys.argv) > 3):
    channel.queue_declare(queue=sys.argv[4])
if (len(sys.argv) > 4):
    channel.queue_declare(queue=sys.argv[5])


#if not message_type:
#    print("error")
#    sys.exit(1)

#On definit la methode de callback principale
def callback(ch, method, properties, body):
    message = ','.join(body)
    sender_id = message[1]
    message_type = message[2]
    if message_type == "request":
        get_request(sender_id)
    elif message_type == "privilege":
        get_privilege(sender_id)


channel.basic_consume(callback,
                      queue=sys.argv[3],
                      no_ack=True)
channel.basic_consume(callback,
                      queue=sys.argv[4],
                      no_ack=True)
channel.basic_consume(callback,
                      queue=sys.argv[5],
                      no_ack=True)

channel.start_consuming()

#On definit la methode pour la reception des privileges
def get_request(sender_id):
    # transmission de request d'un noeud precedent au suivant
    if holder != myid and request_Q != [] and not asked:
        channel.queue_declare(queue=min(holder, myid) + max(holder, myid))
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body = myid + ',' + "request")
        request_Q.append(sender_id)
    # je suis holder et recois une request alors que je suis deja occupe avec la section critique
    elif holder == myid and request_Q != [] and request_Q[0] != myid:
        request_Q.append(sender_id)
        time.sleep(1000)
        give_privilege()
        request_Q.pop(0)
    # je suis holder et recoit une request et ne fais rien
    elif holder == myid and request_Q == []:
        give_privilege()

#On definit la methode pour donner les privileges
def give_privilege():
    # je suis holder et capable de donner le privilege (pas en section critique)
    if holder == myid and not using and request_Q != []:
        channel.queue_declare(queue= min(request_Q[0], myid) + max(request_Q[0], myid))
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body= request_Q[0] + ',' + "privilege")
        holder = request_Q[0]
        request_Q.pop(0)
        asked = False


def get_privilege():
    if request_Q[0] == myid:
        request_Q.pop[0]
        #todo entrée dans section critique
        using = True
        asked = False
        holder = myid
    else:
        give_privilege
        using = False