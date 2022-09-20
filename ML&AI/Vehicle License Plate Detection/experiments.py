import numpy as np
import cv2
import easyocr

img = cv2.imread("C:/Users/nhoei/licenseplate.jpg")
reader = easyocr.Reader(['en'])
ocr_results = reader.readtext("C:/Users/nhoei/licenseplate.jpg")
print(ocr_results)

confidence_treshold = 0.2

for detection in ocr_results:
    if detection[2] > confidence_treshold:
        top_left = [int(value) for value in detection[0][0]]
        bottom_right = [int(value) for value in detection[0][2]]
        text = detection[1]
        img = cv2.rectangle(img, top_left, bottom_right, (0,0,255), 5)
        img = cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2, cv2.LINE_AA)

cv2.imshow("img", img)
cv2.waitKey(0)

"""
img = cv2.imread(r"C:\Users\caio_barros\Documents\git\projetos\ML&AI\Vehicle License Plate Detection\samples\Cars111.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
plt.show()

bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
edged = cv2.Canny(bfilter, 30, 200) #Edge detection
plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
plt.show()

keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None
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

plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
plt.show() # aqui aparece a placa recortada
"""