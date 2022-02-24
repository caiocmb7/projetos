#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='smoke_sensor', exchange_type='direct')

channel.queue_declare(queue='sensor_fumaca')

while True:
    fumaca_state = 0
    channel.basic_publish(exchange='smoke_sensor',
                          routing_key='sensor_fumaca', body=str(fumaca_state))
    time.sleep(5)

connection.close()
