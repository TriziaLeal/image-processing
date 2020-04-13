'''
De Vera, Adrian
Leal, Merry Trizia
U-1L
Exer 06
'''
import cv2
import numpy as np 

image = cv2.imread("coins.jpg", 0)
colored = cv2.imread("coins.jpg", 1)
image = cv2.medianBlur(image,5)
ret, inv_image = cv2.threshold(image, 150, 250, cv2.THRESH_BINARY_INV)

dilation_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
erosion_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilated = cv2.dilate(inv_image, dilation_kernel)
eroded = cv2.erode(dilated, erosion_kernel)
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(eroded, 8)

tally = [0, 0, 0 ,0 ,0]
price = [0.05, 0.1, 0.25 ,1 ,5]
for i in range(1,ret):
	# use the colored version of the image and color the first component green
	# create bounding box from the given stats
	# left
	if (stats[i][4] >= 20000):
		tally [4] = tally[4] + 1
	elif stats[i][4] > 16000:
		tally [3] = tally[3] + 1
	elif stats[i][4] > 11000:
		tally [2] = tally[2] + 1
	elif stats[i][4] > 8000:
		tally [1] = tally[1] + 1
	else:
		tally [0] = tally [0] + 1
	colored[stats[i][1]:stats[i][1]+stats[i][3],stats[i][0]:stats[i][0]+2] = [0,0,255]
	# top 
	colored[stats[i][1],stats[i][0]:stats[i][0]+stats[i][2]] = [0,0,255]
	# right
	colored[stats[i][1]:stats[i][1]+stats[i][3],stats[i][0]+stats[i][2]] = [0,0,255]
	# bottom
	colored[stats[i][1]+stats[i][3],stats[i][0]:stats[i][0]+stats[i][2]] = [0,0,255]


total = 0
print("Found " + str(sum(tally)) + " coins")
for i in range(len(tally)):
	total = total + (tally[i] * price[i])
	print("Found " + str(tally[i]) + " PHP " + str(price[i]) + ' : ' + str(tally[i]*price[i]))
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(colored, 'PHP: ' + str(total), (1000, 50), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

colored[np.uint8(centroids[1][0]),np.uint8(centroids[1][1])] = [255,255,255]

cv2.imwrite("1st contour bounding box.jpg", colored)

cv2.waitKey(0)
cv2.destroyAllWindows()