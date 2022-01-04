import os
import shutil
from PIL import Image 

# função para a realização da transformação das imagens para png
def png_to_jpg():
    for filename in os.listdir(input_path):
        current_img = Image.open(input_path + '\\' + filename)
        current_img.save(input_path + '\\' +
                        filename + '.png', 'PNG')
    print("\n---- Realizando a transformação JPG para PNG ----")
    print("\n Transformação finalizada!")
    print("\n --------------------")

# função para a transferir as imagens transformadas para outra pasta
def mover_imagens():
    os.chdir(input_path)
    imagens_destino = input_path + "\\imagens_transformadas"

    try:
        os.makedirs(input_path + "\\imagens_transformadas")
    except FileExistsError as Err:
        print(f"A Pasta {imagens_destino} já existe.")

    files = os.listdir(input_path)

    for f in files:
        if (f.endswith(".png")):
            shutil.move(f, input_path + "\\imagens_transformadas")
    print("\n---- Separando os arquivos transformados em outra pasta ----")
    print("\n Separação finalizada!")
    print('\n Imagens transformadas e transferidas para a pasta "imagens_transformadas"')
    print("\n --------------------")

if __name__ == "__main__":
    input_path = str(input("Qual o caminho da pasta: "))
    png_to_jpg()
    mover_imagens()