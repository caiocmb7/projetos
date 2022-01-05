import atexit
import socket
import threading

def connectionThread(sock):
    while True:
        try:
            client, address = sock.accept()
        except:
            print("Ocorreu um erro com o IP ou Porta do servidor!")
            break
        print("{} conectou-se.".format(address[0]))
        addresses[client] = address
        threading.Thread(target=clientThread, args=(client,)).start()

def clientThread(client):
    address = addresses[client][0]
    try:
       user = Nickname(client)
    except:
        print("Ocorreu um erro durante o processo, cheque o nickname ou servidor cheio está cheio! {}!".format(address))
        del addresses[client]
        client.close()
        return
    print("{} entrou com nick de {}!".format(address, user))
    users[client] = user
    
    try:
        client.send("Olá {}! Você conectou-se ao servidor".format(user).encode("utf8"))
    except:
        print("Erro! {} ({}).".format(address, user))
        del addresses[client]
        del users[client]
        client.close()
        return
    broadcast("{} entrou no chat!".format(user))

    while True:
        try:
            message = client.recv(2048).decode("utf8")
            if message == "/SAIR":
                client.send("Você saiu do chat!".encode("utf8"))
                del addresses[client]
                del users[client]
                client.close()
                print("{} ({}) saiu.".format(address, user))
                broadcast("{} saiu do chat.".format(user))
                break
            elif message == "/USUARIOS":
                lista_usuarios = ', '.join([user for user in sorted(users.values())])
                client.send("Os usuários conectados são: {}".format(lista_usuarios).encode("utf8"))
            elif message == "/NICK":
                client.send("Deseja trocar seu nick para qual?".encode("utf8"))
                new_nickname = client.recv(2048).decode("utf8")
                antigo = users[client]
                nick_usado = False
                if new_nickname in users.values():
                    nick_usado = True
                    while nick_usado:
                        client.send("Esse nick já está sendo usado, tente novamente com outro:".encode("utf8"))
                        new_nickname = client.recv(2048).decode("utf8")
                        if new_nickname not in users.values():
                                nick_usado = False
                                users[client] = new_nickname
                                user = new_nickname
                print("{} trocou o nick para {}.".format(antigo, users[client]))
                broadcast("{} trocou o nick para {}.".format(antigo, users[client]))
            else:
                print("({}): {}".format(user, message))
                broadcast(message, user)
        except:
            print("{} ({}) saiu.".format(address, user))
            del addresses[client]
            del users[client]
            client.close()
            broadcast("{} saiu do chat.".format(user))
            break

def Nickname(client):
    if len(list(users.values())) >= 4:
        print("\nServidor Cheio!")
        client.close()

    client.send("Escolha seu nickname pro chat:".encode("utf8"))
    nickname = client.recv(2048).decode("utf8")
    nick_usado = False
    if nickname in users.values():
        nick_usado = True
        while nick_usado:
            client.send("Esse nick já está sendo usado, tente novamente com outro:".encode("utf8"))
            nickname = client.recv(2048).decode("utf8")
            if nickname not in users.values():
                nick_usado = False
    return nickname

def broadcast(message, sentBy = ""):
    try:
        if sentBy == "":
            for user in users:
                user.send(message.encode("utf8"))
        else:
            for user in users:
                user.send("{}: {}".format(sentBy, message).encode("utf8"))
    except:
        print("Erro na mensagem!")

def limpeza():
    if len(addresses) != 0:
        for sock in addresses.keys():
            sock.close()
    print("Limpeza feita.")

def main():
    # Limpeza
    atexit.register(limpeza)

    # IP/Port
    host = "127.0.0.1"
    port = 6789

    # config
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen()
    print("Aguardando comandos ...")

    # Thread
    connThread = threading.Thread(target=connectionThread, args=(serverSocket,))
    connThread.start()
    connThread.join()

    # Limpeza
    limpeza()

    # Fechar
    serverSocket.close()
    print("Server desligado.")

users = {}
addresses = {}

if __name__ == "__main__":
    main()
    pass