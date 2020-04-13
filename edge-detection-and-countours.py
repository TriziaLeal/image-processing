import numpy as np
import cv2

# main
FILENAME = "p3.png"
#FILENAME = "p1.jpg"
#FILENAME = "p2.jpg"

image = cv2.imread(FILENAME)

#preprocessing
#Applied median filter to image to reduce noise
image = cv2.medianBlur(image,5)

#canny Edge Detection
threshold = 50
edge = cv2.Canny(image, threshold, 2*threshold, 3)

#produce contours of image
result, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#sorts the contour areas
contours = sorted(contours,key = cv2.contourArea,reverse = True)

#finds the largest contour area with a rectangular shape
for contour in contours:
    arcLen = cv2.arcLength(contour,True)
    print(arcLen)
    approx = cv2.approxPolyDP(contour,0.013*arcLen,True)

    if len(approx) == 4:     
        cv2.drawContours(image,[contour],-1,(0,255,0),2)
        break

cv2.imshow("Original", image)
cv2.imshow("Edge", edge)

cv2.waitKey(0)
cv2.destroyAllWindows()