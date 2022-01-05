import sys
import socket
import colorama
import threading

# Essa função faz deletar a ultima linha para que fique melhor a visualização do chat
def deleteLastLine():
    cursorUp = "\x1b[1A"
    eraseLine = "\x1b[2K"
    sys.stdout.write(cursorUp)
    sys.stdout.write(eraseLine)

def send(sock):
    while threadFlag:
        try:
            message = input()
            deleteLastLine()
            sock.send(message.encode("utf8"))
        except:
            print("Erro durante a mensagem! Possivelmente servidor cheio!")
            break

def receive(sock):
    while threadFlag:
        try:
            message = sock.recv(2048).decode()
            if message:
                print("{}".format(message))
            else:
                break
        except:
            print("Erro durante o acesso ao servidor!")
            break

def main():
    global threadFlag

    # colorama
    colorama.init()
    
    # conexão
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        print("Bem vindo a nossa aplicação, esses são seus comandos:")
        print("/ENTRAR para conectar ao server")
        print("/SAIR para sair do server")
        print("/NICKS para mudar seu nick")
        print("/USUARIOS para saber quem esta conectado ao server")

        comando = input("\n Digite seu comando: ")

        if comando == "/ENTRAR":
            host = str(input("Digite o ip do servidor "))
            port = int(input("Digite a porta do servidor:"))
            try:
                clientSocket.connect((host, port))
                break
            except:
                print("O ip ou porta não existe!")
            else:
                break
        else:
            print("Você precisa primeiro entrar no server para usar os outros comandos")

    # Thread
    thread_envio = threading.Thread(target=send, args=(clientSocket,))
    thread_receber = threading.Thread(target=receive, args=(clientSocket,))
    thread_receber.start()
    thread_envio.start()

    # Manutenção da thread
    while thread_receber.is_alive() and thread_envio.is_alive():
        continue
    threadFlag = False

    # Fechar conexão
    clientSocket.close()
    print("\nServidor Cheio ou você saiu do chat!")

threadFlag = True

if __name__ == "__main__":
    main()
    pass