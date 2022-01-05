import socket

# setup

op = input("\nQual expressão deseja realizar: ")
host = "127.0.0.1"
port = 6789
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(1)

# comunicação com o server

try:
    s.sendto(bytes(op, "utf-8"), (host, port)) # manda pro server realizar a conta
    resp, local = s.recvfrom(1024) # recebe a resp realizada do server
    resp = resp.decode("utf-8")
    print(f"\nResposta que o client recebeu do server: {resp}\n")
    s.close()
except:
    print("Tempo excedido!\n Pode ter ocorrido algum erro durante a mensagem ao servidor!\n")