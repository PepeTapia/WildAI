#Create a red side scoreboard text preprocessor that occurs during the live video feed - TAKE INSPIRATION FROM THE SCRIPTS BELOW
import re
import sbverify
def redtessverify(redpytext):
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


    if sbverify(redstats) is False:
        print("ya did it, ya caught a bad scoreboard!")
        notValid = False
        return notValid
    else:
        return redstats