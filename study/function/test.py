'''
Created on 2009. 8. 14.

'''
import random
import study.function
import unittest




def roundList(l, places=7):
    return [ round(i, places) for i in l ]

class ReplaceListTestCase(unittest.TestCase):
    def testNormal(self):
        l = [1, 2, 3, 4, 5]
        study.function.practice.replaceList(l, 3, 4)
        self.assertEqual(l, [1, 2, 4, 4, 5])
        
        l = [l, l]
        study.function.practice.replaceList(l, 4, 5)
        

class AdderTestCase(unittest.TestCase):
    def testBasic(self):
        result = {
                  (0, 0) : (0, 0),
                  (1, 1): (1, 0),
                  (1, 0): (0, 1),
                  (0, 1): (0, 1)
                  }
        
        for args, rets in result.items():
            ret = study.function.practice.adder(*args)
            self.assertEqual(rets, ret)

class SumTestCase(unittest.TestCase):
    def testBasic(self):
        prefix = ["", "sdfsdf", "thumb", "_thumb_", "thumb_"]   
        postfix = [ "", "sdfsdfsdf", "___", "sdf"]
        extentsions = ["jpg", "jpge", "jjss", "exe", ""]        
        keyword = ["_thumb", "sdfsdf", "__", ".thumb", ""]
        
        args = []
        thumbmails = []
        normals = []
        for pre in prefix:
            for post in postfix:
                for ext in extentsions:
                    for keys in keyword:
                        name = pre + keys + post + "." + ext
                        args.append(name)
                        if keys == keyword[0] and ext == extentsions[0] and post == postfix[0]:
                            thumbmails.append(name)
                        elif ext == extentsions[0]:
                            normals.append(name)
        
        expectImgs = study.function.practice.getImages(args)
        expectThumbImgs = study.function.practice.getImages(args, thumb=True, normal=False)
        expectNormalImgs = study.function.practice.getImages(args, thumb=False, normal=True)
        
        print "expectImgs %r" % expectImgs
        print "expectThumbImgs %r" % expectThumbImgs
        print "expectNormalImgs %r" % expectNormalImgs
        
        
        self.assertEqual(sorted(expectImgs), sorted(normals + thumbmails))
        self.assertEqual(sorted(expectImgs), sorted(expectNormalImgs + expectThumbImgs))
        self.assertEqual(sorted(expectThumbImgs), sorted(thumbmails))
        self.assertEqual(sorted(expectNormalImgs), sorted(normals))
           
        
        
class FRangeTestCase(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
    
#    def roundList(l, places=7):
#        return [ round(i, places) for i in l ]
    
    def testExceptionCase(self):
        NullExpected = []
        for i in range(-100, 1000):
            result = study.function.practice.frange(i, i)
            self.assertEquals(NullExpected, result)
        
        self.assertEquals(NullExpected, study.function.practice.frange(-10, -10))
        
        self.assertEquals(NullExpected, study.function.practice.frange(100, 1000, -1))
        
    def testOneArgu(self):
        for i in range(-10, 1000):
            expected = [ (n / 4.0) for n in range(i)]
            result = study.function.practice.frange(i / 4.0)
            expected = roundList(expected)
            result = roundList(result)
            self.assertEquals(expected, result)
    
    def testThreeArgu(self):
        for i in range(-10, 1000):
            expected = [ n / 8.0 for n in range(-10, i)]
            result = study.function.practice.frange(-10 / 8.0, i / 8.0, 0.125)
            expected = roundList(expected)
            result = roundList(result)
            self.assertEquals(expected, result)
        
        for i in range(10, -1000):
            expected = [ n / 8.0 for n in range(10, i)]
            result = study.function.practice.frange(10 / 8.0, i / 8.0, -0.125)
            expected = roundList(expected)
            result = roundList(result)
            self.assertEquals(expected, result)
            
        self.assertRaises(ValueError, study.function.practice.frange, 1, 10, 0.0)      
        


    def testBasicOp(self):
        
        for i in range(-10, 1000):
            expected = [ n / 4.0 for n in range(-10, i) ]
            result = study.function.practice.frange(-10 / 4.0, i / 4.0)
            expected = roundList(expected)
            result = roundList(result)
            self.assertEquals(expected, result, "%r != %r when: %f %f" % (expected, result, -10 / 4.0, i / 4.0))
            
        for i in range(10, -1000, -1):
            expected = [ n / 4.0 for n in range(10, i, -1) ]
            result = study.function.practice.frange(10 / 4.0, i / 4.0, -0.25)
            expected = roundList(expected)
            result = roundList(result)
            self.assertEquals(expected, result, "%r != %r when: %f %f %f" % (expected, result, 10 / 4.0, i / 4.0, -0.25))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main(argv=('', '-v'))
