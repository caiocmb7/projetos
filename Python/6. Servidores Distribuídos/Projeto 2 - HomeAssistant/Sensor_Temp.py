#!/usr/bin/env python
import pika
import time
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='temp_sensor', exchange_type='direct')


while True:
    ruido = random.random() * random.randrange(-2, 2, 1)
    temperatura = 30 + ruido
    channel.basic_publish(exchange='temp_sensor',
                          routing_key='temp_sensor', body=str(temperatura))
    time.sleep(5)

connection.close()
