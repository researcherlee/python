'''
Created on 2009. 8. 9.

'''
import BaseHTMLProcess
import os
import sys
import getopt
import test_htmlprocessor
import urllib2
import urlparse

class TextEncodeChange(BaseHTMLProcess.BaseHTMLProcess):
    def reset(self):
        self.srcEncode = "euckr"
        self.dstEncode = "utf8"
        
        BaseHTMLProcess.BaseHTMLProcess.reset(self)
        pass
    
    
    def setSrcEncode(self, encode):
        self.srcEncode = encode
    
    def setDstEncode(self, encode):
        self.dstEncode = encode
    
    def handle_comment(self, text):
        text = text.decode(self.srcEncode).encode(self.dstEncode)
        self.pieces.append("<!-- %s -->" % text)
 

    def handle_data(self, text):
        text = text.decode(self.srcEncode).encode(self.dstEncode)
        self.pieces.append(text)
    
    def getStream(self, source):
        retData = ""
        sock = None
        if source.startswith("http://"):
            sock = urllib2.urlopen(source)
        else:
            sock = open(source)

        retData = sock.read()
        return retData
            
        
if __name__ == "__main__":
    helpMsg = """
Usage: htmlencodeChange [-s (euckr|utf8) -d (euckr|utf8) ] <files>
    -s  source encode, default is euckr
    -d  destination encode, default is utf8
    <files> URL ro filePath
    
    ** -t  testing mode
    """
    srcEncode = "euckr"
    dstEncode = "utf8"
    def usage():
        print helpMsg
        sys.exit()
        
    options, arguments = getopt.getopt(sys.argv[1:], "s:d:t")
    
    for k, v in options:
        if k == "-s" and v:
            srcEncode = v
        elif k == "-d" and v:
            dstEncode = v
        elif k == "-t":
            arguments = test_htmlprocessor.testfeeds
        else:
            usage()
    
    if len(arguments) == 0:
        usage()
    
    print "========= Start convert %s to %s =========" % (srcEncode, dstEncode)
    i = 1
    for url in arguments:
        try:
            parser = TextEncodeChange()
            parser.setSrcEncode(srcEncode)
            parser.setDstEncode(dstEncode)
            html = parser.getStream(url)
            print "%d: %s converting..." % (i, url), 
            i = i+1
            parser.feed(html)
            parser.close()
            retVal = parser.output()
            
            # backup existing file
            if os.path.exists(url):
                os.rename(url, url + ".back")
            else:
                url = os.getcwd() + os.sep + os.path.basename(urlparse.urlparse(url)[2])
                while os.path.exists(url):
                    url = url + "_"                
            
            sock = open(url, "w")
            sock.write(retVal)
            sock.close()          
            
            print "... completed saved in %s" % url
        except:
            print >>sys.stderr, "<< Error: %s" % str(sys.exc_info())
    