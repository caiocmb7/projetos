import parte3_pb2 as proto
import socket
import threading
import sys

def main():
    global AC, threadFlagUDP, MESSAGE, clientSocket, host , port
    threadFlagUDP = True

    AC = proto.AC()
    setACConnectionState(proto.DEVICE_IDLE)
    AC.temperature = 20
    MESSAGE = proto.MESSAGE()

    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Send to multicast the requisition every 1 sec
    sendMultiCastPeriodic(sock, MCAST_GRP, MCAST_PORT, 1)

    threadreceivingFromMulticast = threading.Thread(target=receiveMultiCast, args=(sock,))
    threadreceivingFromMulticast.start()

    while threadreceivingFromMulticast.is_alive() and AC.conection_state == proto.DEVICE_IDLE:
        continue

    threadFlagUDP = False

    # Creates two threads for sending and receiving messages from the server
    threadreceivingTCP = threading.Thread(target=receiveTCP, args=(clientSocket,))
    threadreceivingTCP.start()
    while threadreceivingTCP.is_alive() and AC.conection_state == proto.DEVICE_CONNECTED:
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

def receiveMultiCast(sock):
    global host,port, clientSocket
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
            setACConnectionState(proto.DEVICE_CONNECTED)
            try:
                clientSocket.send(("CONECTAR").encode("utf8"))
                clientSocket.send(("AC").encode("utf8"))

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
            if MESSAGE.msg == "ligar ac":
                TurnOnAC()
            elif MESSAGE.msg == "desligar ac":
                TurnOffAC()
            elif MESSAGE.msg == "estado ac":
                StateAC()
            elif MESSAGE.msg == "Aumentar temperatura":
                AumentarTempAC()
            elif MESSAGE.msg == "Baixar temperatura":
                BaixarTempAC()
            elif MESSAGE.msg == "Temperatura":
                TempAC()
        except:
            print("An error occured while trying to receive TCP from the server!")
            break

def setACConnectionState(ConnectionState):
    AC.conection_state = ConnectionState

def TurnOnAC():
    AC.state = "on"
    msg = "O AC foi ligado"
    sendTCP(msg)


def TurnOffAC():
    AC.state = "off"
    msg = "O AC foi desligado"
    sendTCP(msg)


def StateAC():
    msg = "O AC está {}".format(AC.state)
    sendTCP(msg)

def AumentarTempAC():
    AC.temperature = AC.temperature + 1
    msg = "A temperatura do AC agora eh: {}".format(AC.temperature)
    sendTCP(msg)

def BaixarTempAC():
    AC.temperature = AC.temperature - 1
    msg = "A temperatura do AC agora eh: {}".format(AC.temperature)
    sendTCP(msg)

def TempAC():
    msg = "A temperatura do AC agora eh: {}".format(AC.temperature)
    sendTCP(msg)

if __name__ == "__main__":
    main()
    pass


