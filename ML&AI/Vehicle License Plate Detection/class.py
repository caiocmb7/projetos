# imports

import numpy as np
import cv2
import easyocr
import cv2
from matplotlib import pyplot as plt
import imutils
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# A Sample class with init method
class Car:

  # init method or constructor
  def __init__(self):
      pass

  def __filters(self, img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    return gray, bfilter, edged
  
  def __search_plate_and_crop(self, img, edged, gray):
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    location = 0
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    return new_image, approx, cropped_image

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

  def __plot_images(self, img1, img2, title1="", title2=""):
    fig = plt.figure(figsize=[15,15])
    ax1 = fig.add_subplot(121)
    ax1.imshow(img1, cmap="gray")
    ax1.set(xticks=[], yticks=[], title=title1)

    ax2 = fig.add_subplot(122)
    ax2.imshow(img2, cmap="gray")
    ax2.set(xticks=[], yticks=[], title=title2)
    
    return fig

  # Sample Method
  def plateDetection(self, path, folder_name, show_steps = False):
    self.path = path
    self.folder_name = folder_name
    df_lista = []

    full_path = self.__create_new_folder(path, folder_name)

    for dir, subarch, archives in os.walk(path):
      for path_imagem in archives:
        try:
          img = cv2.imread(path + "/" + str(path_imagem))
          gray, bfilter, edged  = self.__filters(img)
          new_image, approx, cropped_image = self.__search_plate_and_crop(img, edged, gray)

          reader = easyocr.Reader(['en'])
          result = reader.readtext(cropped_image)

          text = result[0][-2]
          df_lista.append((path_imagem, text))
          font = cv2.FONT_HERSHEY_SIMPLEX
          res = cv2.putText(img, text=text, org=(approx[1][0][0], approx[2][0][1]+30), fontFace=font, fontScale=0.7, color=(0,255,0), thickness=3, lineType=cv2.LINE_AA)
          res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
          plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
          plt.savefig(full_path + "/" + path_imagem)
        except IndexError as IE:
          print(f"\n\nOcorreu um erro de Index na imagem: {path_imagem}, porém continuando para a proxima imagem")
          continue
        except Exception as error:
          print(f"\n\nOcorreu um erro na imagem: {path_imagem}, porém continuando para a proxima imagem")
          continue

    df_aux = pd.DataFrame(df_lista)
    df_aux.rename(columns={0: "Image", 1: "Plate"}, inplace = True)
    df = df_aux.to_csv(full_path + "/" + "results.csv", index = False)

    if show_steps == True:
      self.__plot_images(img, gray, title1="original", title2="gray")
      self.__plot_images(gray, bfilter, title1="gray", title2="bfilter")
      self.__plot_images(bfilter, edged, title1="bfilter", title2="edged")
      self.__plot_images(img, cropped_image, title1="original", title2="cropped_image")

    return df

# To run the class above, do:

# Car().plateDetection(path = "/content/samples", folder_name = "detection", show_steps = True) -- example