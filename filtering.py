
'''
AUTHOR: 
    Adrian de Vera
    Trizia Leal
DESC: 
    CMSC 165 Exercise 3 Source Code: Filtering
'''
import cv2
import numpy as np


def medianFilter(image, kernel_size):
    
    getSlice = []
    rows, cols = image.shape
    
    #initialize result matrix
    result = np.zeros((rows,cols), np.uint8)
    
    #to get neighbor pixel
    kernel_mid = int(kernel_size/2)
    
    #for each pixels,get its neighbor pixel
    for i in range(rows):
        for j in range(cols):
            #ignores border pixels
            if ((0 <= i < kernel_mid) or (rows-kernel_mid <= i < rows)) or ((0 <= j < kernel_mid) or (cols-kernel_mid <= j < cols)):
                result[i,j] = image[i,j]                
            #get neighbor pixels; sort pixels in the kernel; assign the median to the anchor pixel
            else:
                getSlice = image[i-kernel_mid:i+kernel_mid+1, j-kernel_mid:j+kernel_mid+1]
                sortSlice = sorted(getSlice.ravel())
                mid = sortSlice[int(len(sortSlice)/2)]
                result[i,j] = np.uint8(mid)
    return result

def meanFilter (image, kernel):
    kernel = kernel/kernel.sum()

    rows, cols = image.shape
    getSlice = np.zeros((rows,cols), np.float32)
    result = np.zeros((rows,cols), np.float32)
    kernel_mid = int(len(kernel)/2)

    #for each pixels, get its neighbor pixel
    for i in range(rows):
        for j in range(cols):

            #ignore border pixels
            if ((0 <= i < kernel_mid) or (rows-kernel_mid <= i < rows)) or ((0 <= j < kernel_mid) or (cols-kernel_mid <= j < cols)):
                result[i,j] = image[i,j]

            #get summation of each pixel of the slice * corresponding pixel in the kernel
            #assign it to the anchor pixel
            else:
                getSlice = image[i-kernel_mid:i+kernel_mid+1, j-kernel_mid:j+kernel_mid+1]
                multiply2D = getSlice*kernel
                mid = multiply2D.sum()
                result[i,j] = np.uint8(mid)

    return result

def gaussianFilter(image):
    #define kernel here
    kernel = np.ones((kernel_size, kernel_size), dtype='float32')

    result = meanFilter(image, kernel)
    return result

image = cv2.imread("lena.jpg", 0)	
kernel_size = 11
test = [[1,1,1],
        [1,1,1],
        [1,1,1]]
test = np.array(test, dtype=np.uint8)
#mean filter kernel
kernel = np.ones((kernel_size, kernel_size), dtype='float32')

median = medianFilter(image, kernel_size)
mean = meanFilter(image, kernel)
gaussian = gaussianFilter(image)

cv2.imwrite("./mean.jpg", mean)
cv2.imwrite("./median.jpg",median)
cv2.imwrite("./gaussian.jpg",gaussian)
