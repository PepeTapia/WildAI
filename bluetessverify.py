#Create a blue side scoreboard text preprocessor that occurs during the live video feed - TAKE INSPIRATION FROM THE SCRIPTS BELOW

#Input is a text block that has white space '\x0c' and '\n'
#Output is a list of lists that have 

import re 
import sbverify
def bluetessverify(bluepytext):
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


    if sbverify(bluestats) is False:
        print("ya did it, ya caught a bad scoreboard!")
        notValid = False
        return notValid
    else: 
        return bluestats