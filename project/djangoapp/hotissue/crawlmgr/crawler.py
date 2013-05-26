'''
Created on 2009. 9. 6.

'''
class Crawler:
    ''' Base class of Crawler. It include iterator property.'''
    url = ""
    
    def __init__(self, url):
        ''' Should be implemented additional pre parsing'''
        self.url = url
        pass
        
    # functions that are related to iterator #
    def __iter__(self):
        self.startIter = True
        self.go_recent()
        return self
    
    def next(self):
        if self.startIter == True:
            self.startIter = False
            return self.get_page_info()
        
        try:
            self.go_next()
        except IndexError:
            raise StopIteration
        return self.get_page_info()
    
    # Navigation functions
    def go_next(self, step = 1):
        raise NotImplementedError
    
    def go_previous(self, step = 1):
        raise NotImplementedError
    
    def go_article_num(self, articleNum):
        raise NotImplementedError
    
    def go_absolute_url(self, url):
        raise NotImplementedError
    
    def go_recent(self):
        raise NotImplementedError
    
    def go_oldest(self):
        raise NotImplementedError
    
    # Get Property for the blog
    def get_length(self):
        raise NotImplementedError
    
    def get_tag(self):
        raise NotImplementedError
    
    def get_catalog_list(self):
        """return the list of tuples ( URL, "Tag" )"""
        raise NotImplementedError
    
    def get_catalog_crawler(self, name):
        raise NotImplementedError
    
    def get_page_info(self):
        """Parse current and return the parsed page info."""
        raise NotImplementedError
    
#    def get_page_images(self, sizeFilter = 1024*15, extFilter = [ "jpg", "gif", "png", "jpeg", "bmp" ] ):
#        return []


class PageInfo:
    """
    It represents the one web pages in the internet
    """

    url = ""
    articleNum = ""     # In case of blog, blog page id usuaaly is number
    imageUrls = []  # List of image info
    modifiedDate = None
    tag = ""
    
    def __cmp__(self, other):
        if self.url != other.url:
            return -1
        if self.articleNum != other.articleNum:
            return -1
        if self.imageUrls != other.imageUrls:
            return -1
        if self.tag != other.tag:
            return -1
        return 0



class ImageInfo:
    width = ""
    height = ""
    ext = ""
    url = ""
    tag = ""
