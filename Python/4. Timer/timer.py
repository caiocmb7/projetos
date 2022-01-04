import time

def contador_tempo(t):
    while t:
        #receber o tempo e dividir em 60 para identificar min, seg
        minutos, segundos = divmod(t, 60) 
        timer = "{:02d}:{:02d}".format(minutos, segundos)

        #printar na msm linha
        print(timer, end="\r") 
        time.sleep(1)
        t -= 1
    print("\n Contagem realizada")

if __name__ == "__main__":
    t = input("Digite um valor em segundos: ")
    contador_tempo(int(t))