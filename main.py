import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import uuid
import os
import time
import pytesseract
from PIL import Image
import glob
import timetextverify
import sbverify
import bluetessverify
import redtessverify
#No availability on macbook m1
#import pyautogui
#This is the editable configuration used
bluesb_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist="0123456789/"'
redsb_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist="0123456789/"'
time_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=":0123456789/"'



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
    

    
oldTime = 0
while True: 
    
    #timer start
    st = time.time()


    # This is currently in pyautogui, but ultimately you need any SS tool
    # This SS needs to be in np array form
    # This np array would then be a chopped up array 
    scoreboard = pyautogui.screenshot()
    screen_array = np.array(scoreboard)

    #Scoreboard, Blue scoreboard, and Red scoreboard regions   
    #scoreboard_region = screen_array[840:1200, 720:1200, :]
    bluesb_region = screen_array[850:1070,720:915,:]
    redsb_region = screen_array[850:1070, 1005:1195,:]
    time_region = screen_array[78:105, 935:990,:]



    #Corrected color region for the scoreboards
    
    #corrected_fullscreen = cv2.cvtColor(screen_array, cv2.COLOR_RGB2BGR)
    #corrected_sb = cv2.cvtColor(scoreboard_region, cv2.COLOR_RGB2GRAY)
    corrected_bluesb = cv2.cvtColor(bluesb_region, cv2.COLOR_RGB2GRAY)
    corrected_redsb = cv2.cvtColor(redsb_region, cv2.COLOR_RGB2GRAY)
    corrected_time = cv2.cvtColor(time_region, cv2.COLOR_RGB2GRAY)

    
    #Show the image of the scoreboard you would like to print out
    #Great for debugging purposes!

    #cv2.imshow('fullscreen', corrected_fullscreen)
    #cv2.imshow('scoreboard', corrected_sb)
    #cv2.imshow('bluesb',corrected_bluesb)
    #cv2.imshow('redsb',corrected_redsb)
    #cv2.imshow('time',corrected_time)

    
    if cv2.waitKey(1) & 0xFF==ord('0'):
        break

    
    #Time
    scale_percent = 400
    width = int(corrected_time.shape[1] * scale_percent/100)
    height = int(corrected_time.shape[0] * scale_percent/100)
    dim = (width,height)
    timeimg = cv2.resize(corrected_time, dim, interpolation=cv2.INTER_CUBIC)
    ret, timeimg = cv2.threshold(timeimg,150,255,cv2.THRESH_BINARY_INV)
    timeimg = cv2.blur(timeimg,(1,1))
    #Returns a string to be verified later
    timetest = pytesseract.image_to_string(timeimg,config=time_config)
    #print(f"In game time:\n{timetest}")
    
    #Verify that a time exists by turning it from a string into an integer, ensuring that there exist [minutes, seconds] and no fuzzy figures within it.
    if timetextverify(timetest) == False:
        #print("not a real time")
        continue
    else:
        #Timer is an INTEGER variable that can be used later for the dataset - more valuable than a string. 
        #The string, timetest, can be used for file names though!
        newTime = timetextverify(timetest)
        #print(timer)
    
    #Optimize so the function only grabs a unique instance per second
    if  newTime <= oldTime:
        #print(f"outta there{newTime} is less than {oldTime}")
        continue
    
    else:
        #print(f"In game time after verifying it only occurs once per second:\n{newTime}")
        oldTime = newTime
        #continue
        #Blue SB
        scale_percent = 250
        width = int(corrected_bluesb.shape[1] * scale_percent/100)
        height = int(corrected_bluesb.shape[0] * scale_percent/100)
        dim = (width,height)
        bluesb = cv2.resize(corrected_bluesb, dim, interpolation=cv2.INTER_CUBIC)
        ret, bluesb = cv2.threshold(bluesb,120,255,cv2.THRESH_BINARY_INV)
        bluesb = cv2.blur(bluesb,(3,3))
        bluepytest = pytesseract.image_to_string(bluesb,config=bluesb_config)
        #print(f"Blue side:\n{bluepytest}")


        #Verify Blue scoreboard
        verified_bluesb = bluetessverify(bluepytest)

        if verified_bluesb == False:
            print("NOT A VALID SCOREBOARD BUT KEEP GOING!")
            continue
        else:
            #print("success, continuing")
            print(verified_bluesb)

        #Red SB
        scale_percent = 250
        width = int(corrected_redsb.shape[1] * scale_percent/100)
        height = int(corrected_redsb.shape[0] * scale_percent/100)
        dim = (width,height)
        redsb = cv2.resize(corrected_redsb, dim, interpolation=cv2.INTER_LINEAR)
        ret, redsb = cv2.threshold(redsb,90,255,cv2.THRESH_BINARY_INV)
        redsb = cv2.blur(redsb,(1,1))
        redpytest = pytesseract.image_to_string(redsb,config=redsb_config)
        #print(f"Red side:\n{redpytest}")

        #Verify red scoreboard
        verified_redsb = redtessverify(redpytest)    

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