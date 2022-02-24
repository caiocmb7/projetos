import socket
import threading
import grpc
import pika
import sys
import os
# import the generated classes
import lampada_pb2
import lampada_pb2_grpc
# import the generated classes
import ar_pb2
import ar_pb2_grpc
# import the generated classes
import exaustor_pb2
import exaustor_pb2_grpc
import json
# Conexao socket
IP = "127.0.0.1"
PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((str(IP), int(PORT)))
sock.listen(10)
sock.setblocking(False)
dispositivos = []

# Inicializando os sensores

# Lampada
sensor_iluminacao = []
sensor_iluminacao.append(0)
lampada_valor = []
lampada_valor.append(0)

# Ar
ar_sensor = []
ar_sensor.append(0)
ar_valor = []
ar_valor.append(0)

# Fumaca
fumaca_sensor = []
fumaca_sensor.append(0)
fumaca_valor = []
fumaca_valor.append(0)


def form_procediment(y):
    if int(y['lampada']) == 1:
        comando = 'ligar'
        lampada(comando)
    else:
        comando = 'desligar'
        lampada(comando)

    if int(y['ar']) == 1:
        ar(float(y['temperatura']))
    else:
        ar(0)

    if int(y['exaustor']) > 0:
        print("138")
        print(y['exaustor'])
        exaustor(int(y['exaustor']))
    else:
        exaustor(int(y['exaustor']))


def Aceitar_conexao():
    print("Aceitar_conexao iniciado \n")
    global sensor_iluminacao
    global lampada_valor
    global dispositivos
    global sock
    while True:
        try:
            stauts_exaustor = ""
            conn, addr = sock.accept()
            conn.setblocking(False)
            dispositivos.append(conn)
            valorluminosidade = int(lampada_valor[len(
                lampada_valor)-1]) - int(sensor_iluminacao[len(sensor_iluminacao)-1])

            if int(ar_valor[len(ar_valor)-1]) >= 0 and len(ar_valor) > 1:
                valortemperatura = int(ar_valor[len(ar_valor)-1])
            else:
                valortemperatura = ar_sensor[len(ar_sensor)-1]

            if valorluminosidade < 0:
                valorluminosidade *= -1

            if len(fumaca_valor) > 1:

                if fumaca_valor[len(fumaca_valor)-1] >= 1:
                    stauts_exaustor = "Ligado"
                else:
                    stauts_exaustor = "Desligado"

            else:

                if fumaca_sensor[len(fumaca_sensor)-1] >= 1:
                    stauts_exaustor = "Ligado"
                else:
                    stauts_exaustor = "Desligado"

            conn.send(('HTTP/1.0 200 OK\n').encode('utf-8'))
            conn.send(('Content-Type: text/html\n').encode('utf-8'))
            conn.send(('\n').encode('utf-8'))
            conn.send(("""
                <html style="background-color: rgb(3, 175, 255);">

                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>

                <body>
                    <div>
                        <div style="text-align: center;margin-top: 230px;font-family:fantasy">
                            <h1 style="color: white;font-size: 90px;;">SISTEMAS DISTRIBUÍDOS</h1>
                            <h1 style="color: white;font-size: 50px;">Trabalho 3</h1>
                            <br>
                            <br>
                            <div style="background-color: rgb(216, 168, 10); border-radius: 30px;width: 600px;margin-left: 34%;">
                                <h2 style="color: white;font-size: 25px;">Nivel de luminosidade: {}</h2>
                                <h2 style="color: white;font-size: 25px;">Exaustor: {}</h2>
                                <h2 style="color: white;font-size: 25px;">Temperatura (C°): {}</h2>
                                <br><a href="http://localhost:8080/" style="color: rgb(7, 0, 0);font-size: 50px;">Modificar Estado</a>
                            </div>

                        </div>
                    </div>

                </body>

                </html>

			""").format(valorluminosidade, stauts_exaustor, valortemperatura).encode('utf-8'))
        except:
            pass


def Processar_Conexao():
    print("Processar_Conexao iniciado")
    global dispositivos
    while True:
        if len(dispositivos) > 0:
            for dispositivo in dispositivos:
                try:
                    data = dispositivo.recv(1024)
                    disp_msg = data.decode('utf-8')
                    if data:
                        msg = json.loads(disp_msg)
                        print(msg)
                        form_procediment(msg)
                except:
                    pass


def sub_lampada():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='lum_sensor', exchange_type='direct')

    result = channel.queue_declare(queue='lum_sensor', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='lum_sensor', queue=queue_name)

    def callback(ch, method, properties, body):
        luminosity = int(float(body.decode()))
        global sensor_iluminacao
        sensor_iluminacao.append(luminosity)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def sub_ar():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='temp_sensor', exchange_type='direct')

    result = channel.queue_declare(queue='temp_sensor', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='temp_sensor', queue=queue_name)

    def callback(ch, method, properties, body):
        temp = int(float(body.decode()))
        global ar_sensor
        ar_sensor.append(temp)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def sub_fumaca():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='smoke_sensor', exchange_type='direct')

    result = channel.queue_declare(queue='smoke_sensor', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='smoke_sensor', queue=queue_name)

    def callback(ch, method, properties, body):
        fumaca_state = body.decode()

        global fumaca_sensor
        fumaca_sensor.append(int(fumaca_state))

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def exaustor(comando):

    channel = grpc.insecure_channel('localhost:50053')
    stub = exaustor_pb2_grpc.ExaustorStub(channel)
    # create a valid request message
    if float(comando) >= 0:
        status = exaustor_pb2.StatusExaustor(status=float(comando))
        # make the call
        response = stub.ligarExaustor(status)
    else:
        status = exaustor_pb2.StatusExaustor(status=float(comando))
        # make the call
        response = stub.desligarExaustor(status)

    fumaca_valor.append(response.status)


def ar(comando):
    channel = grpc.insecure_channel('localhost:50052')
    stub = ar_pb2_grpc.ArStub(channel)

    if float(comando) > 0:
        status = ar_pb2.ArTemperatura(temperatura=float(comando))
        # make the call
        response = stub.ligarAr(status)
    else:
        status = ar_pb2.ArTemperatura(temperatura=-1)
        # make the call
        response = stub.desligarAr(status)

    ar_valor.append(response.temperatura)
    # print(ar_valor)


def lampada(comando):
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')
    # create a stub (client)
    stub = lampada_pb2_grpc.LampadaStub(channel)
    # create a valid request message
    status = lampada_pb2.LampadaStatus(stauts=1)
    # make the call

    if comando == 'desligar':
        response = stub.desligarLampada(status)
    else:
        response = stub.ligarLampada(status)

    lampada_valor.append(response.stauts)


t = threading.Thread(target=sub_lampada)
t.start()

t2 = threading.Thread(target=sub_ar)
t2.start()
# sub_fumaca

t3 = threading.Thread(target=sub_fumaca)
t3.start()

accept_Con = threading.Thread(target=Aceitar_conexao)
accept_Con.start()

process_Con = threading.Thread(target=Processar_Conexao)
process_Con.start()

while True:
    try:

        comando = input('')

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
            sock.close()
        except SystemExit:
            sock.close()
            os._exit(0)
