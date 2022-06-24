import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import uuid
import os
import time
import pytesseract
from PIL import Image
import pyautogui
import processimg as pi
import tess_verifiers as tessvf
#No availability on macbook m1
#import pyautogui
#This is the editable configuration used
bluesb_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist="0123456789/"'
redsb_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist="0123456789/"'
time_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=":0123456789"'



# There exists a function variation that can be used to create and save images into a dataset

#Definitions:
    #ROI = Region of Interest

# This function variation is:
    # 1. Scanning the image as an array
    # 2. Manipulating the array into specific ROI
        # Current ROI includes:
            # Time - developed and confirmed
            # Blue scoreboard - developed and confirmed
            # Red scoreboard - developed and confirmed
            # Blue Towers taken - not developed
            # Red Towers taken - not developed

        #Possible ROI includes:
            # Wards - does each category return a specific and consistent output?
                # Yellow Ward
                # Red sweeper Ward
                # Pink Ward

    # 3. Running pytesseract on it to grab the text on the ROI
    # 4. Turning ROI_text into integers for the use of data analysis
    # 5. Saving the integers in a formatted data structure of choice:
        #Currently testing Pandas to determine most appropriate data structure
#Use this as a debugging too whenever you need to check on an image
#if cv2.waitKey(1) & 0xFF==ord('0'):
    #break

#Begin changing pyautogui

# Scoreboard, Blue scoreboard, and Red scoreboard regions   
# scoreboard_region = screen_array[840:1200, 720:1200]
# bluesb_region = gray_array[850:1070,720:915]
# redsb_region = gray_array[850:1070, 1005:1195]
# time_region = gray_array[75:105, 930:990]
# Show the image of the scoreboard you would like to print out
# Great for debugging purposes!

# cv2.imshow('fullscreen', corrected_fullscreen)
# cv2.imshow('scoreboard', corrected_sb)
# cv2.imshow('bluesb',corrected_bluesb)
# cv2.imshow('redsb',corrected_redsb)
# cv2.imshow('time',corrected_time)

    
oldTime = 0 
while True: 
    
    #timer start
    #st = time.time()


    # This is currently in pyautogui, but ultimately you need any SS tool
    # This SS needs to be in np array form
    # This np array would then be a chopped up array 
    scoreboard = pyautogui.screenshot()
    screen_array = np.array(scoreboard)
    gray_array = cv2.cvtColor(screen_array, cv2.COLOR_RGB2GRAY)


    # ------------------ Time to Text ----------------- #
    time_region = gray_array[75:105, 930:990]
    #Preprocess img for pytesseract
    time_img = pi.pre_img(time_region,600, (150,255))
    #Returns a string to be verified later
    timetest = pytesseract.image_to_string(time_img,config=time_config)
    #print(f"In game time:\n{timetest}")


    #---- ALWAYS COPY AND PASTE THESE TO MOVE AND DELETE WHEN DEBUGGING PICTURES ---- #    
    #Verify that a time exists by turning it from a string into an integer, ensuring that there exist [minutes, seconds] and no fuzzy figures within it.
    if tessvf.time(timetest) == False:
        #print("not a real time")
        continue
    else:
        #Timer is an INTEGER variable that can be used later for the dataset - more valuable than a string. 
        #The string, timetest, can be used for file names though!
        newTime = tessvf.time(timetest)
        #print(timer)
    
    #Optimize so the function only grabs a unique instance per second
    if  newTime <= oldTime:
        #print(f"outta there{newTime} is less than {oldTime}")
        continue
    
    else:
        bluesb_region = gray_array[850:1070,720:915]
            
        #---- ALWAYS COPY AND PASTE THESE TO MOVE AND DELETE WHEN DEBUGGING PICTURES ---- #

        #print(f"In game time after verifying it only occurs once per second:\n{newTime}")
        oldTime = newTime
        time_text = tessvf.int_time_to_text(oldTime)
        print(f"time: {time_text}")
        #continue
        #Blue SB
        bluesb_img = pi.pre_img(bluesb_region,300, threshold=(120,255),blur=(3,3))
        cv2.imshow('bluesb_region', bluesb_img)
        if cv2.waitKey(1) & 0xFF==ord('0'):
            break   

        bluepytest = pytesseract.image_to_string(bluesb_img,config=bluesb_config)
        #print(f"Blue side:\n{bluepytest}")


        #Verify Blue scoreboard
        verified_bluesb = tessvf.bluesb(bluepytest)

        if verified_bluesb == False:
            print("NOT A VALID SCOREBOARD BUT KEEP GOING!")
            continue
        else:
            #print("success, continuing")
            print(verified_bluesb)


        #Red SB
        redsb_region = gray_array[850:1070, 1005:1195]
        redsb_img = pi.pre_img(redsb_region, 250, threshold=(90,255),blur=(1,1))

        redpytest = pytesseract.image_to_string(redsb_img,config=redsb_config)
        #print(f"Red side:\n{redpytest}")

        #Verify red scoreboard
        verified_redsb = tessvf.redsb(redpytest)    

        if verified_redsb == False:
            print("NOT A VALID SCOREBOARD BUT KEEP GOING!")
            continue
        else:
            #print("success, continuing")
            print(verified_redsb)
    
        
    
    

    # get the end time
    #et = time.time()
    #time.sleep(interval - (et-st))
    #mimicsleep = interval- (et-st)
    
    #print(f"time slept is {mimicsleep}")
    
    
    #totaltime += mimicsleep + (et-st)
    #print(f"total time elapsed is {totaltime} seconds")
    
    
    #elapsed_time = et - st
    #print('Execution time:', elapsed_time, 'seconds')
    
cv2.destroyAllWindows()