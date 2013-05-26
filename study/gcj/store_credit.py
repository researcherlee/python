'''
Created on 2012. 10. 7.

@author: lee
'''


INPUT_NAME = r"C:\Users\lee\Downloads\A-large-practice.in"
OUTPUT_NAME = INPUT_NAME + ".out.txt"

inputLines = open(INPUT_NAME).readlines()
outputFp = open(OUTPUT_NAME, "w")

testcaseNum = int(inputLines[0])

for i in range(testcaseNum):
    
    credit = int(inputLines[(i*3)+1])
    productList = [ int(z) for z in inputLines[(i*3)+3].split() ]
    originalList = productList[:]
    productList.sort(reverse=True)
    foundValue = None
    for j in range(len(productList)):
        for k in range(j+1, len(productList)):
            value = productList[j] + productList[k]
            if value == credit:
                foundValue = (productList[j], productList[k])
                break
            if value < credit:
                break
        if foundValue != None:
            break
        
    index1 = originalList.index(foundValue[0]) + 1
    if foundValue[0] == foundValue[1]:
        index2 = originalList.index(foundValue[1], index1) + 1
    else:
        index2 = originalList.index(foundValue[1]) + 1
    if index1 > index2:
        t = index2
        index2 = index1
        index1 = t
    print "Case #%d: %d %d" % (i+1, index1, index2)
    outputFp.write("Case #%d: %d %d\n" % (i+1, index1, index2))

outputFp.close()

