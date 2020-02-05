# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:37:17 2020

@author: SHOBHIT SAINI
"""
import cv2
import numpy as np
cap = cv2.VideoCapture('D:\IIT_BBS_CLG_WORK\IITBBS_LAB_WORK\DF2_lab\Assignment_4\Train002.avi')


# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    # Convert the image to grayscale
    src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Laplace function
    dst = cv2.Laplacian(src_gray, cv2.CV_64F)
    
    # converting back to uint8
    abs_dst = cv2.convertScaleAbs(dst)
    # Display the resulting frame
    cv2.imshow('Frame',abs_dst)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()
