'''
Created on 2012. 10. 7.

@author: lee
'''

numberDict = {} 

def getBiggerNumberList(num):
    
    numStr = str(num)
    retList = []
    for i in range(1, len(numStr)):
        newNum = int(numStr[i:] + numStr[0:i])
        if newNum > num and newNum not in retList:
            retList.append(newNum)
    
    return retList


for i in range(1, 2000000):
    numberDict[i] = getBiggerNumberList(i) 

#for i, v in numberDict.items():
#    print "%d : %s" % (i, v)

INPUT_NAME = r"C:\Users\lee\Downloads\C-large-practice.in"
OUTPUT_NAME = INPUT_NAME + ".out.txt"

inputLines = open(INPUT_NAME).readlines()
outputFp = open(OUTPUT_NAME, "w")

testcaseNum = int(inputLines[0])

for i in range(testcaseNum):
    minNum, maxNum = inputLines[i+1].split()
    minNum = int(minNum)
    maxNum = int(maxNum)
    result = 0
    for j in range(minNum, maxNum):
        result += len([ xx for xx in numberDict[j] if xx <= maxNum ])
    print "Case #%d: %d" % (i+1, result)
    outputFp.write("Case #%d: %d\n" % (i+1, result))

outputFp.close()