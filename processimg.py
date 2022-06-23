import numpy as np
import cv2
import pyautogui


#Preprocesses img array
def pre_img(img_array, scale, threshold=(150,255), blur=(1,1)):
    
    width = int(img_array.shape[1] * scale/100)
    height = int(img_array.shape[0] * scale/100)
    dim = (width,height)
    timeimg = cv2.resize(img_array, dim, interpolation=cv2.INTER_CUBIC)
    ret, timeimg = cv2.threshold(timeimg,threshold[0],threshold[1],cv2.THRESH_BINARY_INV)
    timeimg = cv2.blur(timeimg,blur)
    return img_array