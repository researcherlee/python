'''
Created on 2009. 8. 14.

'''


import os
import sys

# # test
def addmember (memberlist, newmember):
    if newmember not in memberlist:
        memberlist.append(newmember)
        

def account_balance(initialBalance):
    balance = initialBalance
    def withdraw(amount):
        balance = balance - amount
        return balance
    def deposit(amount):
        balance = balance + amount
        return balance
    range(1, 3)
    return withdraw, deposit

def _testImport():
    print "testImport"

def __testImport__():
    print "__testImport__"
####

# example 1
def frange(*arg):
    startV = 0.0
    step = 0.25
    tolerate = 7  # round position
    
    arg = [ round(float(i), tolerate) for i in arg]
    
    if len(arg) == 1:
        endV = arg[0]
        
    
    elif len(arg) == 2:
        startV = arg[0]
        endV = arg[1]
    
    elif len(arg) == 3:
        startV = arg[0]
        endV = arg[1]
        step = arg[2]
        if step == 0 or step == 0.0:
            raise ValueError, "frange() step argument must not be zero"
       
    else:
        raise TypeError, "frange() expected at most 3 arguments, got %d" % (len(step))


    ret = []
    if step > 0.0:
        while startV < endV :
            ret.append(startV)
            startV = round(startV + step, tolerate)
    else:
        while startV > endV :
            ret.append(startV)
            startV = round(startV + step, tolerate)

    return ret

# example2
def adder(o1, o2):
    return ((o1 + o2) / 2, (o1 + o2) % 2)

# example3
def getImages(files, thumb=True, normal=True):
    ''' filter _thumb.jpg'''
    thumbs = []
    normals = []
    if thumb == True:
        thumbs.extend([ f for f in files if f.endswith("_thumb.jpg") ])
    if normal == True:
        normals.extend([ f for f in files if f.endswith(".jpg") and f.endswith("_thumb.jpg") == False ])
    
    return thumbs + normals

# example4
def str2list(s):
    import StringIO    
    import operator
    x, y, z = "", "", ""
    
    l = ["", "", ""]
    
    sock = StringIO.StringIO(s)
    
    for i, line in enumerate(sock):
        l[i] = line
        
    x, y, z = l
    
    x, y, z = map(lambda s: [ int(i) for i in s.split()], l)
    
    print "x %s %d" % (str(x), reduce(operator.add, x))
    print "y %s %d" % (str(y), reduce(operator.add, y))
    print "z %s %d" % (str(z), reduce(operator.add, z))  
    

# example5

def replaceList(l, o, n):
    '''
    replace o to n in list l
    '''
    
    for i, item in enumerate(l):
        if type(item) == type([]):
            replaceList(item, o, n)
        elif l[i] == o:
            l[i] = n


print "module start"
