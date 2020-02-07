# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:37:17 2020

@author: SHOBHIT SAINI
"""

import cv2
import numpy as np
from sklearn import preprocessing
from skimage import feature, io
from scipy.spatial import distance
video1 = cv2.VideoCapture("D:\IIT_BBS_CLG_WORK\IITBBS_LAB_WORK\DF2_lab\Assignment_4\Train002.avi")
video2 = cv2.VideoCapture("D:\IIT_BBS_CLG_WORK\IITBBS_LAB_WORK\DF2_lab\Assignment_4\Train003\.avi")
#Driver function       
def opticalflow(cap): 
    #Reading first frame and applying laplacian filter
    ret, frame1 = cap.read()
    frame_arr = np.zeros_like(frame1)
    frame1=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY) 
    pre=np.uint8(cv2.normalize(cv2.Laplacian(frame1,cv2.CV_64F),None,0,255,cv2.NORM_MINMAX))
    count = 0    
    frame_arr[...,1] = 255
    fm=[]
    while(1):
        ret, frame2=cap.read()
        if ret == False:
                break  
        frame2=cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY) 
        nxt=np.uint8(cv2.normalize(cv2.Laplacian(frame2,cv2.CV_64F),None,0,255,cv2.NORM_MINMAX))
        flow =cv2.calcOpticalFlowFarneback(pre,nxt, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        #cartToPolar used to compute the magnitude and angle of 2D vectors
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        ang=ang*180/np.pi/2
        mx=(np.floor(np.max(ang))/3)+1
        frame_arr[...,0] = ang
        #normalize the magnitute 
        frame_arr[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        # 3*3 array initialize to zeros
        ar = np.zeros((3,3),dtype=int)
        for i in range(frame_arr.shape[0]):
            for j in range(frame_arr.shape[1]):
                frame_arr[i,j,0]=frame_arr[i,j,0]/mx
                frame_arr[i,j,2]=frame_arr[i,j,2]/86
                ar[frame_arr[i,j,0],frame_arr[i,j,2]] += 1
        ar=ar.reshape([1,9])
        fm.append(ar)
        pre = nxt
        count+=1
        if count==20:
            break
    fm=np.asarray(fm) 
    fm=fm.reshape([len(fm),9]).T
    return fm
def mahalanobisdistance(fm1,fm2):
    mean1=np.mean(fm1,axis=1)  
    mean2=np.mean(fm2,axis=1)  
    print(mean1,mean2)   
    cov1= np.cov(fm1,y=None,rowvar=True,bias=False,ddof=None,fweights=None,aweights=None)
    covinv=np.linalg.inv(cov1)
    d=distance.mahalanobis(mean2,mean1,covinv)  
    print("distance is:=",d)    

fm1=opticalflow(video1)
fm2=opticalflow(video2)

mahalanobisdistance(fm1,fm2)
video1.release()
video2.release()
cv2.destroyAllWindows()
