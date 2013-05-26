'''
Created on 2009. 8. 24.

'''

# Ex 6: Design Counter Class

class Counter:
    step = 1
    def __init__(self, value=0):
        self.value = value
    
    def incr(self):
        self.value += self.step
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
    def __call__(self):
        self.incr()
        return self.value
    
    def __coerce__(self, x):
        return self.value, x
    

# Ex 7 Define Set
import types

class Set:
    def __isIterable(self, i):
        if type(i) == type(()) or type(i) == type([]) or type(set([])) == type(i):
                return True         
        elif type(i) == types.InstanceType and i.__class__ == Set:
                return True
        return False
        
    def __init__(self, *data):
        self.data = []
        for i in data:
            if self.__isIterable(i):
                self.data.extend(i)
            else:
                self.data.append(i)
        self.data = list(set(self.data))
        
    def __and__(self, op):
        if self.__isIterable(op) == False:
            op = [ op ]
        retList = []
        for item in op:
            if item in self:
                retList.append(item)
        return Set(retList)
        
    def __rand__(self, op):
        return self.__and__(op)
    
    def __or__(self, op):
        if self.__isIterable(op) == False:
            op = [ op ]
        op = list(op)
        return Set(list(set(self.data + op)))
    
    def __ror__(self, op):
        return self.__or__(op)
    
    def __sub__(self, op):
        if self.__isIterable(op) == False:
            op = [ op ]
        retList = []
        for item in self:
            if item not in op:
                retList.append(item)
        return Set(retList)
    
    def __rsub__(self, op):
        if self.__isIterable(op) == False:
            op = [ op ]
        retList = []
        for item in op:
            if item not in self:
                retList.append(item)
        return Set(retList)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __delitem__(self, key):
        del self.data[key]
    
    def __contain__(self, value):
        if value in self.data:
            return True
        return False
    
    def __nonzero__(self):
        if self.data == []:
            return False
        return True 
    
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return str(self.data)
    

class BNode(object):
    def __init__(self, value=None, left=None, right=None, depth=1):
        self._left = None
        self._right = None
        self._depth = 0
        self.value = value
        
        self.setleft(left)       
        self.setright(right)
        self.setdepth(depth)
        
    def __repr__(self):
        return "%s (\n%s%s\n%s%s)" % (self.value, "  "*self.depth, self.left,
                                      "  "*self.depth, self.right)
#    
#    def __setitem__(self, key, value):
#        print key, value
#        if key == "left" or key == "right":
#            value.depth = self.depth + 1
#            self.__dict__[key] = value
#        elif key == "depth":
#            self.__dict__[key] = value
#            if self.left != None:
#                self.left.depth = value + 1
#            if self.right != None:
#                self.right.depth = value + 1
    
    def getleft(self):
        return self._left
    
    def setleft(self, c):
        if c != None:
            c.depth = self.depth + 1
        self._left = c
    
    def getright(self):
        return self._right
    
    def setright(self, c):
        if c != None:
            c.depth = self.depth + 1
        self._right = c
    
    def getdepth(self):
        return self._depth
    
    def setdepth(self, d):
        self._depth = d
        if self.left != None:
            self.left._depth = d + 1
        if self.right != None:
            self.right._depth = d + 1
            
    
    left = property(getleft, setleft)
    right = property(getright, setright)
    depth = property(getdepth, setdepth)
    

root = BNode("root")
root.left = BNode("left")
root.right = BNode("right")
root.left.left = BNode("left-left")
root.left.right = BNode("left-right")


class D(object):
    def __init__(self):
        self.__degree = 0
    
    def get_degree(self):
        return self.__degree
    
    def set_degree(self, d):
        self.__degree = d % 360
    
    degree = property(get_degree, set_degree)
