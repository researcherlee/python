'''
Created on 2012. 8. 21.

@author: lee
'''

import sys, os

BLOCK_SIZE = 1024*4

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: jcopy.py srcPath dstDir"
        sys.exit(-1)
    
    srcPath = sys.argv[1]
    destPath = sys.argv[2]
    
    if os.path.isdir(destPath) == False:
        print "%s desDir is not directory" % destPath
        sys.exit(3)
    
    if os.path.exists(srcPath) == False or  os.path.isfile(srcPath) == False:
        print "%s is not existing file" % srcPath
        sys.exit(2)
    
    destPath = os.path.join(destPath, os.path.basename(srcPath))
    
    if os.path.exists(destPath):
        currentSize = os.path.getsize(destPath)
    else:
        currentSize = 0
        
    maxSize = os.path.getsize(srcPath)
        
    sFp = file(srcPath, "rb")
    dFp = file(destPath, "ab")
    sFp.seek(currentSize)
    
    while currentSize < maxSize:
        readBytes = min (maxSize - currentSize, BLOCK_SIZE)
        data = sFp.read(readBytes)
        dFp.write(data)
        dFp.flush()
        currentSize += len(data)
    
    
    
        
    
