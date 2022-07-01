import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import os
import pytesseract
from PIL import Image
import pyautogui
import wildscripts as ws
import pandas as pd
#No availability on macbook m1
#import pyautogui
#This is the editable configuration used
bluesb_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist="0123456789/"'
redsb_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist="0123456789/"'
time_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=":0123456789"'
header_config = r'--oem 3 --psm 6 digits -c tessedit_char_whitelist="0123456789"'

STATS_HEADER = ["time", "team","top_kill", "top_death", "top_assist", "top_gold",
                "jungle_kill", "jungle_death", "jungle_assist", "jungle_gold",
                "mid_kill","mid_death", "mid_assist", "mid_gold",
                "bot_gold", "bot_death", "bot_assist", "bot_gold",
                "supp_gold", "supp_death", "supp_assist","supp_gold",
               "towers", "team_gold", "team_kills"]
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

#Preprocesses img array
def pre_img(img_array, scale, threshold=(120,255), blur=(1,1)):
    new_img = img_array
    width = int(new_img.shape[1] * scale/100)
    height = int(new_img.shape[0] * scale/100)
    dim = (width,height)
    tess_img = cv2.resize(new_img, dim, interpolation=cv2.INTER_LINEAR)
    ret, tess_img = cv2.threshold(tess_img,threshold[0],threshold[1],cv2.THRESH_BINARY_INV)
    tess_img = cv2.blur(tess_img,blur)
    return tess_img




#Dictionaries that will be updated throughout the while loop
#opt dict is to use as a cache(?) system for reference and backup
blue_dict_opt = {
            'time': None,
            'team': None,
            'towers': 0,
            'team_gold': 0,
            'team_kills': 0,
            'top_kill': None,
            'top_death': None,
            'top_assist': None,
            'top_gold': None,
            'jungle_kill': None, 
            'jungle_death': None,
            'jungle_assist': None,
            'jungle_gold': None,
            'mid_kill': None,
            'mid_death': None,
            'mid_assist': None,
            'mid_gold': None,
            'bot_kill': None,
            'bot_death': None,
            'bot_assist': None,
            'bot_gold': None,
            'supp_kill': None,
            'supp_death': None,
            'supp_assist': None,
            'supp_gold': None
            }
blue_dict_csv = {
            'time': None,
            'team': None,
            'towers': 0,
            'team_gold': 0,
            'team_kills': 0,
            'top_kill': None,
            'top_death': None,
            'top_assist': None,
            'top_gold': None,
            'jungle_kill': None, 
            'jungle_death': None,
            'jungle_assist': None,
            'jungle_gold': None,
            'mid_kill': None,
            'mid_death': None,
            'mid_assist': None,
            'mid_gold': None,
            'bot_kill': None,
            'bot_death': None,
            'bot_assist': None,
            'bot_gold': None,
            'supp_kill': None,
            'supp_death': None,
            'supp_assist': None,
            'supp_gold': None
            }

red_dict_opt = {
            'time': None,
            'team': None,
            'towers': 0,
            'team_gold': 0,
            'team_kills': 0,
            'top_kill': None,
            'top_death': None,
            'top_assist': None,
            'top_gold': None,
            'jungle_kill': None, 
            'jungle_death': None,
            'jungle_assist': None,
            'jungle_gold': None,
            'mid_kill': None,
            'mid_death': None,
            'mid_assist': None,
            'mid_gold': None,
            'bot_kill': None,
            'bot_death': None,
            'bot_assist': None,
            'bot_gold': None,
            'supp_kill': None,
            'supp_death': None,
            'supp_assist': None,
            'supp_gold': None
            }
red_dict_csv = {
            'time': None,
            'team': None,
            'towers': 0,
            'team_gold': 0,
            'team_kills': 0,
            'top_kill': None,
            'top_death': None,
            'top_assist': None,
            'top_gold': None,
            'jungle_kill': None, 
            'jungle_death': None,
            'jungle_assist': None,
            'jungle_gold': None,
            'mid_kill': None,
            'mid_death': None,
            'mid_assist': None,
            'mid_gold': None,
            'bot_kill': None,
            'bot_death': None,
            'bot_assist': None,
            'bot_gold': None,
            'supp_kill': None,
            'supp_death': None,
            'supp_assist': None,
            'supp_gold': None
            }




