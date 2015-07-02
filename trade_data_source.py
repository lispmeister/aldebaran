#!/usr/bin/env python
#!/usr/bin/env python
# This file was auto-generated via org-babel-tangle in Emacs
# Do not modify this file manually. Instead modify the source
# in aldebaran.org and re-run org-babel-tangle
#
# Usage: ./trade_data_source.py -s localhost 
#

import pika
import uuid
import arrow
import time
import sys
import argparse
import json
import random

def create_purchase_request(limit):
  fields = {}
  fields['id'] = str(uuid.uuid4())
  fields['#shares'] = limit
  fields['client'] = 'Goldman'
  fields['stock'] = 'AAPL'
  return fields

def create_purchase(order_id, shares):
  fields = {}
  fields['id'] = str(uuid.uuid4())
  fields['initial_order_id'] = order_id
  fields['#shares'] = shares
  fields['client'] = 'Goldman'
  fields['stock'] = 'AAPL'
  return fields

def publish_purchase_request(channel, pr):
  print ('Purchase Request: %s' % json.dumps(pr))
  channel.basic_publish(exchange='Aldebaran.Trade_Data',
                        routing_key='Aldebaran.Trade_Data', body=json.dumps(pr))

def publish_purchase(channel, p):
  print ('Purchase: %s' % json.dumps(p))
  channel.basic_publish(exchange='Aldebaran.Trade_Data',
                        routing_key='Aldebaran.Trade_Data', body=json.dumps(p))

def publish(channel):
  limit = (random.randint(50, 100))
  amounts = [int(limit / 2 * random.random()) for i in xrange(4)]
  pr = create_purchase_request(limit)
  publish_purchase_request(channel, pr)
  order_id = pr['id']
  for a in amounts:
    p = create_purchase(order_id, a)
    publish_purchase(channel, p)

def main():
  parser = argparse.ArgumentParser(
           description='Loop sending events to RabbitMq with at a rate of 1Hz.')
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
  print 'Sending event to RabbitMq server. To exit press CTRL+C.'
  while ( 1 ):
    publish(channel)
    time.sleep( 1 )
  channel.close()
  connection.close()

if __name__ == "__main__":
  main()
