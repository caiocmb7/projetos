#!/usr/bin/env python
import pika
import time
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='lum_sensor', exchange_type='direct')

while True:
    ruido = random.random() * random.randrange(-5, 5, 1)
    luminosity = 15 + ruido
    channel.basic_publish(
        exchange='', routing_key='lampada', body=str(luminosity))
    time.sleep(5)

connection.close()


connection.close()
