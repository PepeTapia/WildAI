# import numpy as np
# import pandas as pd
# import matplotlib.pylab as plt

# df = pd.read_csv(r'A:\CodingProjects\WildAI\WildAI\Datasets\STMN vs JDG Play-in\Game1.csv',index_col='Time')


# s = pd.Series(np.random.randn(5))

# print(s)

# print(s+s)

# print(s[0])
# print(s[[1,4]])

# new_df = df['team_gold'].diff()
# df['gold diff'] = df['team_gold'].diff()
# print(new_df)
# df.plot(x='time', y='gold diff', kind='line')
# plt.show()

# new_df = df.loc[40]
# gold_df = new_df.at[40,'team_gold']
# print(type(gold_df))

import time
import cv2
from timeit import default_timer as timer
import tesserocr
import mss
import numpy as np
from PIL import Image

# import pyautogui
def pre_img(img_array, scale, threshold=(120,255), blur=(3,3)):
    #start = timer()
    new_img = img_array
    width = int(new_img.shape[1] * scale/100)
    height = int(new_img.shape[0] * scale/100)
    dim = (width,height)
    tess_img = cv2.resize(new_img, dim, interpolation=cv2.INTER_CUBIC)
    ret, tess_img = cv2.threshold(tess_img,threshold[0],threshold[1],cv2.THRESH_BINARY_INV)
    tess_img = cv2.blur(tess_img,blur)
    end = timer()
    #print("pre_img time elapsed: {}".format(end - start))
    return tess_img

with mss.mss() as sct:

    #monitor = {"top": 40, "left":  0, "width": 800, "height": 640}
    monitor = sct.monitors[1]
    while "Screen capturing":
        #last_time = time.time()
        scoreboard = {"top": 845, "left":720, "width":195, "height": 225}
        img = np.array(sct.grab(scoreboard))
        img = cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
        img = pre_img(img,150, threshold=(115,255),blur=(1,1))
        print(img.shape)
        im = Image.fromarray(img)
        
        #cv2.imshow("mss", im)
        #start = timer()
        result = tesserocr.image_to_text(im,psm=6, oem=1)
        #end = timer()
        #print("TOTAL time elapsed: {}".format(end - start))
        print("result: ", result)
        
        #print(tesserocr.get_languages())
        exit()
        #scoreboard = pyautogui.screenshot()
        #screen_array = np.array(scoreboard)
        #cv2.imshow("pyautogui", screen_array)

        #print("fps: {}".format(1/(time.time()-last_time)))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

# import easyocr
# import cv2
# from matplotlib import pyplot as plt
# import numpy as np
# from timeit import default_timer as timer
# import tesserocr
# from PIL import Image
# start = timer()
# IMAGE_PNG = r'A:\CodingProjects\WildAI\Images\time.png'
# #reader = easyocr.Reader(['en'], gpu=True)
# start = timer()
# #result = reader.readtext(IMAGE_PNG,detail=0, batch_size=32, allowlist=":/0123456789")
# #result = pytesseract.image_to_string(IMAGE_PNG)
# im = Image.open(IMAGE_PNG)
# result = tesserocr.image_to_text(im)
# print(result)
# end = timer()
# print("TOTAL time elapsed: {}".format(end - start))
