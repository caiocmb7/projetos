from random import choice

def sorteador(lista):
    for i in range(len(lista)):
        escolha = choice(lista)
        print(f"{i+1}:", escolha)
        lista.remove(escolha)
    
    return lista

if __name__ == "__main__":
    palavras = input("Digite os elementos que deseja sortear, separando-os por um espaço: ")
    lista = palavras.split(" ")
    sorteador(lista)