'''
Created on 2012. 10. 7.

@author: lee
'''

INPUT_NAME = r"C:\Users\lee\Downloads\B-large-practice.in"
OUTPUT_NAME = INPUT_NAME + ".out.txt"

inputLines = open(INPUT_NAME).readlines()
outputFp = open(OUTPUT_NAME, "w")

testcaseNum = int(inputLines[0])

for i in range(testcaseNum):
    
    wordList = inputLines[i+1].split()
    wordList.reverse()
    result = " ".join(wordList)
    print "Case #%d: %s" % (i+1, result)
    outputFp.write("Case #%d: %s\n" % (i+1, result))

outputFp.close()
