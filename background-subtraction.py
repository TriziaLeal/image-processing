'''
Leal, Merry Trizia M
De Vera, Adrian
'''

import cv2
import numpy as np 
import os

__NUM_LEARN_FRAMES__ = 100
__FOREGROUND_DIFF_THRESH__ = 25

capture = cv2.VideoCapture(0) 
if not capture.isOpened():
	capture.open()
count = 0
dirname = './frames'
if not (os.path.isdir(dirname)):
	os.mkdir(dirname)

while True:
	ret, frame = capture.read()
	if ret:
		cv2.imwrite(os.path.join(dirname, "frame%s.jpg" %str(count).zfill(4)), frame)
		count = count + 1
	else:
		print("read failed")
		break
	if count == __NUM_LEARN_FRAMES__:
		break
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

inputFileFormat = "./frames/frame{}.jpg"

filenames = [inputFileFormat.format(str(x).zfill(4)) for x in range(__NUM_LEARN_FRAMES__)]
frames = [cv2.imread(filename, 1) for filename in filenames]
frames = np.array(frames) 
grayFrames = [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in frames ]
grayFrames = np.array(grayFrames) 

background = np.median(grayFrames, axis=0)

backgroundShow = background.clip(0,255).astype('uint8')
cv2.imshow("background", backgroundShow)

if not capture.isOpened():
	capture.open()
while True:
	ret, frame = capture.read()
	if ret:
		grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		diff = grayFrame - background
		diff = np.absolute(diff)
		mask = diff > __FOREGROUND_DIFF_THRESH__
		foreground = frame.copy()
		mask2 = np.invert(mask)
		foreground[mask2] = [255,255,255]

		output = np.concatenate((frame, foreground), axis=1).astype('uint8')
		cv2.imshow("Output", output)
		cv2.waitKey(10)
	else:
		print("read failed")
		break
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.waitKey(0)
cv2.destroyAllWindows()

capture.release()
cv2.destroyAllWindows()