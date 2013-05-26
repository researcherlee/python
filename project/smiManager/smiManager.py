'''
Created on 2010. 1. 10.

@author: reliableelee
'''

import re, sys

usage = """
This script is for syncronizing the smi file

usage: smiManager (-Number | +Number) orgFileName
    -Number: It puts the script to Number/1000 sec in the past
    +Number: It puts the script to Number/1000 sec in the future

"""

timePattern = re.compile("Start=(\d+)")

def smiManager(doc, number):
    d = doc
    result = ""
    while True:
        sre = timePattern.search(d)
        if not sre:
            result += d 
            break
        newNumber = int(sre.group(1)) + number
        if newNumber < 0:
            raise "Some start=Number have minus value after calculating. Check number argu"
        result += d[:sre.start()] + "Start=" + str(newNumber)
        d = d[sre.end():]
    
    return result
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print usage
        sys.exit(12)
    
    number = 0
    try:
        number = int(sys.argv[1])
    except:
        print usage
        print str(sys.exc_info()[1])
        sys.exit(12)
    
    stream = open(sys.argv[2])
    
    output = smiManager(stream.read(), number)
    print output
    
    
    
    
    