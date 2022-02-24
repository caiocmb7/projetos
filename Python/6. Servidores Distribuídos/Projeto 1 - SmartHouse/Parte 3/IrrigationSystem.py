import parte3_pb2 as proto
import socket
import threading
import sys


def main():
    global IrrigationSystem, threadFlagUDP, MESSAGE, clientSocket, host, port
    threadFlagUDP = True

    IrrigationSystem = proto.IrrigationSystem()
    setIrrigationSystemConnectionState(proto.DEVICE_IDLE)

    MESSAGE = proto.MESSAGE()

    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Send to multicast the requisition every 1 sec
    sendMultiCastPeriodic(sock, MCAST_GRP, MCAST_PORT, 1)

    threadreceivingFromMulticast = threading.Thread(target=receiveMultiCast, args=(sock,))
    threadreceivingFromMulticast.start()

    while threadreceivingFromMulticast.is_alive() and IrrigationSystem.conection_state == proto.DEVICE_IDLE:
        continue

    threadFlagUDP = False

    # Creates two threads for sending and receiving messages from the server
    threadreceivingTCP = threading.Thread(target=receiveTCP, args=(clientSocket,))
    threadreceivingTCP.start()
    print("linha 35")
    sendStatePeriodic(30)
    print("linha 36")
    while threadreceivingTCP.is_alive() and IrrigationSystem.conection_state == proto.DEVICE_CONNECTED:
        continue
        print("teste linha 37")
    threadFlagTCP = False


def sendMultiCastPeriodic(sock, MCAST_GRP, MCAST_PORT, period):
    # Handles sending messages to the server
    def MultiCastPeriodicthread():
        if threadFlagUDP:
            try:
                sock.sendto(("CONECTAR").encode("utf8"), (MCAST_GRP, MCAST_PORT))
            except:
                print("An error occured while trying to send a message!")
            finally:
                threading.Timer(period, MultiCastPeriodicthread).start()

    MultiCastPeriodicthread()


def sendStatePeriodic(period):
    # Handles sending messages to the server
    def sendStatePeriodicthread():
        if IrrigationSystem.state == "on":
            try:
                StateIrrigationSystem()
                print("aqui")
            except:
                print("An error occured in sendStatePeriodic messages!")
        threading.Timer(period, sendStatePeriodicthread).start()

    sendStatePeriodicthread()


def receiveMultiCast(sock):
    global host, port, clientSocket
    # Handles receiving messages from the server
    while threadFlagUDP:
        try:
            host = sock.recv(2048).decode("utf8")
            port = int(sock.recv(2048).decode("utf8"))

            print(host, port)
            # Creates the socket for a TCP application
            socketFamily = socket.AF_INET
            socketType = socket.SOCK_STREAM
            clientSocket = socket.socket(socketFamily, socketType)

            # Connects to the server
            clientSocket.connect((host, port))
            setIrrigationSystemConnectionState(proto.DEVICE_CONNECTED)
            try:
                clientSocket.send(("CONECTAR").encode("utf8"))
                clientSocket.send(("SISTEMA DE IRRIGACAO").encode("utf8"))

            except:
                print("erro no handshaking")
        except:
            print("An error occured while trying to connect to tcp server!")
            break


def sendTCP(msg):
    # Handles sending messages to the server
    try:
        MESSAGE.msg = msg
        clientSocket.send(MESSAGE.SerializeToString())
    except:
        print("An error occured while trying to send a TCP message!")


def receiveTCP(clientSocket):
    # Handles receiving messages from the server
    while True:
        try:
            msg = clientSocket.recv(2048)
            MESSAGE.ParseFromString(msg)
            if MESSAGE.msg == "ligar sistema de irrigacao":
                TurnOnIrrigationSystem()
            elif MESSAGE.msg == "desligar sistema de irrigacao":
                TurnOffIrrigationSystem()
            elif MESSAGE.msg == "estado sistema de irrigacao":
                StateIrrigationSystem()
        except:
            print("An error occured while 5 trying to reach the server!")
            break


def setIrrigationSystemConnectionState(ConnectionState):
    IrrigationSystem.conection_state = ConnectionState


def TurnOnIrrigationSystem():
    IrrigationSystem.state = "on"
    msg = "o sistema de irrigacao foi ligado "
    sendTCP(msg)


def TurnOffIrrigationSystem():
    IrrigationSystem.state = "off"
    msg = "O sistema de irrigacao foi desligado"
    sendTCP(msg)


def StateIrrigationSystem():
    msg = "o sistema de irrigacao está {}".format(IrrigationSystem.state)
    sendTCP(msg)


if __name__ == "__main__":
    main()
    pass
