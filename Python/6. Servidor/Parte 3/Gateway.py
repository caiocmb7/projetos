import atexit
import socket
import threading
import parte3_pb2
import struct

def connectionThreadTCP(sock):
    # Accepts a connection request and stores both a socket object and its IP address
    while True:
        try:
            client, address = sock.accept()
        except:
            print("Ocorreu um erro com o IP ou Porta do servidor!")
            break
        print("{} has connected.".format(address[0]))
        threading.Thread(target=clientThreadTCP, args=(client,)).start()
        threading.Thread(target=receiveTCP, args=(client,)).start()

def clientThreadTCP(client):
    # Handles the client

    # Handles specific messages in a different way (user commands)
    while True:
        try:
            msg = input("Digite o dispostivo que voce quer mandar o comando: ")

            device_exists = 0
            for device in devicesTCP:
                if (msg == device):
                    device_exists = 1
            if(device_exists != 0):
                comando = input("Digite o comando que voce quer enviar: ")
                MESSAGETCP_SEND.msg = comando
                try:
                    devicesTCP[msg].send(MESSAGETCP_SEND.SerializeToString())
                except:
                    print("o comando nao existe")
            else:
                print("o dispositivo nao existe")

        except:
            print("erro")
            break
def receiveTCP(client):
    # Handles receiving messages from the server
    while True:
        try:
            msg = client.recv(2048)
            if (msg.decode("utf8") == "CONECTAR"):
              try:
                device = client.recv(2048).decode("utf8")
                devicesTCP[device] = client
                print("\n{} se conectou".format(device))
              except:
                print("An error occured in handshaking!")
            elif (msg.decode("utf8") != ''):
                MESSAGETCP_RECEIVE.ParseFromString(msg)
                print("\n" + MESSAGETCP_RECEIVE.msg)

        except:
            print("An error occured while receiving tcp mensage!")
            break

def receiveMultiCast(sock):
    # Receive the udp mensage, send to the device the ip and port of the tcp server
    # saves the ip port and name of the device in a list
    while True:
        try:
            data, address = sock.recvfrom(1024)
            data = data.decode("utf8")
            if data == "CONECTAR":
                try:
                    msg = host, port
                    print(msg)
                    sock.sendto((str(host)).encode("utf8"), address)
                    sock.sendto((str(port)).encode("utf8"), address)
                except:
                    print("An error occured while sending udp to device")
        except:
            print("An error occured while receiving from multicast")
            break

def main():
    global MESSAGETCP_SEND, MESSAGETCP_RECEIVE, host , port
    MESSAGETCP_RECEIVE = parte3_pb2.MESSAGE()
    MESSAGETCP_SEND = parte3_pb2.MESSAGE()

    # Multicast UDP PART:
    import socket
    import struct

    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    IS_ALL_GROUPS = True

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', MCAST_PORT))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    threadreceivingFromMulticast = threading.Thread(target=receiveMultiCast, args=(sock,))
    threadreceivingFromMulticast.start()

    #TCP PART:
    host = "127.0.0.1"
    port = 6789
    # Creates the socket for a TCP application
    socketFamily = socket.AF_INET
    socketType = socket.SOCK_STREAM
    serverSocket = socket.socket(socketFamily, socketType)
    # Binds the serverSocket at the specified port number
    serverSocket.bind((host, port))
    # Enables accepting connections
    serverSocket.listen()
    # Welcome message to the server owner
    print("Aguardando dispositivos")

    # Creates a thread for accepting incoming connections
    connThread = threading.Thread(target=connectionThreadTCP, args=(serverSocket,))
    connThread.start()
    # Waits for it to end
    connThread.join()
    # Performs socket connections cleanup
    # Closes the server socket object connection
    serverSocket.close()
    print("Server has shut down.")

# Dictionaries of devices and addresses with socket object as key

devicesTCP = {}

if __name__ == "__main__":
    main()
    pass