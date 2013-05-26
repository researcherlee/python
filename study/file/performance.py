# -!- coding: utf-8 -!-

'''
Created on 2009. 8. 9.

Benchmark to read and print from file.
Using readlines, read, xreadlines, 반복??'''

import os
import time
import sys

def usingDefault(files):
    for f in files:
        fsock = open(f)
        for line in fsock:
            print line

def usingReadlines(files):
    for f in files:
        fsock = open(f)        
        for line in fsock.readlines():
            print line

def usingXreadlines(files):
    for f in files:
        fsock = open(f)
        for line in fsock.xreadlines():
            print line


def usingReadline(files):
    for f in files:
        fsock = open(f)
        line = fsock.readline()
        while line:
            print line
            line = fsock.readline()

def usingRead(files):
    for f in files:
        fsock = open(f)
        line = fsock.read()
        print line

def usingReadlinesOpt(files):
    for f in files:
        fsock = open(f)
        print '\n'.join(fsock.readlines())
        
def main():
#    if len(sys.argv) < 2:
#        print >> sys.stderr, "usage: performace file [files..]"
#        sys.exit()
#        
    functions = [ f for f in globals() if f.startswith("using") ]
    
    result = ""
    for func in functions:
        f = getattr(sys.modules["__main__"], func)
        t = time.clock()
        f([ "/Users/aa" + os.sep + f for f in os.listdir("/Users/aa") if os.path.isfile("/Users/aa" + os.sep + f) ])
        t = time.clock() - t
        result = result + "%s : %.3f clock\n" % (func, t)
    print result

        
if __name__ == "__main__":
    main()
    
