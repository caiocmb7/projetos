import socket

# setup

host = ""
port = 6789
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

# controle server-client
try:
    while True:
        print("Aguardando nova mensagem...\n")
        op, local = s.recvfrom(1024)
        resp = str(eval(op))
        print("----- Resposta da Calculadora -----\n")
        print(f"Resposta realizada na calculadora: {resp}\n")
        print("----- Cálculo realizado -----\n")

        s.sendto(bytes(resp, "utf-8"), local) # manda de volta pro client
except SyntaxError as SE:
    print(f"{SE}: Erro de Sintaxe, cuidado com os operadores ou digite algo caso não tenha digitado!\n")
except NameError as NE:
    print(f"{NE}: A expressão passada não são composta por números!\n")
except ZeroDivisionError as ZDE:
    print(f"{ZDE}: A expressão passada não pôde dividir por zero!\n")
except TypeError as TE:
    print(f"{TE}: A expressão passada não conseguiu ser calculada por conta do tipo str que foi passado!\n")
except:
    print("Algum erro ocorreu durante o cálculo, certifique sua expressão e tente novamente\n")