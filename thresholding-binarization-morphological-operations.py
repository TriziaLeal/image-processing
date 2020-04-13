## Created by: Trixia Leal and Adrian Carlos A. de Vera
## Purpose: CMSC 165 exer 05
## Description: Detect and count the shaded circles in the images by processing it using thresholding, and morphological functions

import cv2
import glob
import os
import numpy as np

tally = [0,0,0,0,0,0,0]
tallynames = ['SA', 'A', 'SLA', 'NAD', 'SLD', 'D', 'SD']
def sliceCircle(coordinates, image, original):
  for i in range(len(coordinates)//2):
    x = int(coordinates[2*i])
    y = int(coordinates[2*i+1])
    slicedCircle = image[y-12:y+12, x-12:x+12]
    
    #canny Edge Detection
    threshold = 50
    edge = cv2.Canny(slicedCircle, threshold, 2*threshold, 3)
    # cv2.circle (image, (x,y), 1, (255,0,0), 1)
    #cv2.imwrite('edge.jpg', edge)
    #produce contours of image
    result, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    if (len(contours)<=2):
      tally[i] = tally[i] + 1
      #original[y-12:y+12, x-12:x+12] = slicedCircle
      original = cv2.rectangle(original, (x-10,y-10),(x+10,y+10),(0,255,0),2)
      #cv2.imwrite('test.jpg', original)
  
  return image
  

# for i in range (len(images)):
#   cv2.imwrite(format(i + 1, '04') + '.jpg', images[i])

images = [cv2.imread(file, 0) for file in glob.glob("./images/*.jpg")]
font = cv2.FONT_HERSHEY_SIMPLEX

for i in range (len(images)):
  #read coordinate file
  text = open("coordinates.txt","r")
  rows, cols = images[i].shape
  #apply inverse thresholding
  ret, inv_image = cv2.threshold(images[i], 150, 250, cv2.THRESH_BINARY_INV)
  #closing
  dilation_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
  erosion_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
  dilated = cv2.dilate(inv_image, dilation_kernel)
  eroded = cv2.erode(dilated, erosion_kernel)
  #image[x][y]
  for line in text:
    line = line[0:-1]
    coordinates = str.split(line)
    detect = sliceCircle(coordinates, eroded, images[i])

  # count tally
  for j in range(len(tally)):
    cv2.putText(images[i], tallynames[j] + ' : ' + str(tally[j]), (1100, 200 + 30*j), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
  
    
  cv2.imwrite(format(i + 1, '04') + '.jpg', images[i])
  text.close()
  tally = [0,0,0,0,0,0,0] 

#print(tally)
#cv2.namedWindow("original",cv2.WINDOW_NORMAL)
#cv2.imwrite("test.jpg", hello)
# cv2.waitKey(0)
# cv2.destroyAllWindows()