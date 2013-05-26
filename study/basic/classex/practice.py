'''
Created on 2009. 8. 16.

@author: namjelee
'''


# Practice code

# staticmethod test
class D:
    
    def defineZ(self):
        self.z = 10
        print "z", self.z
        
    def spam(X, y):
        print "static method", X, y

  
    
    spam = staticmethod(spam)

# decorator

def myprint(a):
    
    def b(*args, **kwargs):
        print "before execute a"
        r = a(*args, **kwargs)
        print "result ", r
    
    return b


def accepts(*types):
    def check_accepts(f):      
        assert len(types) == f.func_code.co_argcount
        def new_f(*args, **kwargs):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), " arg %r does not match %s" % (a, t)
            return f(*args, **kwargs)
        
        #new_f.func_name = f.func_name
        return new_f    
    return check_accepts

import types
@ myprint
@ accepts(types.IntType)
def mysum(l):
    return sum(l)

