# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:41:27 2020

@author: SHOBHIT SAINI
"""

import cv2
import numpy as np
import math

#Embed the image on original image
def embed(original_copy, watermark_img, key):
    row = 0
    column = 0
    for i in range(0, key.__len__(), 2):
        original_copy[ord(key[i]) % original_copy.shape[0]][ord(key[i + 1]) % original_copy.shape[1]] = watermark_img[row][column]
        row = row + 1
        if(row % watermark_img.shape[0] == 0):
            row = 0
            column = column + 1


def decode_watermark(original_copy, watermark_img, key):
    row = 0
    column = 0
    img = np.zeros((watermark_img.shape[0], watermark_img.shape[1], watermark_img.shape[2]), np.uint8)
    for i in range(0, key.__len__(), 2):
        img[row][column] = original_copy[ord(key[i]) % original_copy.shape[0]][ord(key[i + 1]) % original_copy.shape[1]]
        row = row + 1
        if(row % watermark_img.shape[0] == 0):
            row = 0
            column = column + 1
    final = cv2.medianBlur(img, 3)
    cv2.imshow("extract", final)
    

original = cv2.imread("D:\\IIT_BBS_CLG_WORK\\IITBBS_LAB_WORK\\DF2_lab\\Assignment_2\\bird.jpg")
Height = original.shape[0]
Width = original.shape[1]
parameter = max(Height, Width)

def KSA(key):
    keylength = len(key)

    S = list(range(parameter))

    j = 0
    for i in range(parameter):
        j = (j + S[i] + ord(key[i % keylength])) % parameter
        S[i], S[j] = S[j], S[i]  # swap

    return S

def PRGA(S, size):
    i = 0
    j = 0
    K = ''
    for incr in range(size):
        i = (i + 1) % parameter
        j = (j + S[i]) % parameter
        S[i], S[j] = S[j], S[i]  # swap

        K += chr(S[(S[i] + S[j]) % parameter])
        
    return K

def RC4(key, size):
    S = KSA(key)
    string = PRGA(S, size)
    return string
    
def addNoise(img):
    column, row, depth = img.shape
    mean = 0
    var = 0.01
    sigma = var ** 0.5
    guass = np.random.normal(mean, sigma, (row, column, depth))
    guass = guass.reshape(column, row, depth)
    noisy = img + guass
    return noisy

def compute_psnr(img1, img2):
    img1 = img1.astype(np.float64) / 255.
    img2 = img2.astype(np.float64) / 255.
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return "Same Image"
    return 10 * math.log10(1. / mse)

#image input
original_img = cv2.imread("D:\\IIT_BBS_CLG_WORK\\IITBBS_LAB_WORK\\DF2_lab\\Assignment_2\\bird.jpg")
original_copy = original_img
watermark_img = cv2.imread("D:\\IIT_BBS_CLG_WORK\\IITBBS_LAB_WORK\\DF2_lab\\Assignment_2\\flag.jpg")

cv2.imshow("original", original_img)
cv2.imshow("watermark", watermark_img)
#Intialize the key variable 
key = "shobhitsaini"
#initialize the size with the twice of image size
size = watermark_img.shape[0] * watermark_img.shape[1] * 2

keystream = RC4(key, size)
print(keystream.__len__())
embed(original_copy, watermark_img, keystream)
cv2.imshow("Watermarked_img", original_copy)

decode_watermark(original_copy, watermark_img, keystream)
original_copy = addNoise(original_copy)
psnr = compute_psnr(original_img, original_copy)
print(psnr)
cv2.waitKey(0)
cv2.destroyAllWindows()
