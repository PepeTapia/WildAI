import re


def timetextverify(timetext):
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
        #Each minute passed will value at 60 seconds
        tempMinutes = int(timetemp[0]) * 60
        seconds = int(timetemp[1]) + tempMinutes
        #print(seconds)
        return seconds
