'''
Created on 2009. 8. 9.

'''
import BaseHTMLProcess
import unittest
import euckr2utf8
import urllib2

testfeeds = [ 
                      "http://reliableelee.com/vicode/parkingsystem.shtml",
                      "http://reliableelee.com/vicode/downloads.shtml",
                      "http://reliableelee.com/vicode/index.html",
                      "http://reliableelee.com/vicode/doc/index.html",
                      ]

class TestBaseHTMLProcess(unittest.TestCase):

    def assertEqualLongString(self, a, b):
        NOT, POINT = '-', '*'
        if a != b:
            print a
            o = ''
            for i, e in enumerate(a):
                try:
                    if e != b[i]:
                        o += POINT
                    else:
                        o += NOT
                except IndexError:
                    o += '*'

            o += NOT * (len(a)-len(o))
            if len(b) > len(a):
                o += POINT* (len(b)-len(a))

            print o
            print b

            raise AssertionError, '(see string comparison above)'
    
    def setUp(self):
        self.feeds = testfeeds;
        
        
    def testHtml(self):
        for url in self.feeds:
            sock = urllib2.urlopen(url)
            originalData = sock.read()
            htmlParser = BaseHTMLProcess.BaseHTMLProcess()
            htmlParser.feed(originalData)
            htmlParser.close()
            returnData = htmlParser.output()
            
            def removeSpacenQuota(s):
                s = "".join(s.split())
                s = "".join(s.split('"'))
                s = "".join(s.split("'"))
                s = s.lower()
                return s
            
            returnData = removeSpacenQuota(returnData)
            originalData = removeSpacenQuota(originalData)
            
            self.assertEqualLongString(returnData, originalData)
            
            self.assertEqual(originalData, returnData)
    
    def testDoubleCheck(self):
        for url in self.feeds:
            sock = urllib2.urlopen(url)
            originalData = sock.read()
            htmlParser = BaseHTMLProcess.BaseHTMLProcess()
            htmlParser.feed(originalData)
            htmlParser.close()
            returnData = htmlParser.output()
            
            htmlParser = BaseHTMLProcess.BaseHTMLProcess()
            htmlParser.feed(returnData)
            htmlParser.close()
            originalData = htmlParser.output()
            
            def removeSpacenQuota(s):
                s = "".join(s.split())
                s = "".join(s.split('"'))
                s = "".join(s.split("'"))
                s = s.lower()
                return s
            
            returnData = removeSpacenQuota(returnData)
            originalData = removeSpacenQuota(originalData)
            
            self.assertEqualLongString(returnData, originalData)
            
            self.assertEqual(originalData, returnData)
            
    def testEncodeEuckr2Utf8(self):
        for url in self.feeds:
            sock = urllib2.urlopen(url)
            originalData = sock.read()
            htmlParser = euckr2utf8.TextEncodeChange()
            htmlParser.feed(originalData)
            htmlParser.close()
            returnData = htmlParser.output()
            
            htmlParser = euckr2utf8.TextEncodeChange()
            htmlParser.setDstEncode("euckr")
            htmlParser.setSrcEncode("utf8")
            htmlParser.feed(returnData)
            htmlParser.close()
            returnData = htmlParser.output()
            
            def removeSpacenQuota(s):
                s = "".join(s.split())
                s = "".join(s.split('"'))
                s = "".join(s.split("'"))
                s = s.lower()
                return s
            
            returnData = removeSpacenQuota(returnData)
            originalData = removeSpacenQuota(originalData)
            
            self.assertEqualLongString(returnData, originalData)
            
            self.assertEqual(originalData, returnData)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
#    for url in testfeeds:
#        sock = urllib2.urlopen(url)
#        originalData = sock.read()
#        htmlParser = euckr2utf8.TextEncodeChange()
#        htmlParser.feed(originalData)
#        htmlParser.close()
#        returnData = htmlParser.output()
#        print "========== %s ==========" % url
#        print returnData
        