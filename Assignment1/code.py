# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 20:47:33 2020

@author: SHOBHIT SAINI
"""
import math
import cv2
import numpy as np
import pandas as pd
"""""""""""""""""""Reading of image"""""""""""""""""""
img = cv2.imread("D:\IIT_BBS_CLG_WORK\IITBBS_LAB_WORK\DF2_lab\Assignment1\white.jpg")
"""""""""""""""""""converting of image into gray image"""""""""""""
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
original_gray = gray
print("Image_matrix:")
print(gray)

"""""""""""""""""""""Input"""""""""""""""""""""
val = input("Enter your watermark text: ") 
"""""""""""""""Converting string into binary"""""""""""""""""""""
converted_binary = ''.join(format(ord(i), 'b') for i in val)
print("Watermark Text in binary:")
print(converted_binary)
length = len(converted_binary)
num_rows, num_cols = img.shape[:2]
a = math.ceil(length/num_cols)
i = 40
j= 0
"""""""""""""Embedding of the watermark"""""""""""""
for x in range(length):
    if(j < num_cols):
        if(gray[i][x%num_cols] % 2 == 0 and converted_binary[x] == '1'):
            gray[i][x%num_cols] += 1      
        elif(gray[i][x%num_cols] % 2 != 0 and converted_binary[x] == '0'):
            gray[i][x%num_cols] -= 1
        j = j+1
    else:
        i += 1
        j = 0
result = ''
watermark_gray = gray
j= 0
"""""""""""""""""""Retrieving of watermark message""""""""""""" 
for x in range(length):
    if(j < num_cols):
        result = result + str(gray[i][x%num_cols] % 2)
        j = j+1
    else:
        i += 1
        j = 0
        
def conversion_binary_into_ascii(aug1):
    temp = ''
    result = ''
    for i in range(aug1.__len__()):
        temp = temp + aug1[i]
        if((i + 1) % 7 == 0):
            result = result + chr(int(temp, 2))
            temp = ''
    return result

result_ascii = conversion_binary_into_ascii(result)
print("After retrieving watermark message:")
print(result_ascii)
"""""""""""""""""""Function to add noise into the image"""""""""""""
def noisy_adder_gaussian():
      row,col= gray.shape[:2]
      mean = 0
      var = 0.1
      sigma = var**0.5
      gauss = np.random.normal(mean,sigma,(row,col))
      gauss = gauss.reshape(row,col)
      noisy = gray + gauss
      return noisy
noisy_image = noisy_adder_gaussian()
noisy_image = noisy_image.round()
print(noisy_image)
result = ''
j = 0
"""""""""Retrieving of watermark message from noisy image"""""""""
for x in range(length):
    if(j < num_cols):
        result = result + str(np.int(noisy_image[i][x%num_cols]) % 2)
        j = j+1
    else:
        i += 1
        j = 0
print("Retrieving of watermark message from noisy image")       
print(result)
"""""""""""""function to calculate psnr value"""""""""
def Peak_Signal_to_Noise_Ratio(aug1, aug2):
    mse = np.mean( (aug1 - aug2) ** 2 )
    if mse == 0:
        return 100
    Pixel_maximum = 255.0
    return 20 * math.log10(Pixel_maximum / math.sqrt(mse))

b=Peak_Signal_to_Noise_Ratio(gray,noisy_image)
print("psnr value:")
print(b)
cv2.imshow('Original_image', gray)
cv2.imshow('Watermark_image', watermark_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
