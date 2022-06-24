#This module contains verification methods that interact with regions of interest to text

import re 


def bluesb(bluepytext):
    notValid = None
    #Blue stats list that will ultimately be returned
    bluestats= []
    
    #Blue temp list that is used for processing
    bluetemp = []

    #Remove all 'x0c' - similar to \f
    bluetemp = bluepytext.strip('\x0c')

    #Split into each respective role
    bluetemp = bluetemp.splitlines()

    #Preprocess scoreboard text
    for i in bluetemp:
        #re.sub will substitute the / from KDA and turn it into an empty space
        bluetemp = re.sub(r'/',' ',i)
        #re.split will create a list at each ' ', space, and split from there
        bluetemp = re.split(r' ',bluetemp)
        #print(bluestats)
        bluestats.append(bluetemp)


    if verify_sb(bluestats) is False:
        print("Bad scoreboard!")
        notValid = False
        return notValid
    else: 
        return bluestats



def redsb(redpytext):
    notValid = None

    #Red stats list that will ultimately be returned
    redstats= []
    
    #Red temp list that is used for processing
    redtemp = []

    #Remove all 'x0c' - similar to \f
    redtemp = redpytext.strip('\x0c')

    #Split into each respective role
    redtemp = redtemp.splitlines()

    #Preprocess scoreboard text
    for i in redtemp:
        #re.sub will substitute the / from KDA and turn it into an empty space
        redtemp = re.sub(r'/',' ',i)
        #re.split will create a list at each ' ', space, and split from there
        redtemp = re.split(r' ',redtemp)
        #In the case of redstats, I move the gold to the back, to match blue side stats and prepares for further verification
        redtemp.insert(len(redtemp),redtemp.pop(0))
        #print(redtemp)
        redstats.append(redtemp)


    if verify_sb(redstats) is False:
        print("Bad scoreboard!")
        notValid = False
        return notValid
    else:
        return redstats



def verify_sb(sbtext):
    verify = False
    if len(sbtext) == 5:
    #print("it's the right size!")
        for player in sbtext:
            if len(player) == 4:
                for stat in player:
                    if stat == '':
                        #print("there is a player stat that is not complete")
                        verify = False
                        return verify
                    else:    
                        verify = True
            else:
                verify = False
                return verify
    else:
        #print("the scoreboard is incomplete")
        return verify
    return verify

# This script takes int and turns it into a 00:00 min:sec time 
def time(timetext):
    #The base case will be used as a comparison to keep track of the time. 
    #If the incoming time is less than or the same as the cached time - False and you can continue in the main function
    #If the incoming time is greater than the cached time - True and you can finish the main function
    verify = False

    timetemp = []
    
    seconds = 0
    #Remove all 'x0c' - similar to \f
    timetemp = timetext.strip('\x0c')
    timetemp = timetext.strip(':')
    timetemp = re.sub("[^0-9:]", "", timetemp)
    timetemp = re.split(':', timetemp)

    if len(timetemp) != 2:
        verify = False
        #print(timetemp)
        return verify
    else:

        #print(timetemp)
        
        #String of "MM:SS" turned into integer of seconds
        #timetemp[0] is minutes, turn into seconds
        tempMinutes = int(timetemp[0]) * 60
        #timetemp[1] is seconds, add tempMinutes for total seconds
        seconds = int(timetemp[1]) + tempMinutes
        #print(seconds)
        return seconds




def int_time_to_text(time_int):
    minutes = time_int // 60 # // is to ensure it is always an int
    seconds = time_int % 60
    time_string = str("%02d:%02d" %(minutes,seconds))
    #print(minutes)
    #print(seconds)
    return time_string


#def text_to_data(scoreboardtext):
#    pass