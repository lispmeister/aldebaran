#!/usr/bin/env python
# This file was auto-generated via org-babel-tangle in Emacs
# Do not modify this file manually. Instead modify the source
# in aldebaran.org and re-run org-babel-tangle
#
# Usage: ./declare-2.py -s localhost 
#

import pika
import uuid
import arrow
import time
import sys
import argparse

def declare_exchanges(channel):
  channel.exchange_declare(exchange='Aldebaran.Trade_Data', 
                           exchange_type='direct', durable=True)
  channel.exchange_declare(exchange='Aldebaran.Work', 
                           exchange_type='direct', durable=True)
  channel.exchange_declare(exchange='Aldebaran.Alert', 
                           exchange_type='direct', durable=True)

def declare_queues(channel):
  channel.queue_declare(queue='Aldebaran.Trade_Data', durable=True)
  channel.queue_declare(queue='Aldebaran.Work', durable=True)
  channel.queue_declare(queue='Aldebaran.Alert', durable=True)

def bind_queues(channel):
  channel.queue_bind('Aldebaran.Trade_Data', 'Aldebaran.Trade_Data' , 
                     routing_key='Aldebaran.Trade_Data', nowait=False, arguments=None)
  channel.queue_bind('Aldebaran.Work', 'Aldebaran.Work' , 
                     routing_key='Aldebaran.Work', nowait=False, arguments=None)
  channel.queue_bind('Aldebaran.Alert', 'Aldebaran.Alert' , 
                     routing_key='Alert', nowait=False, arguments=None)

def main():
  parser = argparse.ArgumentParser(
           description='Declare exchanges and queues.')
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
  print 'Declaring exchanges and queues on the RabbitMq server.'
  declare_exchanges(channel)
  declare_queues(channel)
  bind_queues(channel)
  channel.close()
  connection.close()

if __name__ == "__main__":
  main()
