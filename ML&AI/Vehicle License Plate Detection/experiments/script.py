# imports

import numpy as np
import cv2
import easyocr
import cv2
from matplotlib import pyplot as plt
import imutils
import pandas as pd
import os

def plate_detection(pasta):
  df_lista = []

  for dir, subarch, archives in os.walk(pasta):
    for path_imagem in archives:
      img = cv2.imread(pasta + "/" + str(path_imagem))
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

      bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
      edged = cv2.Canny(bfilter, 30, 200) #Edge detection

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

      reader = easyocr.Reader(['en'])
      result = reader.readtext(cropped_image)

      text = result[0][-2]
      df_lista.append((path_imagem, text))
      font = cv2.FONT_HERSHEY_SIMPLEX
      res = cv2.putText(img, text=text, org=(approx[1][0][0], approx[2][0][1]+30), fontFace=font, fontScale=0.6, color=(0,255,0), thickness=3, lineType=cv2.LINE_AA)
      res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
      plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
      plt.savefig(f"/content/detection/{path_imagem}")
      
  df_aux = pd.DataFrame(df_lista)
  df_aux.rename(columns={0: "Image", 1: "Plate"}, inplace = True)
  df = df_aux.to_csv("/content/detection/results.csv", index = False)
  return df


