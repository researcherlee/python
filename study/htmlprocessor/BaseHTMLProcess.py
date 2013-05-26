'''
Created on 2009. 8. 9.

'''

from sgmllib import SGMLParser
import htmlentitydefs

class BaseHTMLProcess(SGMLParser):
    '''
    classdocs
    '''

    def appendSelfTag(self, tag, attr):
        attrs = "".join([' %s="%s"' % (key, value) for (key, value) in attr])
        self.pieces.append("<%(tag)s %(attrs)s/>" % locals())

    def reset(self):
        self.pieces = []
        SGMLParser.reset(self)
        pass
    
    def start_meta(self, attr):
        self.appendSelfTag("meta", attr)
        
    def start_link(self, attr):
        self.appendSelfTag("link", attr)
    
    def tag_meta(self, tag, attr):
        attrs = "".join([' %s="%s"' % (key, value) for key, value in attr ])
        self.pieces.append("<%(tag)s %(attrs)s/>" % locals() )
    
    def unknown_starttag(self, tag, attr):
        startattr = "".join([' %s="%s"' % (key, value) for key, value in attr ])
        self.pieces.append("<%(tag)s %(startattr)s>" % locals())
        
    
    def unknown_endtag(self, tag):
        self.pieces.append("</%s>" % tag)
        
    
    def handle_comment(self, text):
        self.pieces.append("<!-- %s -->" % text)
        
    
    def handle_data(self, text):
        self.pieces.append(text)
        
    
    def handle_decl(self, text):
        self.pieces.append("<!%s>" % text)
        
    
    def handle_charref(self, ref):
        self.pieces.append("&#%s;" % ref)
        
    def handle_entityref(self, ref):
        self.pieces.append("&%s" % ref)
        if htmlentitydefs.entitydefs.has_key(ref):
            self.pieces.append(";")
    
    def handle_pi(self, text):
        self.pieces.append("<?%s>", text)        
    
    def output(self):
        return "".join(self.pieces)
    
