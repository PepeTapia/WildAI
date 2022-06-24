import numpy as np
import cv2
import pyautogui


#Preprocesses img array
def pre_img(img_array, scale, threshold=(150,255), blur=(1,1)):
    new_img = img_array
    width = int(new_img.shape[1] * scale/100)
    height = int(new_img.shape[0] * scale/100)
    dim = (width,height)
    tess_img = cv2.resize(new_img, dim, interpolation=cv2.INTER_CUBIC)
    ret, tess_img = cv2.threshold(tess_img,threshold[0],threshold[1],cv2.THRESH_BINARY_INV)
    tess_img = cv2.blur(tess_img,blur)
    return tess_img