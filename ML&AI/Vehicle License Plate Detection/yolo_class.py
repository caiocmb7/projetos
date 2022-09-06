# imports

#import pytesseract
import cv2
import matplotlib.pyplot as plt
#from IPython.display import Image
import warnings
import os
import pandas as pd
warnings.filterwarnings('ignore')

# A Sample class with init method
class Car:

  # init method or constructor
  def __init__(self):
      pass

    # read .txt to get x,y,w,h of ALPR
  def __read_txt(self, filepath):
    f = open(filepath, 'r')
    lines = f.readlines()
    objects = []

    for line in lines:
      line=line.rstrip()
      obj = [int(float(str(i))) for i in line.split(' ')]
      objects.append(obj)

    return objects

  def __create_new_folder(self, path, folder_name): 
    try: 
      current_path = os.getcwd() 
      os.chdir('.')
      path = os.getcwd()
      full_path = os.path.join(path, folder_name) 
      os.makedirs(full_path) 
      os.chdir(current_path)
      return full_path
    except OSError as error: 
      print(f"Already have a folder called: {folder_name} in this directory")
      full_path = os.path.join(path, folder_name)
      return full_path 

  # Sample Method
  def YOLOplateDetection(self, path, path_label, folder_name):
    self.path = path
    self.path_label = path_label
    self.folder_name = folder_name
    df_lista = []

    full_path = self.__create_new_folder(path, folder_name)

    for dir, subarch, archives in os.walk(path):
      for path_imagem in archives:
        try:
          img = cv2.imread(path + "/" + str(path_imagem))
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          lics = self.__read_txt(path_label + "/" + str(path_imagem[:-4]) + '.txt')

          for lic in lics:
            print(lic)
            c, x, y, w, h = lic
            print(f"c: {c}")
            print(f"x: {x}")
            print(f"y: {y}")
            print(f"w: {w}")
            print(f"h: {h}")
            print(x,y,w,h) # center of the bounding box
            img_alpr = img[y-int(h/2):y+int(h/2),x-int(w/2):x+int(w/2)]
            plt.imshow(img_alpr)
            #txt = pytesseract.image_to_string(img_alpr)
            #df_lista.append((path_imagem, txt))

        except IndexError as IE:
          print(f"\n\nOcorreu um erro de Index na imagem: {path_imagem}, porém continuando para a proxima imagem")
          continue
        except Exception as error:
          print(f"\n\nOcorreu um erro na imagem: {path_imagem}, porém continuando para a proxima imagem")
          continue

    df_aux = pd.DataFrame(df_lista)
    df_aux.rename(columns={0: "Image", 1: "Plate"}, inplace = True)
    df = df_aux.to_csv(full_path + "/" + "yolo_results.csv", index = False)

    return df