#Below are Variables that are "optimized" - consider them a base
#Change them during a run, save them as a cache and use them as a fail-safe
oldTime = 0 
#-----towers-----#
blue_towers_opt = 0
red_towers_opt = 0
#-----team_gold-----#
blue_gold_opt = 0
red_gold_opt = 0
#-----team_kills-----#
blue_kills_opt = 0
red_kills_opt = 0



#----------- Pandas and File setup -------------- #
game_num = 1
base = os.getcwd()
title = input("""Enter folder title. Format should be similar to 'Team A vs Team B Series (Play-in/Group/Knockout)  """)
os.makedirs(f'WildAI\Datasets\{title}',exist_ok=True)
output_csv = os.path.join(base, f'WildAI\Datasets\{title}\Game{game_num}.csv')


#-------------------- Begin Processing ------------------------- #
blue_dict_csv['team'] = "TF"
red_dict_csv['team'] = "T1"


while True: 
    
    #timer start
    #st = time.time()

    # This np array would then be a chopped up array 
    scoreboard = pyautogui.screenshot()
    screen_array = np.array(scoreboard)
    gray_array = cv2.cvtColor(screen_array, cv2.COLOR_RGB2GRAY)

    # ------------------ Time to Text ----------------- #
    time_region = gray_array[75:105, 930:990]
    #Preprocess img for pytesseract
    time_img = pre_img(time_region,600, (150,255))
    #Returns a string to be verified later
    timetest = pytesseract.image_to_string(time_img,config=time_config)
    #print(f"In game time:\n{timetest}")


    #Verify that a time exists by turning it from a string into an integer, ensuring that there exist [minutes, seconds] and no fuzzy figures within it.
    if ws.verify_time(timetest) == False:
        print("No time found. Likely in replay or not in a game")
        continue
    #else:
    #Timer is an INTEGER variable that can be used later for the dataset - more valuable than a string. 
    #The string, timetest, can be used for file names though!
    newTime = ws.verify_time(timetest)
    blue_dict_csv['time'] = newTime
    red_dict_csv['time'] = newTime

    #Time to text for output reasons but I don't think it's needed for csv reasons    
    time_text = ws.int_time_to_text(newTime)
    print(f"time: {time_text}")
    
    #------------------------------------------- Auxiliary Header Scoreboard ----------------------------------------------- #
    #Create one preprocessed image and then splice from there
    header_score = gray_array[25:60,735:1210]
    header_score_img = pre_img(header_score, 100, threshold=(110,255), blur=(1,1))
    cv2.imshow('header_score_img',header_score_img)
    if cv2.waitKey(1) & 0xFF==ord('0'):
        break
    #------------ towers --------------#
    #Towers Taken
    #--- blue towers --- #
    blue_towers = header_score_img[0:35,0:25] 
    blue_towers_num = pytesseract.image_to_string(blue_towers, config=header_config)
    blue_towers_verified = ws.header_int_verify(blue_towers_num)
    if blue_towers_verified == False:
        blue_dict_csv['towers'] = blue_dict_opt.get('towers')
    elif ((blue_towers_verified != False)) and ( blue_towers_verified > blue_dict_opt.get('towers')):    
        blue_dict_csv['towers'] = blue_towers_verified
        blue_dict_opt['towers'] = blue_towers_verified
    # else:
    #     blue_dict_csv['towers'] = blue_dict_opt.get('towers')
    #--- red towers --- #
    red_towers = header_score_img[0:35,450:476]
    red_towers_num = pytesseract.image_to_string(red_towers, config=header_config)
    red_towers_verified = ws.header_int_verify(red_towers_num)
    if red_towers_verified == False:
        red_dict_csv['towers'] = red_dict_opt.get('towers')
    elif ((red_towers_verified != False)) and ( red_towers_verified > red_dict_opt.get('towers')):    
        red_dict_csv['towers'] = red_towers_verified
        red_dict_opt['towers'] = red_towers_verified
    # else:
    #     red_dict_csv['towers'] = red_dict_opt.get('towers')


    #------------ team_gold --------------#
    #--- blue gold --- #
    blue_gold = header_score_img[0:35,75:145]
    blue_gold_num = pytesseract.image_to_string(blue_gold, config=header_config)
    blue_gold_int = ws.team_gold_verify(blue_gold_num)
    if blue_gold_int == False:
        blue_dict_csv['team_gold'] = blue_dict_opt.get('team_gold')
    elif ((blue_gold_int != False)) and (blue_gold_int > blue_dict_opt.get('team_gold')):
        blue_dict_csv['team_gold'] = blue_gold_int
        blue_dict_opt['team_gold'] = blue_gold_int
    # else:
    #     blue_dict_csv['team_gold'] = blue_dict_opt.get('team_gold')

    #--- red gold --- #
    red_gold = header_score_img[0:35, 335:410]
    red_gold_num = pytesseract.image_to_string(red_gold, config=header_config)
    red_gold_int = ws.team_gold_verify(red_gold_num)
    if red_gold_int == False:
        red_dict_csv['team_gold'] = red_dict_opt.get('team_gold')
    elif (red_gold_int != False):
        red_dict_csv['team_gold'] = red_gold_int
        red_dict_opt['team_gold'] = red_gold_int
    # else:
    #     red_dict_csv['team_gold'] = red_dict_opt.get('team_gold')



    #------------ team_kills --------------#
    #--- blue kills --- #
    blue_kills = header_score_img[0:35, 185:215] 
    blue_kills_num = pytesseract.image_to_string(blue_kills, config=header_config)
    blue_kills_verified = ws.header_int_verify(blue_kills_num)
    if blue_kills_verified == False:
        blue_dict_csv['team_kills'] = blue_dict_opt.get('team_kills')
    elif ((blue_kills_verified != False)) and (blue_kills_verified > blue_dict_opt.get('team_kills')):
        blue_dict_csv['team_kills'] = blue_kills_verified
        blue_dict_opt['team_kills'] = blue_kills_verified
    # else:
    #     blue_dict_csv['team_kills'] = blue_dict_opt.get('team_kills')

    #--- red kills --- #
    red_kills = header_score_img[0:35, 235:275] 
    red_kills_num = pytesseract.image_to_string(red_kills, config=header_config)
    red_kills_verified = ws.header_int_verify(red_kills_num)
    if red_kills_verified == False:
        red_dict_csv['team_kills'] = red_dict_opt.get('team_kills')
    elif ((red_kills_verified != False)) and (red_kills_verified > red_dict_opt.get('team_kills')):
        red_dict_csv['team_kills'] = red_kills_verified
        red_dict_opt['team_kills'] = red_kills_verified
    # else:
    #     red_dict_csv['team_kills'] = red_dict_opt.get('team_kills')

    # print(f"""
    # Blue Towers Taken: {blue_towers_num}
    # Blue Team Gold: {blue_gold_int}
    # Blue Team Kills: {blue_kills_num}
    # Red Towers Taken: {red_towers_num}
    # Red Team Gold: {red_gold_int}
    # Red Team Kills: {red_kills_num}
    # """)
    #print(blue_dict_csv)
    #print(red_dict)    
    #Time logic to continue to new loop
    
    if newTime == oldTime:
        continue
    oldTime = newTime

    #---------------Blue scoreboard begins --------------------#
    bluesb_region = gray_array[850:1070,720:915]
    bluesb_img = pre_img(bluesb_region,250, threshold=(120,255),blur=(1,1))
    bluepytest = pytesseract.image_to_string(bluesb_img,config=bluesb_config)

    #Verify Blue scoreboard
    verified_bluesb = ws.verify_bluesb(bluepytest)

    if verified_bluesb == False:
        print("Blue scoreboard not valid")
        continue
    #else:
    #print("success, continuing")
    #print(f"Blue scoreboard: {verified_bluesb}")

    #--------------- Red scoreboard begins ------------------- #
    redsb_region = gray_array[850:1070, 1005:1195]
    redsb_img = pre_img(redsb_region, 200, threshold=(85,255),blur=(3,3))
    redpytest = pytesseract.image_to_string(redsb_img,config=redsb_config)
    #cv2.imshow('header_score_img',redsb_img)
    #if cv2.waitKey(1) & 0xFF==ord('0'):
    #0    break
    #Verify red scoreboard
    verified_redsb = ws.verify_redsb(redpytest)
    if verified_redsb == False:
        print("Red scoreboard not valid")
        continue

    # if ((verified_bluesb == False) or (verified_redsb == False)):
    #     blue_df = pd.DataFrame(blue_dict_opt,index=[newTime])
    #     red_df = pd.DataFrame(red_dict_opt,index=[newTime])
    #     #df.to_csv(output_csv,mode='a',index=False,header=False)
    #     with open(output_csv, 'a') as f:
    #         blue_df.to_csv(f, header=f.tell()==0)
    #         red_df.to_csv(f,header=f.tell()==0)
    #     continue
    #else:
    #print("success, continuing")
    #print(f"Red scoreboard: {verified_redsb}")



    #-----------------------CSV Pre-processing---------------------#
    final_bluestats = [x for xs in verified_bluesb for x in xs]
    final_redstats = [x for xs in verified_redsb for x in xs]
    #Bandage fix. Find a way to efficiently iterate and apply these
    #DRY CODE
    blue_dict_csv['top_kill'] = final_bluestats[0]
    blue_dict_csv['top_death'] = final_bluestats[1]
    blue_dict_csv['top_assist'] = final_bluestats[2]
    blue_dict_csv['top_gold'] = final_bluestats[3]
    blue_dict_csv['jungle_kill'] = final_bluestats[4]
    blue_dict_csv['jungle_death'] = final_bluestats[5]
    blue_dict_csv['jungle_assist'] = final_bluestats[6]
    blue_dict_csv['jungle_gold'] = final_bluestats[7]
    blue_dict_csv['mid_kill'] = final_bluestats[8]
    blue_dict_csv['mid_death'] = final_bluestats[9]
    blue_dict_csv['mid_assist'] = final_bluestats[10]
    blue_dict_csv['mid_gold'] = final_bluestats[11]
    blue_dict_csv['bot_kill'] = final_bluestats[12]
    blue_dict_csv['bot_death'] = final_bluestats[13]
    blue_dict_csv['bot_assist'] = final_bluestats[14]
    blue_dict_csv['bot_gold'] = final_bluestats[15]
    blue_dict_csv['supp_kill'] = final_bluestats[16]
    blue_dict_csv['supp_death'] = final_bluestats[17]
    blue_dict_csv['supp_assist'] = final_bluestats[18]
    blue_dict_csv['supp_gold'] = final_bluestats[19]
    #Bandage fix. Find a way to efficiently iterate and apply these
    #DRY CODE
    red_dict_csv['top_kill'] = final_redstats[0]
    red_dict_csv['top_death'] = final_redstats[1]
    red_dict_csv['top_assist'] = final_redstats[2]
    red_dict_csv['top_gold'] = final_redstats[3]
    red_dict_csv['jungle_kill'] = final_redstats[4]
    red_dict_csv['jungle_death'] = final_redstats[5]
    red_dict_csv['jungle_assist'] = final_redstats[6]
    red_dict_csv['jungle_gold'] = final_redstats[7]
    red_dict_csv['mid_kill'] = final_redstats[8]
    red_dict_csv['mid_death'] = final_redstats[9]
    red_dict_csv['mid_assist'] = final_redstats[10]
    red_dict_csv['mid_gold'] = final_redstats[11]
    red_dict_csv['bot_kill'] = final_redstats[12]
    red_dict_csv['bot_death'] = final_redstats[13]
    red_dict_csv['bot_assist'] = final_redstats[14]
    red_dict_csv['bot_gold'] = final_redstats[15]
    red_dict_csv['supp_kill'] = final_redstats[16]
    red_dict_csv['supp_death'] = final_redstats[17]
    red_dict_csv['supp_assist'] = final_redstats[18]
    red_dict_csv['supp_gold'] = final_redstats[19]

    blue_dict_opt.update(blue_dict_csv)
    red_dict_opt.update(red_dict_csv)
    # for x, y in enumerate(blue_dict_csv.items()):
    #     if y[1] is None:
    #         iter = x-5
    #         blue_dict_csv[y[0]] = final_bluestats[iter]

    # for x, y in enumerate(red_dict_csv.items()):
    #     if y[1] is None:
    #         iter = x-5
    #         red_dict_csv[y[0]] = final_redstats[iter]
    print(f"blue_dict_csv:{blue_dict_csv}\n")
    print(f"red_dict_csv: {red_dict_csv}\n") 
    blue_df = pd.DataFrame(blue_dict_csv,index=[oldTime])
    red_df = pd.DataFrame(red_dict_csv,index=[oldTime])
    #df.to_csv(output_csv,mode='a',index=False,header=False)
    with open(output_csv, 'a') as f:
        blue_df.to_csv(f, header=f.tell()==0)
        red_df.to_csv(f,header=f.tell()==0)
    #et = time.time()    
    #elapsed_time = et - st
    #print('Execution time:', elapsed_time, 'seconds')
    
cv2.destroyAllWindows()

