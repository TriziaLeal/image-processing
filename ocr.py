'''
De Vera, Adrian
Leal, Merry Trizia
'''

import numpy as np
import cv2
import pytesseract

# main
FILENAME = "p3.png"
#FILENAME = "p1.jpg"
#FILENAME = "p2.jpg"

image = cv2.imread(FILENAME)
#preprocessing
#Applied median filter to image to reduce noise
image = cv2.medianBlur(image,3)
#canny Edge Detection
threshold = 50
edge = cv2.Canny(image, threshold, 2*threshold, 3)

#produce contours of image
_, contours, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#sorts the contour areas
contours = sorted(contours,key = cv2.contourArea,reverse = True)

#finds the largest contour area with a rectangular shape
x = []
y = []
for contour in contours:
    arcLen = cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,0.013*arcLen,True)

    if len(approx) == 4:     
        #cv2.drawContours(image,[contour],-1,(0,255,0),2)
        for i in range(len(contour)):
            x = np.append (x, contour[i][0][0])
            y = np.append (y, contour[i][0][1])

        topx = int(np.min(x))
        topy = int(np.min(y))
        botx = int(np.max(x))
        boty = int(np.max(y))
        cropped = image [topy:boty, topx:botx]

        ret,binarized = cv2.threshold(cropped, 105, 230, cv2.THRESH_BINARY_INV)
        cv2.imshow('gray', cropped)
        print(pytesseract.image_to_string(cropped, config="--psm 1"))  
        break




#cv2.imshow("Original", image)
#cv2.imshow("binarized", binarized)

cv2.waitKey(0)
cv2.destroyAllWindows()