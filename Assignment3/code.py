# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 14:03:13 2020

@author: SHOBHIT SAINI
"""

import cv2
import numpy as np
#Image reading
img = cv2.imread('D:\\IIT_BBS_CLG_WORK\\IITBBS_LAB_WORK\\DF2_lab\\fruits.jpg')
#Histogram canvas creation
img1 = np.ones((550, 368, 3), np.uint8)*255
#Creating array of size 256 and array is initialize to zeros
arr = np.zeros((256))
#increamenting count array based on the pixel value
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        arr[img[i][j][1]] += 1

#Finding maximum and normalize the array value from 0 to 549        
maximum = np.amax(arr)
arr = (arr/maximum)*549
arr =arr.astype(int)

#Drawing of histogram
for i in range(256):
    img1 = cv2.line(img1, (i,550), (i,550 - arr[i]),(140, 98, 22), 1)

#original image
cv2.imshow("img", img)
#Histogram image
cv2.imshow("img1", img1)

#Making of random list of size 10 and having the value from 0 to 255
list_int = []
for i in range(10):
    list_int.append(np.random.randint(0,256))

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if list_int.count(img[i][j][1]) > 0:
            if np.random.rand() > 0.5:
                if j + 1 <img.shape[1] and j-1 > 0 and i+1 < img.shape[0] and i-1 > 0:
                    img[i][j][1] = (int(img[i+1][j][1]) + int(img[i][j+1][1]) + int(img[i-1][j][1]) + int(img[i][j-1][1]))/4
                
arr1 = np.zeros((256)) 
img2 = np.ones((550, 368, 3), np.uint8)*255        
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        arr1[img[i][j][1]] += 1
        
maximum = np.amax(arr1.astype(int))
print(maximum)
arr1 = (arr1/maximum)*549
arr1 =arr1.astype(int)
for i in range(256):
    img2 = cv2.line(img2, (i,550), (i,550- arr1[i]),(140, 98, 22), 1)


cv2.imshow("new_histo", img2)
cv2.imshow("img2", img)
upper_limit = 10
for i in range(256):
    if arr[i] - arr1[i] > upper_limit:
        print(i);

cv2.waitKey(0)
cv2.destroyAllWindows()
