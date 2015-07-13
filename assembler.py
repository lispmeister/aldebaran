#!/usr/bin/env python
# This file was auto-generated via org-babel-tangle in Emacs
# Do not modify this file manually. Instead modify the source
# in aldebaran.org and re-run org-babel-tangle
#
# Usage: ./assembler.py -s localhost
#

import pika
import arrow
import sys
import argparse 
import json

def keyCheck(arr, key):
  """If the key can be found in the dictionary
     we return the first element otherwise None.
  """
  if key in arr.keys():
    return arr[key]
  else:
    return None

def keyExists(arr, key):
  """Return True if the dictionary contains the key,
     return false otherwise
  """
  if (keyCheck(arr, key)) == None:
    return False
  else:
    return True

def isPurchaseEvent(event):
  """If the event contains a key named 'initial_order_id' it is
     a purchase event and we return True. Otherwise  it is a
     purchase request event and we return False.
  """
  if (keyExists(event, 'initial_order_id')):
    return True
  else:
    return False

def parseMessage(body):
   return json.loads(body)

def publishPurchase(P):
  """Set routing_key 'purchase' and publish the event
     to the default exchange with a routing key of 
     "Aldebaran.<initial_order_id>".
  """
  queue_name = "Aldebaran." + keyCheck(P, 'initial_order_id') 
  channel.queue_declare(queue=queue_name,durable=True)
  channel.basic_publish(exchange='',
                        routing_key=queue_name, json.dumps(P))

def publishPurchaseRequest(PR):
  """Set routing_key 'Aldebaran.Work' and publish the event 
     to the Aldebaran.Work exchange. Set routing_key to 'Aldebaran.<id>'
     and publish to default exchange.
  """
  queue_name = "Aldebaran." + keyCheck(event, 'id')
  channel.queue_declare(queue=queue_name,durable=True)
  channel.basic_publish(exchange='',
                        routing_key=queue_name, json.dumps(PR))
  channel.basic_publish(exchange='Aldebaran.Work',
                        routing_key='Aldebaran.Work', json.dumps(PR))

def callback(channel, method_frame, header_frame, body):
#  print "method_frame: %s" % (method_frame, )
#  print "header_frame: %s" % (header_frame, )
#  print "body: %s" % (body, )
  event = parseMessage(body)
#  print "body parsed: %s" % (event, )
  print "Is purchase event: %s" % (isPurchaseEvent(event), )
  if isPurchaseEvent(event):
    publishToPurchaseExchange(event)
  else:
    publishToPurchaseRequestExchange(event)
  channel.basic_ack(method_frame.delivery_tag)

def main():
  parser = argparse.ArgumentParser(
           description='Consume Trade Data and route to appropriate exchanges.')
  parser.add_argument('-s', metavar='rabbitmq', default='localhost',
                      help='The IP or DNS name of the RabbitMq server')
  args = parser.parse_args()
  myrabbit = args.s
  # connect to RabbitMq
  try:
    connection = pika.BlockingConnection(
                 pika.ConnectionParameters(host=myrabbit,heartbeat_interval=20))
  except Exception as err:
    print('Cant connect to RabbitMq. Reason: %s' % err)
    exit(1)
  channel = connection.channel()
  print ' [*] Waiting for events. To exit press CTRL+C'
  channel.basic_consume(callback, queue='Aldebaran.Trade_Data', no_ack=False)
  channel.start_consuming()

if __name__ == "__main__":
  main()
