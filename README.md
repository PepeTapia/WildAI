# WildAI
Wild Rift AI uses Computer Vision techniques to extract text and detect images from video input of a full display of a Wild Rift game.
Consider this a barebones project to get started with screenshots. The current project is still under development and review for long term sustainability, though this is the starting point for anyone wanting to replicate it.

# Table of Contents

- [Why I started this project!](#1-why-i-started-this-project)
- [What is the task at hand?](#2-what-is-the-task-at-hand)
- [What steps were taken to solve the task?](#3-what-steps-were-taken-to-solve-the-task)
- [Issues and resolutions](#4-issues-and-resolutions)
- [What were the results to the project?](#5-what-were-the-results-to-the-project)
- [What I learned](#6-what-i-learned)


# 1. Why I started this project!
<p>This project was created for a video game titled "Wild Rift", a mobile phone game created by the company Riot Games. At the time this project was created, there was a competitive esports scene that lacked a proper way to perform data analytics since there was no public API to pull data from. The parent game, League of Legends, has a thriving esports scene through the use of public and private APIs. These teams use Data Science practices to analyze their team and the opposing teams.</p>

# 2. What is the task at hand?
<p> The Wild Rift game client has two ways to access this data, through a live spectate during the game or a Video On Demand(VOD) after the game has ended. In both modes, teams would have to rewatch the games a few times to analyze their strengths and weaknesses, then they would have to go back again to look at the scoreboard for any significant data such as: Gold Difference, Vision Trinket Usage, Kill/Death/Assist Ratio, and more. My task was the find a way to record as much available data as possible on the given display. </p>

2.1 **Example of the given display**
<p>Screenshot of the game display from which we pull data from. Credit: Riot Games Wild Rift: Icons event.</p>

![Full screen display that provides access to the Wild Rift game data.](https://github.com/PepeTapia/WildAI/blob/main/images/colorscale_img.png)

# 3. What steps were taken to solve the task?
**3.1 Requirements:**
- Connect a mobile phone display to a streaming or recording platform. 
- Use a video feed, live streamed or recorded, from the game with the scoreboard open at all times. The program can handle the case where the scoreboard is down for a bit of time, but not too long!

**3.2 Coding tasks:**<br>
Use Computer Vision tools to extract data from the video feed. I used Pytesseract, a Python Wrapper for Google's Tesseract-OCR Engine. Optical character recognition worked well here because I am grabbing only numbers from 0-10. 

<p>Pytesseract configuration</p>

`'--oem 3 --psm 7 digits -c tessedit_char_whitelist="0123456789"'`

<p>Which gets processed through the pytesseractt image_to_string method. Here is an example of processing the time displayed. </p>

`pytesseract.image_to_string(time_img,config=time_config)` 

**Step 1:** Screenshot a frame and convert it to grayscale. Doing so will help deal with the variety of color that differentiates "Blue" and "Red" side of the teams.

![Grayscale version of the full screen display that provides access to the Wild Rift game data.](https://github.com/PepeTapia/WildAI/blob/main/images/grayscale_img.png)

From here, we categorize the data needed:
- Time
- Blue Towers
- Red Towers
- Blue team gold
- Red team gold
- Blue team kills
- Red team kills

From here, we categorize the data needed:
| Location on screenshot | Data Available |
| ------ | ------ |
| Header scoreboard | Time, Blue/Red Towers, Blue/Red team gold, Blue/Red team kills|
| Blue side bottom scoreboard | 5 Individual rows each containing: Kills/Death/Assists, Gold, Vision Trinket|
| Red side bottom scoreboard| 5 Individual rows each containing: Kills/Death/Assists, Gold, Vision Trinket |

**Step 2:** Image processing must be done to leverage Pytesseract efficiently and I accomplish this by generalizing the image processing with the following transformations:

**Parameters:**

**Scale**
: changes depending on the images. I found that some data categories requires different scalings.

**Threshold**
: works only for grayscale images and allows for a minimum pixel value to be set, and a maximum value. Anything below the miniumum pixel value is set to zero.

**Blur**
: helps us round out the images a bit, defaulting to (3,3) but it could vary depending on the data category

```Python
def pre_img(img_array, scale, threshold=(120,255), blur=(3,3)):
```

<p>The following is the processing that takes place, where we create a copy of the image, rescale it, apply the threshold, and blur. <br>
Current improvements would be to change from "copying the image" to processing it "in-place". </p>


```Python
#Use the timer to keep track of any bottlenecks that can happen in this processing, we want 60fps and it starts here.
#start = timer()

# New image created from the original
new_img = img_array

# Rescale the image
width = int(new_img.shape[1] * scale/100)
height = int(new_img.shape[0] * scale/100)

# Grab new dimensions
dim = (width,height)

# Resize it to prepare it as a tesseract ready image
tess_img = cv2.resize(new_img, dim, interpolation=cv2.INTER_CUBIC)

# tess_img is what we are working with
ret, tess_img = cv2.threshold(tess_img,threshold[0],threshold[1],cv2.THRESH_BINARY_INV)
tess_img = cv2.blur(tess_img,blur)

#end = timer()
#print("pre_img time elapsed: {}".format(end - start))

return tess_img
```

|Data Category| Grayscale image | Processed Image |
| ------ | ------ | ------ | 
| Header scoreboard | ![Header Scoreboard in grayscale](https://github.com/PepeTapia/WildAI/blob/main/images/scoreboard_gray.png) | ![Header Scoreboard postprocess ](https://github.com/PepeTapia/WildAI/blob/main/images/scoreboard_processed.png) |
| Header scoreboard (Time) | ![Grayscale image of time](https://github.com/PepeTapia/WildAI/blob/main/images/grayscale_time.png) | ![Time image postprocess](https://github.com/PepeTapia/WildAI/blob/main/images/grayscale_resize.png) |
| Blue side bottom scoreboard | ![Grayscale Blue side bottom scoreboard](https://github.com/PepeTapia/WildAI/blob/main/images/bluesb_gray.png) |![Blue side bottom scoreboard postprocess](https://github.com/PepeTapia/WildAI/blob/main/images/bluesb_processed.png) |
| Red side bottom scoreboard | ![Grayscale Red side bottom scoreboard](https://github.com/PepeTapia/WildAI/blob/main/images/redsb_gray.png) | ![Red side bottom scoreboard postprocess](https://github.com/PepeTapia/WildAI/blob/main/images/redsb_processed.png) |

**Resulting Dataframe**

<p>Screenshot of the terminal</p>

![Screenshot of the terminal that has output of the program while running](https://github.com/PepeTapia/WildAI/blob/main/images/processing_output.png)

<p>Output csv headers, visually seperated for clarity.</p>

- Time, index value that is the in-game time as an integer. 02:00 would be index 120
- time, the time value as a strsing. 02:00 would show as string "02:00"
- Team, the string 3 code value that represents a team.
- towers ,team_gold, team_kills are within the Header scoreboard
- top_, jungle_, mid_, bot_, supp_ prefixes contain the data represented from the individual rows on the respective Blue or Red scoreboard

```
Time,time,team,towers,team_gold,team_kills,
top_kill,top_death,top_assist,top_gold,
jungle_kill,jungle_death,jungle_assist,jungle_gold,
mid_kill,mid_death,mid_assist,mid_gold,
bot_kill,bot_death,bot_assist,bot_gold,
supp_kill,supp_death,supp_assist,supp_gold
```

<p>Example of the first few rows of a dataframe</p>

```
29,00:29,STM,0,2800,0,0,0,0,524,0,0,0,524,0,0,0,734,0,0,0,524,0,0,0,524
29,00:29,JDG,0,2800,0,0,0,0,524,0,0,0,524,0,0,0,654,0,0,0,524,0,0,0,524
30,00:30,STM,0,2800,0,0,0,0,528,0,0,0,528,0,0,0,738,0,0,0,528,0,0,0,528
30,00:30,JDG,0,2900,0,0,0,0,528,0,0,0,528,0,0,0,658,0,0,0,528,0,0,0,528
31,00:31,STM,0,2900,0,0,0,0,531,0,0,0,531,0,0,0,741,0,0,0,531,0,0,0,531
31,00:31,JDG,0,2800,0,0,0,0,531,0,0,0,531,0,0,0,661,0,0,0,531,0,0,0,531
32,00:32,STM,0,2900,0,0,0,0,535,0,0,0,535,0,0,0,745,0,0,0,535,0,0,0,535
32,00:32,JDG,0,2800,0,0,0,0,535,0,0,0,535,0,0,0,705,0,0,0,535,0,0,0,535
33,00:33,STM,0,3000,0,0,0,0,603,0,0,0,538,0,0,0,748,0,0,0,538,0,0,0,538
33,00:33,JDG,0,2900,0,0,0,0,603,0,0,0,538,0,0,0,708,0,0,0,538,0,0,0,538
34,00:34,STM,0,3000,0,0,0,0,607,0,0,0,542,0,0,0,752,0,0,0,542,0,0,0,542
34,00:34,JDG,0,3200,0,0,0,0,607,0,0,0,542,0,0,0,712,0,0,0,607,0,0,0,574
35,00:35,STM,0,3000,0,0,0,0,610,0,0,0,545,0,0,0,755,0,0,0,545,0,0,0,545
35,00:35,JDG,0,3200,0,0,0,0,675,0,0,0,545,0,0,0,755,0,0,0,610,0,0,0,578
36,00:36,STM,0,3000,0,0,0,0,614,0,0,0,549,0,0,0,759,0,0,0,549,0,0,0,549
36,00:36,JDG,0,3200,0,0,0,0,679,0,0,0,549,0,0,0,789,0,0,0,614,0,0,0,581
37,00:37,STM,0,3100,0,0,0,0,686,0,0,0,556,0,0,0,766,0,0,0,556,0,0,0,556
37,00:37,JDG,0,3200,0,0,0,0,686,0,0,0,556,0,0,0,766,0,0,0,621,0,0,0,588
38,00:38,STM,0,3200,0,0,0,0,689,0,0,0,589,0,0,0,769,0,0,0,559,0,0,0,559
38,00:38,JDG,0,3300,0,0,0,0,729,0,0,0,559,0,0,0,769,0,0,0,624,0,0,0,592
40,00:40,STM,0,3300,0,0,0,0,693,0,0,0,563,0,0,0,773,0,0,0,628,0,0,0,595
40,00:40,JDG,0,3400,0,0,0,0,733,0,0,0,563,0,0,0,773,0,0,0,693,0,0,0,628
```

**Yolov5 testing and potential**

I used opencv's matchTemplate() to keep track of Vision Trinkets, creating flags of Active and Unactivate states for them. A bordered trinket indicates the Vision Trinket has not been used and unborded means it has been used. This helps us find patterns for both our players and enemy players.

![Ward detection with yellow borders indicating not used and no borders indicating used]]https://github.com/PepeTapia/WildAI/blob/main/images/wardDetection.gif

I attempted using Yolov5, and it still has room for exploration for detecting all champions and all items, but that will be for a later time. In most cases it is easiest to just write down the champs in some type of GUI when recording the data.

# 4. Issues and resolutions

**Data validation**
<p>As you can see from the headers above, there is a gap between index 38 and index 40. Index "39" is missing, but index 29 is not missing. The most common error when starting were the amount of frames being read, typically I would get .75-1.25 framse per second, which makes sense why an index would be skipped. Once I changed to my current methods I improved to 60 frames per second, but if I get a skip at those frames that must mean the OCR is not picking up the time properly.</p>

These can be found in [wildscripts.py](https://github.com/PepeTapia/WildAI/blob/main/wildscripts.py)


```Python
def verify_time(timetext):
    # Clears all empty spaces from potential hidden characters like 'x0c'
    # Next it changes the 00:00 time to an integer, if it successfully does this that implies the 00:00 was valid as well
    # Returns an integer that is then used for an index

def verify_redsb(redpytext):
    # Clears all empty spaces from potential hidden characters like 'x0c'
    # Since this is the red side scoreboard we have to handle Gold then Kills/Deaths/Assists, specifically clearing the '/' characters using re.sub()
    # With all the empty spaces, I use re.split() to separate the text
    # Append each seperate text into a list using .append()
    # Red side required it's own method because of the different format, so I popped the 'Gold' to the back of the list and returned it.

def verify_bluesb(bluepytext):
    # Clears all empty spaces from potential hidden characters like 'x0c'
    # Since this is the red side scoreboard we have to handle Gold then Kills/Deaths/Assists, specifically clearing the '/' characters using re.sub()
    # With all the empty spaces, I use re.split() to separate the text
    # Append each seperate text into a list using .append()

def verify_sb(sbtext):
    # This ensures that each scoreboard contains the text needed: Gold, Kills, Death, Assists
    # If the data is not valid then we skip the data and instead use the last successful scorerboard data

def team_gold_verify(team_gold):
  # Clears all empty spaces from potential hidden characters like 'x0c' and '\n'
  # Since this is the team_gold from the header scoreboard, it is read as a 0.0 value while removing the '.' and is multiplied by 100, ex: 43k -> 43 -> 4300

def header_int_verify(tower_or_kills):
  # Clears all empty spaces from potential hidden characters like 'x0c' and '\n'
  # Verifies each individual digit from Tower or Kill into a digit
```




# 5. What were the results to the project?

I began this project early in the competitive season, and it helped our team to understand our strengths and weaknesses which led to making data led decisions on top of regular discussions. There is still a lot of room for data processing, cleaning, and potential usage using AI/ML to create fun data points, but I chose to focus more on school which led to newer projects. 

# 6. What I learned aboue this project. 

I learned a lot about this project, including: Computer Vision techniques, YoloV5, Data Processing methods: Extraction, Validation, and creating CSVs. I hope to continue this as a passion project once I finish school!
