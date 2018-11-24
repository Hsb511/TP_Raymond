#!/usr/bin/env python
import pika
import sys
import time

using = False
request_Q = []
asked = False

#On initialise le noeud, le premier argument est son id, le deuxieme est son holder
myid = sys.argv[1]
print("node's id is: " + myid)
global holder
holder = sys.argv[2]
print("node's holder is: " + holder)

#On initie la connection et le channel
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

#On cree une queue par voisin, on inscrit manuellement le nom des queues
neighbor1 = sys.argv[3]

channel.queue_declare(queue=neighbor1+myid)
print("node " + myid + " is listening to " + neighbor1)
channel.queue_declare(queue=myid+neighbor1)
print("node " + myid + " is writing on " + myid + neighbor1)

#On cree les queues avec le voisin "I"
channel.queue_declare(queue="I"+myid)
print("node " + myid + " is listening to " + "I")
channel.queue_declare(queue=myid+"I")
print("node " + myid + " is writing on " + myid + "I")


if (len(sys.argv) > 4):
    channel.queue_declare(queue=sys.argv[4] + myid)
    print("node " + myid + " is listening to " + sys.argv[4])
    channel.queue_declare(queue=myid + sys.argv[4])
    print("node " + myid + " is writing on " + myid + sys.argv[4])

if (len(sys.argv) > 5):
    channel.queue_declare(queue=sys.argv[5] + myid)
    print("node " + myid + " is listening to " + sys.argv[5])
    channel.queue_declare(queue=myid + sys.argv[5])
    print("node " + myid + " is writing on " + myid + sys.argv[5])


#if not message_type:
#    print("error")
#    sys.exit(1)

#On definit la methode pour donner les privileges
def give_privilege(holder):
    print ("trying give privilege to " + request_Q[0])
    # je suis holder et capable de donner le privilege (pas en section critique)
    if holder == myid and not using and request_Q != []:
        #channel.queue_declare(queue= min(request_Q[0], myid) + max(request_Q[0], myid))
        channel.basic_publish(exchange='',
                              routing_key=myid+request_Q[0],
                              body= request_Q[0] + ',' + "privilege")
        holder = request_Q[0]
        request_Q.pop(0)
        asked = False
        print("done")
    else: print("condition not accepted to do so")


#On definit la methode pour la reception des privileges
def get_request(sender_id):
    print ("just received a request, holder is: "+holder+ " sender_id is: "+ sender_id +" , request_Q : ", request_Q, " , asked : ", asked)
    # transmission de request d'un noeud precedent au suivant
    if holder != myid and request_Q != [] and not asked:
        #channel.queue_declare(queue=min(holder, myid) + max(holder, myid))
        channel.basic_publish(exchange='',
                              routing_key=myid+holder,
                              body = myid + ',' + "request")
        request_Q.append(sender_id)
        print("request transmission done")
    # je suis holder et recois une request alors que je suis deja occupe avec la section critique
    elif holder == myid and request_Q != [] and request_Q[0] != myid:
        request_Q.append(sender_id)
        time.sleep(1000)
        give_privilege(holder)
        request_Q.pop(0)
        print("i'm already doing sthg")
    # je suis holder et recoit une request et ne fais rien
    elif holder == myid and request_Q == []:
	request_Q.append(sender_id)
        give_privilege(holder)
        print("just gave privilege")
    elif holder != myid and request_Q == []:
        request_Q.append(sender_id)
        print("initiating a request on queue: "+min(holder, myid) + max(holder, myid))
        #channel.queue_declare(queue=min(holder, myid) + max(holder, myid))
        #channel.queue_delete(queue=myid+"I")
        channel.basic_publish(exchange='',
                              routing_key=myid+holder,
                              body = myid + ',' + "request")
        print("just made request")

def get_privilege(holder):
    print("just received privilege")
    #channel.queue_declare(queue=myid+"I")
    channel.basic_publish(exchange='', routing_key=myid+"I", body="[x] "+myid+" is the current holder of the privilege")
    if request_Q[0] == myid:
        request_Q.pop(0)
        #todo entree dans section critique
        using = True
        asked = False
        holder = myid
        print("i'm using it")
	
	channel.stop_consuming()
	#channel.queue_declare(queue=min("I", myid) + max("I", myid))
        
        channel.basic_publish(exchange='',
                              routing_key=myid+'I',
                              body = myid + " : i'm the captain now" )

    else:
        holder = myid
        give_privilege(holder)
        print("just gave privilege")
        using = False

#On definit la methode de callback principale
def callback(ch, method, properties, body):
    message = body.split(',')
    print(message)
    sender_id = message[0]
    message_type = message[1]
    print("[x] message received from " + sender_id + " of type " + message_type)
    if message_type == "request":
        get_request(sender_id)
    elif message_type == "privilege":
        get_privilege(holder)


channel.basic_consume(callback,
                      queue="I"+myid,
                      no_ack=True)

channel.basic_consume(callback,
                      queue=neighbor1+myid,
                      no_ack=True)

if (len(sys.argv) > 4):
	channel.basic_consume(callback,
                      queue=sys.argv[4]+myid,
                      no_ack=True)

if (len(sys.argv) > 5):
	channel.basic_consume(callback,
                      queue=sys.argv[5]+myid,
                      no_ack=True)

channel.start_consuming()














