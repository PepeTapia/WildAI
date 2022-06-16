#This function is a scoreboard text preprocessor that verifies the following:
#Scoreboard is a list of 5 items
    #Each item in the list has a total of 4 items
        #Any potential number validation will be done in post-processing when handling data
#returns False or returns a verified list of lists in <str> format

def sbverify(sbtext):
    verify = False
    if len(sbtext) == 5:
    #print("it's the right size!")
        for player in sbtext:
            if len(player) == 4:
                for stat in player:
                    verify = True
            else:
                #print("there is a player stat list that is not complete")
                verify = False
                break
    else:
        #print("the scoreboard is incomplete")
        verify = False
    return verify