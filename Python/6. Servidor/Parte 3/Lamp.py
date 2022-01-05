import parte3_pb2 as proto
import socket
import threading

def main():
    global lamp, threadFlagUDP, MESSAGE, clientSocket, host , port
    threadFlagUDP = True

    lamp = proto.lamp()
    setLampConnectionState(proto.DEVICE_IDLE)

    MESSAGE = proto.MESSAGE()

    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Send to multicast the requisition every 1 sec
    sendMultiCastPeriodic(sock, MCAST_GRP, MCAST_PORT, 1)

    threadreceivingFromMulticast = threading.Thread(target=receiveMultiCast, args=(sock,))
    threadreceivingFromMulticast.start()

    while threadreceivingFromMulticast.is_alive() and lamp.conection_state == proto.DEVICE_IDLE:
        continue

    threadFlagUDP = False

    # Creates two threads for sending and receiving messages from the server
    threadreceivingTCP = threading.Thread(target=receiveTCP, args=(clientSocket,))
    threadreceivingTCP.start()
    while threadreceivingTCP.is_alive() and lamp.conection_state == proto.DEVICE_CONNECTED:
        continue
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
            setLampConnectionState(proto.DEVICE_CONNECTED)
            try:
                clientSocket.send(("CONECTAR").encode("utf8"))
                clientSocket.send(("LAMPADA").encode("utf8"))

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
            if MESSAGE.msg == "ligar lampada":
                TurnOnLamp()
            elif MESSAGE.msg == "desligar lampada":
                TurnOffLamp()
            elif MESSAGE.msg == "estado lampada":
                StateLamp()
        except:
            print("An error occured while 5 trying to reach the server!")
            break

def setLampConnectionState(ConnectionState):
    lamp.conection_state = ConnectionState

def TurnOnLamp():
    lamp.state = "on"
    msg = "A lampada foi ligada "
    sendTCP(msg)


def TurnOffLamp():
    lamp.state = "off"
    msg = "A lampada foi desligada"
    sendTCP(msg)

def StateLamp():
    msg = "A lampada está {}".format(lamp.state)
    sendTCP(msg)


if __name__ == "__main__":
    main()
    pass
